from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from api import deps
from models import User
from schemas.user import UserUpdateProfile, User as UserSchema
from services.user_service import user_service # Assuming a user_service will be created/updated

router = APIRouter()

@router.put("/profile", response_model=UserSchema)
def update_user_profile(
    user_update: UserUpdateProfile,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update the current user's profile information.
    """
    if user_update.full_name is not None:
        return user_service.update_user(db=db, user=current_user, user_data={"full_name": user_update.full_name})
    
    raise HTTPException(status_code=400, detail="No updatable fields provided")

