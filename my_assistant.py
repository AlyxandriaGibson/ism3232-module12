# my_assistant.py
# Author: Alyxandria Gibson


HANDOFF_WORDS = ["refund", "dispute", "return", "complaint"]
MAX_TOOL_ROUNDS = 3


class FAQAssistant:
    """An assistant for Tampa Outfitters. The model decides. The toolbox checks every request."""

    def __init__(self, name, instructions, tools, model):
        """Set up an assistant with its own name, instructions, tool, model, and history."""
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the message, determine a reply, record the reply, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Send financial and return requests to a person. Send the rest to the model."""
        if self.needs_human(user_message.lower()):
            return "Financial and return requests require a human agent. I am routing you to customer support."
        return self.model_reply()

    def needs_human(self, text):
        """Return True if the request requires a human to handle it."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def model_reply(self):
        """Ask the model. Run each tool it asks for, then ask again, up to a limit."""
        rounds = 0
        while rounds < MAX_TOOL_ROUNDS:
            tool_list = self.tools.tool_list()
            decision = self.model.decide(self.instructions, self.history, tool_list)
            if decision is None:
                return (
                    "I'm sorry, I can't answer that right now, please try again later."
                )
            if "text" in decision:
                return decision["text"]
            name = decision["tool"]
            arguments = decision["arguments"]
            result = self.tools.run(name, arguments, self.history)
            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )
            rounds += 1
        return "Sorry, I couldn't finish that. I am routing you to customer support."
