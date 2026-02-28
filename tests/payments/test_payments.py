import pytest
import allure
from models.dto import PaymentIntentDTO
from utils.validator import Validator

@allure.feature("Payment Processing")
class TestPayments:

    @pytest.fixture
    def payment_intent_dto(self):
        return PaymentIntentDTO(
            amount=2000, 
            currency="usd", 
            payment_method_types=["card"], # Note: handled as 'payment_method_types': ['card'] which requests might serialize to key=value&key=value .. Stripe accepts this often or key[]=value
            description="Test Payment"
        )

    @allure.story("Create Payment Intent")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_payment_intent(self, payment_service, payment_intent_dto, schemas):
        with allure.step("Create payment intent"):
            # Workaround for list serialization if needed, requests handles list as repeated keys
            # Stripe accepts repeated keys for array params in form-url-encoded
            response = payment_service.create_payment_intent(payment_intent_dto)
        
        with allure.step("Check response"):
            assert response.status_code == 200, f"Failed: {response.text}"
            
        with allure.step("Validate schema"):
            Validator.validate_schema(response.json(), schemas['payment_schema'])
            
        with allure.step("Verify amount"):
            assert response.json()['amount'] == 2000

    @allure.story("Confirm Payment")
    def test_confirm_payment(self, payment_service, payment_intent_dto):
        # Setup
        pi = payment_service.create_payment_intent(payment_intent_dto).json()
        pi_id = pi['id']
        
        with allure.step(f"Confirm payment {pi_id}"):
            # We need a payment method attached. 
            # Standard flow: create PI -> attach PM (or pass pm id during confirm) -> confirm
            # Using 'pm_card_visa' test token
            response = payment_service.confirm_payment(pi_id, payment_method="pm_card_visa")
            
        # In some flows confirmation might fail if requires_action (3DS), but sandbox cards usually succeed
        with allure.step("Verify confirmation"):
            assert response.status_code in [200, 202] # 202 if processing
            status = response.json()['status']
            assert status in ["succeeded", "processing", "requires_capture"]
