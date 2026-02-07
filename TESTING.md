# Phase 3 Testing Guide

This document provides step-by-step instructions to test the full-stack Todo application with the integrated AI Agent. These commands are for **Windows PowerShell**.

## Prerequisites

Before you begin, ensure you have configured your environment variables correctly.

1.  **Set `OPENAI_API_KEY`**:
    Make sure your valid OpenAI API key is present in the following files:
    - `backend/.env`
    - `mcp-server/.env`
    - `ai-agent/.env`

    Example:
    ```
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

2.  **Verify `DATABASE_URL`**:
    The `backend/.env` file should have a configured `DATABASE_URL`. The default is a SQLite database, which requires no extra setup.
    ```
    DATABASE_URL=sqlite:///./test.db
    ```

## Step 1: Database Migration

The database tables for `users`, `tasks`, `conversations`, and `messages` are created automatically when the backend server starts for the first time. No manual migration command is needed.

## Step 2: Start Services

You will need to open **four separate PowerShell terminals** to run each service simultaneously.

---

### Terminal 1: Backend Server (Port 8000)

```powershell
# Navigate to the backend directory
cd backend

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Install/update dependencies
pip install -r requirements.txt

# Start the FastAPI server on port 8000
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

### Terminal 2: MCP Server (Port 8001)

```powershell
# Navigate to the mcp-server directory
cd mcp-server

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Install/update dependencies
pip install -r requirements.txt

# Start the MCP server on port 8001
uvicorn main:app --host 0.0.0.0 --port 8001
```

---

### Terminal 3: Frontend Server (Port 3000)

```powershell
# Navigate to the frontend directory
cd frontend

# Install dependencies (only needs to be done once)
npm install

# Start the Next.js development server on port 3000
npm run dev
```

---

### Terminal 4: AI Agent (Console)

```powershell
# Navigate to the ai-agent directory
cd ai-agent

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Install/update dependencies
pip install -r requirements.txt

# Set the session token (replace with the token from Step 3.2)
# This is required for the AI Agent to have the identity of the logged-in user
$env:SESSION_TOKEN="your_jwt_token_here"

# Run the agent
python agent.py
```

## Step 3: Test Scenarios

### 1. User Signup

Create a new user.

```powershell
curl -X POST "http://localhost:8000/api/v1/auth/register" `
-H "Content-Type: application/json" `
-d '{"email": "test@example.com", "password": "password123"}'
```

You should receive an access token in the response.

### 2. User Login

Log in to get a new access token (JWT).

```powershell
# Execute the curl command and save the result to a variable
$response = curl -X POST "http://localhost:8000/api/v1/auth/login" `
-H "Content-Type: application/x-www-form-urlencoded" `
-d "username=test@example.com&password=password123" | ConvertFrom-Json

# Extract and store the access token in a variable
$token = $response.access_token

# Print the token to verify
Write-Output "Your JWT Token: $token"

# IMPORTANT: Use this token for the AI Agent (Step 2, Terminal 4) and for the Chat Endpoint test.
```

### 3. Chat Endpoint

Use the token from the login step to send a message to the new chat endpoint.

```powershell
# Make sure you have the $token variable from the previous step
curl -X POST "http://localhost:8000/api/v1/chat" `
-H "Content-Type: application/json" `
-H "Authorization: Bearer $token" `
-d '{"message": "Hello, can you help me?"}'
```
The system will create a new conversation and return the AI's response.

### 4. AI Agent and MCP Tools

In the AI Agent terminal (Terminal 4), interact with the agent. Make sure you have set the `$env:SESSION_TOKEN` before running `python agent.py`.

**Example Interactions:**
- `You: list my tasks`
- `You: create a new task to buy groceries`
- `You: what have I done so far?`

The agent should use the MCP tools to perform these actions, and you should see the tool calls in the console output.

## Troubleshooting

- **`Port already in use`**: Another process is using port 8000, 8001, or 3000. Stop the other process or change the port in the `uvicorn` or `npm` command.
- **`ModuleNotFoundError`**: You forgot to install the dependencies. Run `pip install -r requirements.txt` in the respective virtual environment.
- **`500 Internal Server Error` on chat or agent**: This most likely means the `OPENAI_API_KEY` is invalid or not set correctly in the `.env` file for the service that's failing (backend or ai-agent).
- **`Connection refused` from AI Agent to MCP**: The MCP server (Terminal 2) is not running or is on a different port.
- **`401 Unauthorized`**: Your JWT token is invalid, expired, or not provided in the `Authorization` header correctly. Make sure you are using the full token from the login step.
