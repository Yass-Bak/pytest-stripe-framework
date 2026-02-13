from clients.stripe_client import StripeClient
from models.dto import CustomerDTO

class CustomerService:
    def __init__(self, client: StripeClient):
        self.client = client

    def create_customer(self, customer_dto: CustomerDTO):
        """
        Creates a new customer in Stripe.
        """
        response = self.client.post("customers", data=customer_dto.model_dump(exclude_none=True))
        return response

    def get_customer(self, customer_id: str):
        """
        Retrieves a customer by ID.
        """
        return self.client.get(f"customers/{customer_id}")

    def delete_customer(self, customer_id: str):
        """
        Deletes a customer by ID.
        """
        return self.client.delete(f"customers/{customer_id}")
