# my_toolbox.py
# Author: Alyxandria Gibson


class FAQToolbox:
    """Every tool request from tje model comes through here and is checked."""

    def __init__(self, faq_tool, warranty_queue):
        """Hold the tools the model is allowed to ask for."""
        self.faq_tool = faq_tool
        self.warranty_queue = warranty_queue

    def tool_list(self):
        """Return the tpp;s the model may ask for. They are not called here."""
        return [
            self.faq_tool.look_up_faq,
            self.warranty_queue.request_warranty_claim,
        ]

    def run(self, name, arguments, history):
        """Check one tool request. Run the tool only if every test passes."""
        if name == "look_up_faq":
            topic = self.clean(arguments, "topic")
            if topic == "":
                return "The topic is missing. Ask the client which topic."
            return self.faq_tool.look_up_faq(topic)
        if name == "request_warranty_claim":
            item = self.clean(arguments, "item")
            customer = self.clean(arguments, "customer")
            if item == "" or customer == "":
                return "The product and the customer's name are both needed."
            if not self.client_said(history, item):
                return "The client has not given that product. Ask them for it."
            if not self.client_said(history, customer):
                return "The client has not given that name. Ask them for it."
            return self.warranty_queue.request_warranty_claim(item, customer)
        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return one argument as text without extra spaces, or "" if it is missing."""
        return str(arguments.get(key, "")).strip()

    def client_said(self, history, text):
        """Return True if text appears in a message the client typed."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
