from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError # Import IntegrityError

from core.security import get_password_hash, verify_password
from models.user import User
from schemas.user import UserCreate

def get_user_by_email(db: Session, *, email: str) -> Optional[User]:
    return db.exec(select(User).where(User.email == email)).first()

def create_user(db: Session, *, user_in: UserCreate) -> User:
    password_hash = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=password_hash,
    )
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError: # Catch the specific error
        db.rollback() # Rollback the session on error
        raise ValueError("Email already registered") # Raise a custom error that auth.py can catch
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, *, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
