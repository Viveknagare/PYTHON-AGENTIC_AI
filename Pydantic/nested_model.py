from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    street: str
    city: str
    postal_code: str


class User(BaseModel):
    id: int
    name: str
    address: Address

address = Address(
    street="Ghatkopar",
    city="mumbai",
    postal_code="400075"
)

user = User(
    id=1,
    name="Vivek",
    address=address
)

print(user)

user1 = User(
    id=2,
    name="Sakshi",
    address={
        "street" : "Ghatkopar",
        "city": "Mumbai",
        "postal_code": "400075"
    }
)

print(user1)
