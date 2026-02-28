from pydantic import BaseModel
from typing import List, Optional, Union

class Address(BaseModel):
    street: str
    city: str
    postal_code: str

class Company(BaseModel):
    name: str
    Address: Optional[Address] = None

class Employee(BaseModel):
    name: str
    company: Optional[Company] = None

class Textcontent(BaseModel):
    type: str = "text"
    content: str

class ImageContent(BaseModel):
    type: str = "Image"
    url: str
    alt_url: str

class Article(BaseModel):
    title: str
    sections: list[Union[Textcontent, ImageContent]] = None

    