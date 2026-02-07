from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List, Optional
from pydantic import BaseModel

from api import deps
from models import User
from services.chat_service import chat_service

router = APIRouter()


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: Optional[List] = None


@router.post("", response_model=ChatResponse)
def handle_chat(
    *,
    db: Session = Depends(deps.get_db),
    chat_in: ChatRequest,
    current_user: User = Depends(deps.get_current_user),
    token: str = Depends(deps.oauth2_scheme),
):
    """
    Handle a chat message from the user.

    If conversation_id is provided, it continues the existing conversation.
    Otherwise, it starts a new one.
    """
    if chat_in.conversation_id:
        conversation = chat_service.get_conversation(db, user=current_user, conversation_id=chat_in.conversation_id)
    else:
        conversation = chat_service.create_conversation(db, user=current_user)

    # 1. Save user's message to the database
    chat_service.add_message(
        db, conversation=conversation, role="user", content=chat_in.message
    )

    # 2. Load the full conversation history
    history = chat_service.get_conversation_history(db, conversation_id=conversation.id)

    # 3. Get the AI's response
    ai_response_content = chat_service.get_ai_response(
        history=history, user=current_user, token=token
    )

    # 4. Save the AI's response to the database
    chat_service.add_message(
        db, conversation=conversation, role="assistant", content=ai_response_content
    )

    return ChatResponse(
        conversation_id=conversation.id,
        response=ai_response_content,
        tool_calls=[]  # Placeholder for now
    )
