# test_my_assistant.py
# Author: Alyxandria Gibson

from fake_model import FakeModel
from keyword_model import KeywordModel
from my_assistant import FAQAssistant
from my_queue import WarrantyQueue
from my_tool import FAQKnowledgeBase
from my_toolbox import FAQToolbox


class SilentModel:
    """A model that never has an answer. It stands in for Ollama being switched off."""

    def decide(self, instructions, history, tools):
        return None


def make_assistant(model):
    faq_tool = FAQKnowledgeBase(
        {"hours": "9 am to 5 pm", "shipping": "3-5 business days"}
    )
    tools = FAQToolbox(faq_tool, WarrantyQueue(faq_tool))
    return FAQAssistant("Bizzy", "Be clear.", tools, model)


def claim(item, customer):
    """Build the decision a model returns when it wants to request a warranty claim."""
    arguments = {"item": item, "customer": customer}
    return {"tool": "request_warranty_claim", "arguments": arguments}


def test_model_can_ask_for_faq():
    model = FakeModel(
        [
            {"tool": "look_up_faq", "arguments": {"topic": "hours"}},
            {"text": "We are open 9 am to 5 pm."},
        ]
    )
    assistant = make_assistant(model)
    assistant.respond("What are your hours?")
    assert assistant.history[1]["content"] == "9 am to 5 pm"


def test_warranty_claim_waits_for_staff():
    model = FakeModel([claim("rain jacket", "Luna Lopez"), {"text": "Sent."}])
    assistant = make_assistant(model)
    assistant.respond("Please file a warranty claim for my rain jacket for Luna Lopez")
    assert len(assistant.tools.warranty_queue.waiting()) == 1
    assert assistant.tools.faq_tool.warranty_claims == []


def test_made_up_name_is_refused():
    model = FakeModel([claim("rain jacket", "John Doe"), {"text": "Name?"}])
    assistant = make_assistant(model)
    assistant.respond("Please file a warranty claim for my rain jacket")
    assert "has not given that name" in assistant.history[1]["content"]
    assert assistant.tools.warranty_queue.waiting() == []


def test_approval_records_the_claim_once():
    faq_tool = FAQKnowledgeBase({"warranty": "1-year warranty"})
    queue = WarrantyQueue(faq_tool)
    queue.request_warranty_claim("rain jacket", "Luna Lopez")
    queue.approve(1)
    queue.approve(1)
    assert len(faq_tool.warranty_claims) == 1


def test_cancellation_goes_to_human():
    assistant = make_assistant(FakeModel([]))
    assert "human agent" in assistant.respond("I want a refund for my order")


def test_keyword_model_still_greets():
    assistant = make_assistant(KeywordModel())
    assert assistant.respond("hello") == "Hello! How can I help you today?"
