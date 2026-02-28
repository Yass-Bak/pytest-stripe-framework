from clients.stripe_client import StripeClient
from models.dto import PaymentIntentDTO

class PaymentService:
    def __init__(self, client: StripeClient):
        self.client = client

    def create_payment_intent(self, payment_dto: PaymentIntentDTO):
        """
        Creates a payment intent.
        """
        data = payment_dto.model_dump(exclude_none=True)
        # Fix array params
        payload = {}
        for key, value in data.items():
            if isinstance(value, list):
                for i, v in enumerate(value):
                    payload[f"{key}[{i}]"] = v
            else:
                payload[key] = value

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
