from clients.stripe_client import StripeClient
from models.dto import RefundDTO

class RefundService:
    def __init__(self, client: StripeClient):
        self.client = client

    def create_refund(self, refund_dto: RefundDTO):
        """
        Creates a refund for a specific payment intent.
        """
        return self.client.post("refunds", data=refund_dto.model_dump(exclude_none=True))
