# my_tool.py
# Author: Alyxandria Gibson


class FAQKnowledgeBase:
    """A tool that looks up store policies and frequently asked questions."""

    def __init__(self, faq_data):
        """Store the FAQ dictionary with topic keywords to policy details."""
        self.faq_data = faq_data
        self.warranty_claims = []

    def find_topic(self, text):
        """Return the first known topic found in the message text, or None."""
        text_lower = text.lower()
        for topic in self.faq_data:
            topic_lower = topic.lower()
            if topic_lower == "policy":
                if "store policy" in text_lower or "warranty" in text_lower:
                    return topic
                continue
            if topic_lower in text_lower:
                return topic
        return None

    def answer_for(self, topic):
        """Return the answer for a specific topic, or None if the topic is unknown."""
        if topic is None:
            return None
        return self.faq_data.get(topic)

    def look_up_faq(self, topic):
        """Look up the store information or policy for a specific topic.

        Args:
            topic: The topic to look up, such as hours, shipping, or warranty.
        """
        return self.faq_data.get(topic)

    def record_warranty_claim(self, product, customer_name):
        self.warranty_claims.append(
            {
                "product": product,
                "customer": customer_name,
            }
        )
