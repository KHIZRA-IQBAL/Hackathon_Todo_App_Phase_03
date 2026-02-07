from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
import datetime

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: Optional[int] = Field(default=None, foreign_key="conversations.id")
    user_id: Optional[int] = Field(default=None, foreign_key="app_user.id")
    role: str = Field(nullable=False)
    content: str = Field()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
    owner: Optional["User"] = Relationship(back_populates="messages")
