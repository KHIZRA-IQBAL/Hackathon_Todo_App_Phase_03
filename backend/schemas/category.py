from typing import Optional

from sqlmodel import SQLModel

class CategoryBase(SQLModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True