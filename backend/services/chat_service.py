from typing import List, Dict, Any
from sqlmodel import Session, select
from fastapi import HTTPException
import requests
import os

from models import User, Conversation, Message

# --- Configuration ---
AI_AGENT_URL = "http://localhost:8001/chat"

class ChatService:

    def get_conversation(self, db: Session, *, user: User, conversation_id: int) -> Conversation:
        conversation = db.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user.id:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation

    def create_conversation(self, db: Session, *, user: User) -> Conversation:
        conversation = Conversation(user_id=user.id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    def add_message(self, db: Session, *, conversation: Conversation, role: str, content: str) -> Message:
        message = Message(
            conversation_id=conversation.id,
            user_id=conversation.user_id,
            role=role,
            content=content
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        # Update conversation timestamp
        conversation.updated_at = message.created_at
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return message

    def get_conversation_history(self, db: Session, *, conversation_id: int) -> List[Dict[str, Any]]:
        messages = db.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        ).all()
        return [{"role": msg.role, "content": msg.content} for msg in messages]

    def get_ai_response(self, *, history: List[Dict[str, Any]], user: User, token: str) -> str:
        """
        Calls the external AI Agent server to get a response.
        """
        payload = {
            "messages": history,
            "user_id": user.id,
            "token": token,
        }
        
        try:
            response = requests.post(AI_AGENT_URL, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            agent_response = response.json()
            return agent_response.get("content", "No response from AI agent.")

        except requests.exceptions.RequestException as e:
            # This catches connection errors, timeouts, etc.
            print(f"Error calling AI Agent service: {e}")
            raise HTTPException(
                status_code=503, 
                detail=f"Could not connect to the AI agent. Please try again later."
            )
        except Exception as e:
            # This catches other errors, like JSON decoding errors
            print(f"An unexpected error occurred while communicating with the AI agent: {e}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")


chat_service = ChatService()