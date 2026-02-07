from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
import datetime

from .user import User

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="app_user.id")
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    owner: Optional[User] = Relationship(back_populates="tasks")