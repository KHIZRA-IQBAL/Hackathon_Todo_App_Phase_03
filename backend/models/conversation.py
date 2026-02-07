from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
import datetime

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="app_user.id")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    owner: Optional["User"] = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")
