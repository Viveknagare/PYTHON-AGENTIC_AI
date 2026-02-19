from pydantic import BaseModel;

class Product(BaseModel):
    id: int
    name: str
    price: float
    is_stock: bool = True

product1 = Product(id = 1, name = "Laptop", price = 75000)
product2 = Product(id = '11', name = "Phone", price = 40000, is_stock = False)

print(product1)
print(product2)