# Phase 3: AI Chatbot Technical Implementation Plan

## 1. System Architecture

This diagram illustrates the flow of communication between the components of our AI-powered Todo application.

```
+----------------+      +-----------------+      +-----------------+      +----------------+      +-----------------+      +----------+
| Frontend       |----->| Backend         |----->| AI Agent        |----->| MCP Server     |----->| Backend         |----->| Database |
| (Next.js with  |      | (FastAPI /chat  |      | (OpenAI Agents  |      | (FastMCP)      |      | (FastAPI CRUD   |      | (Neon    |
|  ChatKit)      |      |  endpoint)      |      |  SDK)           |      |                |      |  endpoints)     |      |  PGSQL)  |
+----------------+      +-----------------+      +-----------------+      +----------------+      +-----------------+      +----------+
```

- **Frontend (ChatKit)**: The user interacts with the ChatKit UI, sending messages.
- **Backend (/chat endpoint)**: A new endpoint in our existing FastAPI backend receives the chat message and forwards it to the AI Agent.
- **AI Agent (OpenAI Agents SDK)**: This service receives the message, uses the OpenAI SDK to determine the user's intent, and decides which tool to call.
- **MCP Server (FastMCP)**: Exposes the backend's CRUD operations as tools for the AI Agent to consume via the Model Context Protocol (MCP).
- **Backend (CRUD endpoints)**: The original FastAPI endpoints from Phase 2 that perform the actual database operations.
- **Database (Neon PGSQL)**: The PostgreSQL database where the user's tasks are stored.

---

## 2. Data Flow Example: "Add task to buy groceries"

1.  **User Input**: The user types "Add task to buy groceries" into the ChatKit widget on the frontend and hits send.
2.  **Frontend → Backend**: The frontend makes a POST request to the `/api/chat` endpoint on the FastAPI backend, sending the user's message and the session token.
3.  **Backend → AI Agent**: The `/api/chat` endpoint forwards the message and token to the AI Agent service.
4.  **AI Agent → OpenAI**: The AI Agent, using the OpenAI Agents SDK, sends the conversation history and the available tools (from the MCP Server) to the GPT-4o-mini model.
5.  **OpenAI Response**: The model determines that the user wants to create a task and responds with a request to call the `create_task` tool with the argument `title="Buy groceries"`.
6.  **AI Agent → MCP Server**: The AI Agent calls the `create_task` tool on the MCP Server, passing the `session_token` and `title`.
7.  **MCP Server → Backend API**: The `create_task` tool implementation in the MCP server makes an authenticated POST request to the `/api/tasks/` endpoint of the Phase 2 backend.
8.  **Backend API → Database**: The backend's `/api/tasks/` endpoint creates the new task in the PostgreSQL database.
9.  **Database → Backend API**: The database confirms the creation and returns the new task object.
10. **Backend API → MCP Server**: The backend API returns the newly created task object to the MCP Server.
11. **MCP Server → AI Agent**: The MCP Server returns the result of the tool call (the new task object) to the AI Agent.
12. **AI Agent → OpenAI**: The AI Agent sends the tool's result back to the OpenAI model to get the final natural language response.
13. **OpenAI → AI Agent**: The model generates a friendly response, e.g., "Okay, I've added 'Buy groceries' to your list."
14. **AI Agent → Backend**: The AI Agent returns this final response to the `/api/chat` endpoint.
15. **Backend → Frontend**: The backend sends the response back to the frontend ChatKit widget.
16. **UI Update**: The ChatKit widget displays the AI's response. The frontend may also re-fetch the task list to show the new item in the main UI.

---

## 3. Component Details

### 3.1 MCP Server (`mcp-server/`)

- **Framework**: `FastMCP`
- **Runner**: `mcp_server.py`
- **Tools**: `mcp_server/tools.py`

**`mcp_server.py`:**
```python
from fastmcp import FastMCP
from mcp_server.tools import get_tasks, create_task, update_task, delete_task

app = FastMCP()

app.add_tool(get_tasks)
app.add_tool(create_task)
app.add_tool(update_task)
app.add_tool(delete_task)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

**`mcp_server/tools.py`:**
This file will define the four CRUD tools. They will use `httpx` to call the main backend API.

```python
import httpx
from mcp import tool

BACKEND_API_URL = "http://localhost:8000" # From .env

@tool
async def get_tasks(session_token: str) -> dict:
    """Retrieve all tasks for the authenticated user."""
    headers = {"Authorization": f"Bearer {session_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_API_URL}/api/tasks/", headers=headers)
        response.raise_for_status()
        return response.json()

# ... similar implementations for create_task, update_task, delete_task
```

### 3.2 AI Agent (`ai-agent/`)

- **Framework**: `openai` Agents SDK
- **Runner**: `agent_server.py`
- **Main Logic**: `ai_agent/main.py`

**`agent_server.py`:**
This will be a simple FastAPI server that exposes a single endpoint for the main backend to call.

```python
from fastapi import FastAPI
from ai_agent.main import get_chat_response
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_token: str
    # conversation_history: list # Managed by frontend

app = FastAPI()

@app.post("/chat")
async def chat_handler(request: ChatRequest):
    response = await get_chat_response(request.message, request.session_token)
    return {"reply": response}
```

**`ai_agent/main.py`:**
```python
import os
from openai import Assistant
from mcp_client import MCPClient

# System instructions for the assistant
ASSISTANT_INSTRUCTIONS = (
    "You are a friendly and efficient productivity assistant for a Todo app. "
    "Help users manage their tasks. Be concise and clear in your responses."
)

# Connect to the MCP server to get the tool definitions
mcp_client = MCPClient(base_url="http://localhost:8001") # From .env

assistant = Assistant(
    name="Todo App Assistant",
    instructions=ASSISTANT_INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=mcp_client.get_tools(),
)

async def get_chat_response(message: str, session_token: str) -> str:
    # The OpenAI SDK needs a thread to manage conversation state
    thread = assistant.create_thread()
    
    # Add the user's message to the thread
    thread.add_message(content=message, role="user")

    # The `run` method will automatically handle tool calls
    run = thread.run()

    # Pass the session_token to the tool calls when they are executed
    # Note: The exact mechanism for this may vary with SDK updates.
    # We might need to subclass the tool calling logic to inject the token.
    # For now, we assume a mechanism exists to pass context.
    
    # Wait for the run to complete
    await run.wait_for_completion()
    
    # Get the latest message from the assistant
    last_message = thread.get_last_message()
    return last_message.content
```

### 3.3 Backend Chat Endpoint (`backend/app/api/`)

- **File**: `backend/app/api/endpoints/chat.py`
- **Framework**: `FastAPI`

```python
from fastapi import APIRouter, Depends, HTTPException
from app.models import User
from app.api.deps import get_current_user
import httpx
from pydantic import BaseModel

router = APIRouter()
AI_AGENT_URL = "http://localhost:8002/chat" # From .env

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def handle_chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session_token: str = Depends(...) # How you get the raw token
):
    """Proxies chat messages to the AI Agent service."""
    payload = {
        "message": request.message,
        "session_token": session_token
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(AI_AGENT_URL, json=payload, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error from AI service.")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="AI service is unavailable.")

```

### 3.4 Frontend ChatWidget (`frontend/components/`)

- **File**: `frontend/components/ChatWidget.tsx`
- **Library**: `openai-chatkit` (or a similar React chat component library)

```tsx
'use client';

import { useState } from 'react';
import { Chat } from '@chat-ui/core'; // Example library
import { useSession } from 'next-auth/react'; // Assuming NextAuth for session

export default function ChatWidget() {
  const { data: session } = useSession();
  const [messages, setMessages] = useState([]);

  const handleSend = async (message) => {
    if (!session) return;

    const userMessage = { role: 'user', content: message.content };
    setMessages((prev) => [...prev, userMessage]);

    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.accessToken}`,
      },
      body: JSON.stringify({ message: message.content }),
    });

    if (response.ok) {
      const data = await response.json();
      const assistantMessage = { role: 'assistant', content: data.reply };
      setMessages((prev) => [...prev, assistantMessage]);
    } else {
      // Handle error
      const errorMessage = { role: 'assistant', content: 'Sorry, something went wrong.' };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  return (
    <div className="chat-widget-container">
      <Chat messages={messages} onSend={handleSend} />
    </div>
  );
}
```

---

## 4. Dependencies

### `mcp-server/pyproject.toml`
```toml
[project]
name = "mcp-server"
version = "0.1.0"
dependencies = [
    "fastmcp",
    "uvicorn",
    "httpx",
    "python-dotenv",
]
```

### `ai-agent/pyproject.toml`
```toml
[project]
name = "ai-agent"
version = "0.1.0"
dependencies = [
    "openai",
    "fastapi",
    "uvicorn",
    "mcp-client",
    "python-dotenv",
]
```

### `frontend/package.json` (Updates)
```json
{
  "dependencies": {
    ...
    "@chat-ui/core": "^1.0.0", // Or chosen chat library
    "@chat-ui/react": "^1.0.0"
  }
}
```

---

## 5. Environment Variables (`.env`)

A single `.env` file in the project root can be used, and each service can load the variables it needs.

```env
# Main Backend
DATABASE_URL="postgresql://..."

# MCP Server
BACKEND_API_URL="http://localhost:8000"

# AI Agent
OPENAI_API_KEY="sk-..."
MCP_SERVER_URL="http://localhost:8001"

# Backend Chat Endpoint
AI_AGENT_URL="http://localhost:8002/chat"
```

---

## 6. Development Workflow

1.  **Start Database**: Ensure the Neon PostgreSQL database is active.
2.  **Start Backend**: `cd backend && uvicorn app.main:app --reload --port 8000`
3.  **Start MCP Server**: `cd mcp-server && uvicorn mcp_server:app --reload --port 8001`
4.  **Start AI Agent**: `cd ai-agent && uvicorn agent_server:app --reload --port 8002`
5.  **Start Frontend**: `cd frontend && npm run dev`

A `docker-compose.yml` file would be ideal to manage these services.

---

## 7. Testing Strategy

-   **Unit Tests**:
    -   **MCP Server**: Test each tool function in `tools.py` by mocking `httpx` requests.
    -   **AI Agent**: Test the `get_chat_response` function by mocking the `openai` SDK and `MCPClient`.
    -   **Backend**: Test the `/api/chat` endpoint by mocking `httpx` calls to the AI agent.
    -   **Frontend**: Use Jest/RTL to test the `ChatWidget` component's state and rendering.
-   **Integration Tests**:
    -   Test the flow from **AI Agent → MCP Server → Backend API**.
    -   Test the flow from **Backend Chat Endpoint → AI Agent**.
-   **End-to-End (E2E) Tests**:
    -   Use a framework like Playwright or Cypress to simulate a user typing a command in the chat widget and verify that the UI updates correctly and the task appears in the database.

---

## 8. Error Handling

-   **Frontend**: The `ChatWidget` will have a `try...catch` block around the `fetch` call. On error, it will display a generic error message in the chat history.
-   **Backend (`/chat`)**: Uses `try...except` blocks to catch `httpx` errors (e.g., connection errors, non-2xx status codes) and returns appropriate HTTP status codes (e.g., 503 Service Unavailable, 502 Bad Gateway).
-   **AI Agent**: The agent will wrap OpenAI and MCP client calls in `try...except` blocks. If a tool call fails, it should be able to report this failure back to the model, which can then generate a user-facing error message (e.g., "I couldn't add your task right now.").
-   **MCP Server**: The `httpx` calls within tools will use `response.raise_for_status()` to catch API errors from the main backend. These errors will propagate back to the AI Agent.

---

## 9. Security Considerations

-   **Authentication**: The entire chat flow is protected by the `session_token`. The AI Agent and MCP Server must be in a trusted private network, as they receive the raw session token. They should not be exposed to the public internet.
-   **Input Sanitization**: The primary concern is prompt injection. The system instructions for the AI Agent should be carefully crafted to prevent it from executing unintended tool calls. The limited scope of the tools (only task management) reduces the risk.
-   **Secret Management**: The `OPENAI_API_KEY` and `DATABASE_URL` must be stored securely in environment variables and never be committed to version control.
-   **Data Transfer**: The `session_token` is passed between services. This is acceptable within a trusted backend environment (e.g., Docker network), but would be a major vulnerability if these services were communicating over the public internet without encryption.

---

## 10. Performance Optimization

-   **Async Operations**: All services (FastAPI, FastMCP, AI Agent) are built on an async framework (`asyncio`), which is crucial for handling concurrent I/O-bound operations (API calls) efficiently.
-   **Timeouts**: Set aggressive but realistic timeouts for all `httpx` client calls to prevent requests from hanging indefinitely.
-   **Model Choice**: `gpt-4o-mini` is chosen for its balance of speed and capability. If latency is critical, further optimizations might be needed.
-   **Caching**: The available tools from the MCP server can be cached by the AI Agent on startup, as they are unlikely to change during runtime.
-   **Database Queries**: Ensure the backend's CRUD operations use efficient database queries with proper indexing.
