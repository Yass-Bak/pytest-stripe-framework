import pytest
import os
import json
import logging
from clients.stripe_client import StripeClient
from services.customer_service import CustomerService
from services.payment_service import PaymentService
from services.refund_service import RefundService
from utils.logger import logger

@pytest.fixture(scope="session")
def client():
    """
    Session-scoped client to reuse TCP connections.
    """
    return StripeClient()

@pytest.fixture(scope="function")
def customer_service(client):
    return CustomerService(client)

@pytest.fixture(scope="function")
def payment_service(client):
    return PaymentService(client)

@pytest.fixture(scope="function")
def refund_service(client):
    return RefundService(client)

@pytest.fixture(scope="session")
def schemas():
    """
    Loads all schemas into a dictionary.
    """
    schema_dir = os.path.join(os.path.dirname(__file__), 'schemas')
    schemas = {}
    for filename in os.listdir(schema_dir):
        if filename.endswith('.json'):
            name = filename.replace('.json', '')
            with open(os.path.join(schema_dir, filename)) as f:
                schemas[name] = json.load(f)
    return schemas

@pytest.fixture(autouse=True)
def log_test_name(request):
    logger.info(f"STARTING TEST: {request.node.name}")
    yield
    logger.info(f"FINISHED TEST: {request.node.name}")

