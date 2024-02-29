from pydantic import BaseModel


class ProductCreate(BaseModel):
    title: str
    description: str
    brand: str
    price: int
    category: str


class ProductResponse(ProductCreate):
    id: int


class CategoryCreate(BaseModel):
    title: str



class CategoryResponse(CategoryCreate):
    id: int
