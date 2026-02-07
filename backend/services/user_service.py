from typing import Dict, Any
from sqlmodel import Session, select
from fastapi import HTTPException
from models import User

class UserService:
    def update_user(self, db: Session, user: User, user_data: Dict[str, Any]) -> User:
        for key, value in user_data.items():
            setattr(user, key, value)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

user_service = UserService()