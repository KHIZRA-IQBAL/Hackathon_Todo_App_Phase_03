import os
import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

# Load environment variables
load_dotenv()

# --- Configuration ---
MOCK_MODE = True  # Set to False when you have OpenAI credits

# --- FastAPI App ---
ai_router = APIRouter(
    prefix="/ai",
    tags=["AI Agent"]
)

# --- Pydantic Models ---
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    user_id: int
    token: str

# --- API Endpoints ---
@ai_router.post("/chat")
async def chat(request: ChatRequest):
    """Handle chat request with mock AI responses"""
    
    if not MOCK_MODE:
        raise HTTPException(
            status_code=503,
            detail="OpenAI credits exhausted. Enable MOCK_MODE for demo."
        )
    
    try:
        # Get user's message
        user_message = request.messages[-1].content.lower()
        
        # Mock AI responses based on keywords
        if "add" in user_message and "task" in user_message:
            # Extract task title (simple approach)
            task_title = "your task"
            if "buy" in user_message:
                task_title = "Buy groceries"
            elif "call" in user_message:
                task_title = "Call someone"
            elif "study" in user_message:
                task_title = "Study for exam"
            
            response = f"✅ Great! I've added the task '{task_title}' to your list. You can see it on the left side now!"
            
        elif "show" in user_message or "list" in user_message or "my tasks" in user_message:
            response = "📋 I can see your tasks on the left side! You currently have:\n\n• Buy groceries (pending)\n\nYou can add more tasks by saying 'Add a task to...' or mark tasks as complete!"
            
        elif "complete" in user_message or "mark" in user_message or "done" in user_message or "finish" in user_message:
            response = "✅ Awesome! I've marked your task as complete. Great job staying productive! 🎉"
            
        elif "delete" in user_message or "remove" in user_message:
            response = "🗑️ I've removed that task from your list. All clean now!"
            
        elif "update" in user_message or "change" in user_message or "edit" in user_message:
            response = "✏️ I've updated the task with the new information!"
            
        elif "hello" in user_message or "hi" in user_message or "hey" in user_message:
            response = "👋 Hello! I'm your AI task assistant. I can help you:\n\n✨ Add tasks: 'Add a task to buy milk'\n📋 Show tasks: 'Show me my tasks'\n✅ Complete tasks: 'Mark the first task as done'\n🗑️ Delete tasks: 'Delete the grocery task'\n\nWhat would you like to do?"
            
        elif "help" in user_message:
            response = "🤖 I'm here to help you manage your tasks! Here's what I can do:\n\n• **Add tasks**: 'Add a task to call mom'\n• **View tasks**: 'Show all my tasks'\n• **Complete tasks**: 'Mark task as complete'\n• **Delete tasks**: 'Remove the meeting task'\n\nJust tell me what you need in natural language! 💬"
            
        else:
            response = "I'm your AI task assistant! 🤖\n\nI can help you:\n• Add new tasks\n• Show your task list\n• Mark tasks as complete\n• Delete tasks\n\nTry saying something like 'Add a task to buy groceries' or 'Show me my tasks'!"
        
        return {
            "role": "assistant",
            "content": response
        }
            
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
