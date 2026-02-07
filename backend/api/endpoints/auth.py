from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from api import deps
from core.security import create_access_token
from crud import user as user_crud
from schemas.user import UserCreate, Token, User

router = APIRouter()

@router.post("/register", response_model=Token)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
):
    """
    Create new user and return access token.
    """
    user = user_crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=409, # Changed to 409 Conflict
            detail="The user with this email already exists in the system.",
        )
    try:
        user = user_crud.create_user(db, user_in=user_in)
    except ValueError as e: # Catch the custom error from crud
        raise HTTPException(
            status_code=409, # 409 Conflict is more appropriate for duplicate resource
            detail=str(e),
        )
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login_for_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    print(f"Login attempt: Email={form_data.username}, Password={'*' * len(form_data.password)}") # Debug print
    user = user_crud.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        print("Login failed: Invalid credentials or user not found.") # Debug print
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password.", # More specific detail
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(f"Login successful for user ID: {user.id}") # Debug print
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_user_me(
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get current user.
    """
    return current_user
