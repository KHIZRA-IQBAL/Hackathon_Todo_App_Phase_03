from datetime import date
from typing import Optional


from sqlmodel import SQLModel

class CategoryBase(SQLModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryPublic(CategoryBase):
    id: int

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = None  # Simple string field - "low", "medium", "high" etc.
    due_date: Optional[date] = None
    category_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    category_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    user_id: int
    category: Optional[CategoryPublic] = None