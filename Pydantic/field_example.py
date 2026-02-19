from pydantic import BaseModel;
from typing import List, Dict, Optional

class Cart(BaseModel):
    user_id: int
    items: List[str]
    quantity: Dict[str,int]

class BlogPost(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

cart_data = {
    "user_id": 124, 
    "items": ["Laptop", "Mobile", "Phone"],
    "quantity": {"Laptop": 3, "Mobile": 2, "Phone": 5}
}