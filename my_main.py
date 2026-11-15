# my_main.py
# Author: Alyxandria Gibson

from my_assistant import FAQAssistant
from my_queue import WarrantyQueue
from my_tool import FAQKnowledgeBase
from my_toolbox import FAQToolbox
from ollama_model import OllamaModel

FAQ_DATA = {
    "hours": "We are open from 9 AM - 5 PM, Monday through Friday.",
    "shipping": "Standard shipping takes 3-5 business days, and is free on orders over $60.",
    "warranty": "We offer a 1-year warranty on all products.",
}


INSTRUCTIONS = """You are Bizzy, a helpful customer service assistant for Tampa Outfitters.
Answer in one short sentence.
If the client only says hello, greet them and ask how you can help.
Store hours are 9 AM to 5 PM, Monday through Friday.
Standard shipping takes 3-5 business days, and is free on orders over $60.
Store policy offers a 1-year warranty on all products.
To request a warranty claim you need the product name and the customer's full name.
Only state facts in these instructions or in tool results.
If you do not know the answer, say you do not know and offer to pass the customer to a human agent."""


faq_tool = FAQKnowledgeBase(FAQ_DATA)
warranty_queue = WarrantyQueue(faq_tool)
tools = FAQToolbox(faq_tool, warranty_queue)
model = OllamaModel("granite4.1:3b")
assistant = FAQAssistant("Bizzy", INSTRUCTIONS, tools, model)


print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{assistant.name}: {assistant.respond(user_message)}")
    user_message = input("You: ")


print(f"Messages in this conversation: {len(assistant.history)}")


print("Staff review")
for request in warranty_queue.waiting():
    number = request["number"]
    print(f"Request {number}: {request['customer']}, {request['item']}")
    answer = input("Approve? yes or no: ")
    if answer == "yes":
        print(warranty_queue.approve(number))
    else:
        print(warranty_queue.reject(number))


print(f"Claims: {len(faq_tool.warranty_claims)}")
