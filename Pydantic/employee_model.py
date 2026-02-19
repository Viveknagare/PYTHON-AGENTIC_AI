from pydantic import BaseModel, Field
from typing import Optional

class Employee(BaseModel):
    id: int
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Employee Name",
        examples="Vivek Nagare"
    )

    department: Optional[str] = "General"
    salary: float = Field(
        ...,
        ge=1000,
        le=100000,
        description="Salary",
        examples=10000
    )

class User(BaseModel):
    email: str = Field(..., pattern = r'')
    phone: str = Field(..., pattern = r'')
    age: int = Field(
        ...,
        ge=18,
        le=100,
        description="age of a person"
    )
    discount: float = Field(
        ...,
        ge=0,
        le=100,
        description="Discount Percentage"
    )