import pytest
import allure
from models.dto import RefundDTO, PaymentIntentDTO

@allure.feature("Refund Management")
class TestRefunds:

    @allure.story("Create Refund")
    def test_create_refund(self, payment_service, refund_service):
        # 1. Create PI
        pi_dto = PaymentIntentDTO(amount=1000, currency="usd", payment_method_types=["card"])
        pi = payment_service.create_payment_intent(pi_dto).json()
        pi_id = pi['id']
        
        # 2. Confirm PI (Refunds require a charge, usually generated after confirmation)
        # However, for 'payment_intent', we need a successful charge.
        # Confirming with pm_card_visa usually succeeds immediately.
        payment_service.confirm_payment(pi_id, "pm_card_visa")
        
        # 3. Refund
        # We might need to wait for status to be succeeded.
        # For simplicity, we attempt refund. If not chargeable yet, might fail.
        # But in sandbox, it's usually instant.
        
        refund_dto = RefundDTO(payment_intent=pi_id, amount=500)
        
        with allure.step("Issue refund"):
            response = refund_service.create_refund(refund_dto)
            
        with allure.step("Verify refund"):
            # If status is not succeeded, refund might fail with 400.
            # We Assert 200 assuming happy path works in sandbox.
            assert response.status_code == 200, f"Refund failed: {response.text}"
            assert response.json()['amount'] == 500
            assert response.json()['status'] == "succeeded" # or 'pending'
