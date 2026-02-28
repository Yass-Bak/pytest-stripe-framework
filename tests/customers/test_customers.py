import pytest
import allure
import uuid
from models.dto import CustomerDTO
from utils.validator import Validator

@allure.feature("Customer Management")
class TestCustomers:

    @pytest.fixture
    def new_customer(self, customer_service):
        email = f"test_{uuid.uuid4()}@example.com"
        dto = CustomerDTO(name="Test User", email=email, description="Automated test customer")
        return dto

    @allure.story("Create Customer")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_customer(self, customer_service, new_customer, schemas):
        with allure.step("Send create customer request"):
            response = customer_service.create_customer(new_customer)
        
        with allure.step("Verify response status"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
        with allure.step("Validate response schema"):
            data = response.json()
            Validator.validate_schema(data, schemas['customer_schema'])
            
        with allure.step("Verify customer data"):
            assert data['email'] == new_customer.email
            assert data['name'] == new_customer.name

    @allure.story("Get Customer")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_customer(self, customer_service, new_customer):
        # Setup: create customer first
        create_res = customer_service.create_customer(new_customer)
        customer_id = create_res.json()['id']
        
        with allure.step(f"Retrieve customer {customer_id}"):
            response = customer_service.get_customer(customer_id)
            
        with allure.step("Verify response"):
            assert response.status_code == 200
            assert response.json()['id'] == customer_id

    @allure.story("Delete Customer")
    def test_delete_customer(self, customer_service, new_customer):
        create_res = customer_service.create_customer(new_customer)
        customer_id = create_res.json()['id']
        
        with allure.step(f"Delete customer {customer_id}"):
            response = customer_service.delete_customer(customer_id)
            
        with allure.step("Verify deletion status"):
            assert response.status_code == 200
            assert response.json()['deleted'] is True
            
        with allure.step("Verify customer is gone"):
            get_res = customer_service.get_customer(customer_id)
            assert get_res.json()['deleted'] is True 
            # Note: Stripe returns the deleted object with 'deleted': true when getting generic resource? 
            # Or maybe 404? 
            # For Stripe, retrieving a deleted customer usually returns the object with deleted=true.
