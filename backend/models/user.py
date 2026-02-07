from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
import datetime

class User(SQLModel, table=True):
    __tablename__ = "app_user"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    password_hash: str = Field(nullable=False)
    full_name: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    conversations: List["Conversation"] = Relationship(back_populates="owner")
    messages: List["Message"] = Relationship(back_populates="owner")
    tasks: List["Task"] = Relationship(back_populates="owner")