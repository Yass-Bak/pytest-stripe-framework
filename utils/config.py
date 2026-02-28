import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

class Config:
    BASE_URL = os.getenv("STRIPE_BASE_URL", "https://api.stripe.com/v1")
    API_KEY = os.getenv("STRIPE_API_KEY")
    TIMEOUT = int(os.getenv("TIMEOUT", "30"))
    ENVIRONMENT = os.getenv("ENVIRONMENT", "sandbox")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls):
        if not cls.API_KEY:
            raise ValueError("STRIPE_API_KEY environment variable is mandatory")
