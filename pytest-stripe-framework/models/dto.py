from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class CustomerDTO(BaseModel):
    name: str = Field(..., description="Full name of the customer")
    email: EmailStr = Field(..., description="Email address of the customer")
    description: Optional[str] = Field(None, description="Arbitrary description")

class PaymentIntentDTO(BaseModel):
    amount: int = Field(..., ge=1, description="Amount in cents")
    currency: str = Field(..., min_length=3, max_length=3, description="3-letter ISO currency code")
    payment_method_types: list[str] = Field(default=["card"])
    description: Optional[str] = None
    confirm: bool = False

class RefundDTO(BaseModel):
    payment_intent: str = Field(..., description="ID of the PaymentIntent to refund")
    amount: Optional[int] = Field(None, description="Amount to refund, defaults to full amount")
