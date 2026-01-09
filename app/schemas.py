from pydantic import BaseModel
from typing import List

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    image: str
    category: str

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True

class ProductDetail(ProductOut):
    pass

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemOut(BaseModel):
    id: int
    quantity: int
    product: ProductOut

    class Config:
        orm_mode = True
