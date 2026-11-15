# my_queue.py
# Author: Alyxandria Gibson


class WarrantyQueue:
    """Warranty requests waiting for staff approval. Nothing is registered until then."""

    def __init__(self, faq_tool):
        """Start with no requests. Approved claims go into the FAQ tool."""
        self.faq_tool = faq_tool
        self.requests = []

    def request_warranty_claim(self, product, customer_name):
        """Ask staff to approve a product warranty request. Staff must approve it.

        Args:
            product: The product name, like rain jacket.
            customer_name: The customer's full name.
        """
        number = len(self.requests) + 1
        request = {
            "number": number,
            "item": product,
            "customer": customer_name,
            "status": "waiting",
        }
        self.requests.append(request)
        return f"Request {number} was sent to staff. Nothing has been recorded yet."

    def waiting(self):
        """Return the requests that are still waiting for a decision."""
        result = []
        for request in self.requests:
            if request["status"] == "waiting":
                result.append(request)
        return result

    def find(self, number):
        """Return the request with this number, or None."""
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        """Approve one waiting request and record the claim."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "approved"
        self.faq_tool.record_warranty_claim(request["item"], request["customer"])
        return f"Request {number} approved."

    def reject(self, number):
        """Reject one waiting request. Nothing is recorded."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "rejected"
        return f"Request {number} was rejected."
