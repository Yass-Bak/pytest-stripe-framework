from clients.stripe_client import StripeClient
from models.dto import PaymentIntentDTO

class PaymentService:
    def __init__(self, client: StripeClient):
        self.client = client

    def create_payment_intent(self, payment_dto: PaymentIntentDTO):
        """
        Creates a payment intent.
        """
        # Pydantic dump needs to handle list for form-urlencoded correctly if complicated,
        # but requests handles simple lists. Stripe expects 'payment_method_types[]': 'card'
        # We might need custom serialization for arrays if requests doesn't handle it the way Stripe wants.
        # Stripe usually wants: payment_method_types[0]=card
        # For simplicity in this demo, we assume standard dict or handle basic list.
        # Let's adjust manually if needed, or trust requests/stripe compat.
        payload = payment_dto.model_dump(exclude_none=True)
        return self.client.post("payment_intents", data=payload)

    def confirm_payment(self, payment_intent_id: str, payment_method="pm_card_visa"):
        """
        Confirms a payment intent.
        For testing, we use a test payment method like pm_card_visa.
        """
        return self.client.post(f"payment_intents/{payment_intent_id}/confirm", data={"payment_method": payment_method})

    def retrieve_payment(self, payment_intent_id: str):
        """
        Retrieves a payment intent.
        """
        return self.client.get(f"payment_intents/{payment_intent_id}")
