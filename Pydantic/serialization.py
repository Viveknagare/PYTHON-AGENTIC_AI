from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    id:int
    name: str
    email: str
    is_active: bool
    createdAt:datetime
    address: Address
    tags: List[str] = []

    model_config = ConfigDict(
    json_encoders={datetime: lambda v: v.strftime('%d-%m-%y %H:%M:%S')}
    )




user = User(
    id= 1,
    name= "vivek",
    email= "bvcoevivek31@gmail.com",
    is_active= True,
    createdAt=datetime(2026, 1, 31, 14, 30, 21),
    address=Address(
        street= "ghatkopar",
        city="mumbai",
        zip_code = "400075"
    ),
    tags = ["premium", "subscriber"]
)

python_dict = user.model_dump()
print(user)
print("="*30)
print(python_dict)
python_json = user.model_dump_json()
print("="*30)
print(python_json)