# Phase 3: AI Chatbot Task Breakdown

This document breaks down the implementation of the AI Chatbot into atomic, actionable tasks, organized by phase.

---

## Phase 1: Foundation Setup (4 tasks)

### **Task T3.1.1**
- **Description**: Copy the `backend` and `frontend` directories from the completed Phase 2 project into the `phase3-ai-chatbot` root directory.
- **Input**: Completed Phase 2 project files.
- **Output**: `backend` and `frontend` directories present in the project root.
- **Dependencies**: None.
- **Acceptance Criteria**: Both directories and all their contents are successfully copied.
- **Complexity**: Simple

### **Task T3.1.2**
- **Description**: Create the initial Python project structures for the `mcp-server` and `ai-agent` services.
- **Input**: Directories created in the initial setup.
- **Output**: `mcp-server/pyproject.toml`, `mcp-server/main.py`, `ai-agent/pyproject.toml`, `ai-agent/main.py`.
- **Dependencies**: T3.1.1.
- **Acceptance Criteria**: All specified files are created and the `pyproject.toml` files are populated with basic project info.
- **Complexity**: Simple

### **Task T3.1.3**
- **Description**: Create a `.env.example` file in the root directory listing all required environment variables.
- **Input**: `plan.md` document.
- **Output**: A `.env.example` file.
- **Dependencies**: None.
- **Acceptance Criteria**: The file contains keys for `DATABASE_URL`, `OPENAI_API_KEY`, `BACKEND_API_URL`, `MCP_SERVER_URL`, and `AI_AGENT_URL`.
- **Complexity**: Simple

### **Task T3.1.4**
- **Description**: Populate the `pyproject.toml` and `package.json` files with all required dependencies.
- **Input**: `plan.md` dependency list.
- **Output**: Updated `mcp-server/pyproject.toml`, `ai-agent/pyproject.toml`, and `frontend/package.json`.
- **Dependencies**: T3.1.2.
- **Acceptance Criteria**: `uv install` and `npm install` run without errors in their respective directories.
- **Complexity**: Medium

---

## Phase 2: MCP Server Implementation (7 tasks)

### **Task T3.2.1**
- **Description**: Create the `mcp-server/main.py` file and initialize a `FastMCP` application.
- **Input**: An empty `main.py` file.
- **Output**: A runnable `FastMCP` server file that starts with `uvicorn`.
- **Dependencies**: T3.1.4.
- **Acceptance Criteria**: The server starts without errors on `localhost:8001`.
- **Complexity**: Simple

### **Task T3.2.2**
- **Description**: Implement the `get_tasks` tool in `mcp-server/tools.py`.
- **Input**: Session token.
- **Output**: A function that calls the backend's `/api/tasks/` GET endpoint and returns a list of tasks.
- **Dependencies**: Phase 2 backend running.
- **Acceptance Criteria**: The tool correctly retrieves tasks for a valid session token.
- **Complexity**: Medium

### **Task T3.2.3**
- **Description**: Implement the `create_task` tool.
- **Input**: Session token, title, optional description.
- **Output**: A function that calls the backend's `/api/tasks/` POST endpoint and returns the created task.
- **Dependencies**: Phase 2 backend running.
- **Acceptance Criteria**: The tool correctly creates a new task.
- **Complexity**: Medium

### **Task T3.2.4**
- **Description**: Implement the `update_task` tool.
- **Input**: Session token, task ID, and optional fields to update.
- **Output**: A function that calls the backend's `/api/tasks/{task_id}` PUT endpoint.
- **Dependencies**: Phase 2 backend running.
- **Acceptance Criteria**: The tool correctly updates an existing task.
- **Complexity**: Medium

### **Task T3.2.5**
- **Description**: Implement the `delete_task` tool.
- **Input**: Session token, task ID.
- **Output**: A function that calls the backend's `/api/tasks/{task_id}` DELETE endpoint.
- **Dependencies**: Phase 2 backend running.
- **Acceptance Criteria**: The tool correctly deletes an existing task.
- **Complexity**: Medium

### **Task T3.2.6**
- **Description**: Add error handling to all tools in `mcp-server/tools.py`.
- **Input**: Implemented tools.
- **Output**: Tools that use `try...except` blocks and `response.raise_for_status()` to handle API errors gracefully.
- **Dependencies**: T3.2.2, T3.2.3, T3.2.4, T3.2.5.
- **Acceptance Criteria**: Invalid requests (e.g., bad token, non-existent task ID) return appropriate error messages instead of crashing the server.
- **Complexity**: Medium

### **Task T3.2.7**
- **Description**: Create a test file (`mcp-server/test_tools.py`) to unit test the MCP tools.
- **Input**: Implemented tools.
- **Output**: A `pytest` file that mocks `httpx` and tests the logic of each tool.
- **Dependencies**: T3.2.6.
- **Acceptance Criteria**: All unit tests pass.
- **Complexity**: Complex

---

## Phase 3: AI Agent Implementation (6 tasks)

### **Task T3.3.1**
- **Description**: Create the `ai-agent/main.py` file to hold the core agent logic and `ai-agent/agent_server.py` for the FastAPI wrapper.
- **Input**: Empty files.
- **Output**: Skeleton files for the agent and its server.
- **Dependencies**: T3.1.4.
- **Acceptance Criteria**: `agent_server.py` can be run with `uvicorn` and shows a basic "hello world" response.
- **Complexity**: Simple

### **Task T3.3.2**
- **Description**: Configure the `OpenAI` Assistant in `ai-agent/main.py`.
- **Input**: `OPENAI_API_KEY`.
- **Output**: An initialized `openai.Assistant` instance.
- **Dependencies**: T3.3.1.
- **Acceptance Criteria**: The assistant object is created without errors.
- **Complexity**: Simple

### **Task T3.3.3**
- **Description**: Connect the `MCPClient` to the MCP server to fetch available tools.
- **Input**: `MCP_SERVER_URL`.
- **Output**: The `openai.Assistant` is configured with tools from the MCP server.
- **Dependencies**: T3.2.1 (MCP Server running).
- **Acceptance Criteria**: The AI agent starts and successfully registers the tools from the running MCP server.
- **Complexity**: Medium

### **Task T3.3.4**
- **Description**: Define the system instructions for the assistant.
- **Input**: `plan.md` specifications.
- **Output**: A detailed, security-conscious system prompt string in `ai-agent/main.py`.
- **Dependencies**: T3.3.2.
- **Acceptance Criteria**: The system prompt is assigned to the assistant's `instructions` parameter.
- **Complexity**: Simple

### **Task T3.3.5**
- **Description**: Implement the `get_chat_response` function to handle a conversation turn.
- **Input**: User message, session token.
- **Output**: A function that manages the `Thread` and `Run` lifecycle and returns the assistant's response.
- **Dependencies**: T3.3.3, T3.3.4.
- **Acceptance Criteria**: The function can take a message, process it (including potential tool calls), and return a string response.
- **Complexity**: Complex

### **Task T3.3.6**
- **Description**: Create a simple test CLI (`ai-agent/test_cli.py`) to interact with the agent directly.
- **Input**: The implemented `get_chat_response` function.
- **Output**: A command-line script that allows sending messages to the agent for quick testing.
- **Dependencies**: T3.3.5.
- **Acceptance Criteria**: Can have a basic conversation with the agent and see it call tools (via log output).
- **Complexity**: Medium

---

## Phase 4: Backend Integration (5 tasks)

### **Task T3.4.1**
- **Description**: Create the file `backend/app/api/endpoints/chat.py`.
- **Input**: Phase 2 backend structure.
- **Output**: A new chat router file.
- **Dependencies**: T3.1.1.
- **Acceptance Criteria**: The file is created in the correct directory.
- **Complexity**: Simple

### **Task T3.4.2**
- **Description**: Define the `ChatRequest` and `ChatResponse` Pydantic models in the chat router file.
- **Input**: `plan.md` specifications.
- **Output**: Pydantic models for the chat endpoint.
- **Dependencies**: T3.4.1.
- **Acceptance Criteria**: Models are defined correctly.
- **Complexity**: Simple

### **Task T3.4.3**
- **Description**: Implement the `POST /api/chat` endpoint.
- **Input**: `ChatRequest`, session token.
- **Output**: An endpoint that proxies the request to the AI Agent service and returns its response.
- **Dependencies**: T3.3.1 (AI Agent running), T3.4.2.
- **Acceptance Criteria**: The endpoint correctly forwards requests and responses between the client and the agent.
- **Complexity**: Medium

### **Task T3.4.4**
- **Description**: Add the new chat router to the main FastAPI app in `backend/app/main.py`.
- **Input**: Existing main FastAPI app.
- **Output**: The `/api/chat` endpoint is registered and available.
- **Dependencies**: T3.4.3.
- **Acceptance Criteria**: The application includes the chat router under the correct prefix.
- **Complexity**: Simple

### **Task T3.4.5**
- **Description**: Test the `/api/chat` endpoint using `curl` or a similar HTTP client.
- **Input**: A running backend and a valid session token.
- **Output**: A successful JSON response from the AI Agent.
- **Dependencies**: T3.4.4.
- **Acceptance Criteria**: A `curl` POST request to `/api/chat` returns a 200 OK with a valid response body.
- **Complexity**: Simple

---

## Phase 5: Frontend Integration (6 tasks)

### **Task T3.5.1**
- **Description**: Install the chosen chat UI library dependencies.
- **Input**: `frontend/package.json`.
- **Output**: `node_modules` updated with chat UI packages.
- **Dependencies**: T3.1.4.
- **Acceptance Criteria**: `npm install` completes successfully.
- **Complexity**: Simple

### **Task T3.5.2**
- **Description**: Create the `frontend/components/ChatWidget.tsx` component.
- **Input**: `plan.md` specifications.
- **Output**: A React component that renders the chat interface.
- **Dependencies**: T3.5.1.
- **Acceptance Criteria**: The component renders a basic, non-functional chat box.
- **Complexity**: Medium

### **Task T3.5.3**
- **Description**: Create the Next.js API route `frontend/app/api/chat/route.ts` to act as a proxy.
- **Input**: Chat message from the widget.
- **Output**: A route that forwards the chat request to the main backend's `/api/chat` endpoint.
- **Dependencies**: T3.4.5 (Backend chat endpoint working).
- **Acceptance Criteria**: The API route successfully proxies requests and includes the auth token.
- **Complexity**: Medium

### **Task T3.5.4**
- **Description**: Add the `ChatWidget` component to the main dashboard page.
- **Input**: `frontend/app/dashboard/page.tsx`.
- **Output**: The chat widget is visible on the dashboard.
- **Dependencies**: T3.5.2.
- **Acceptance Criteria**: The chat widget appears in a fixed position (e.g., bottom right) on the dashboard.
- **Complexity**: Simple

### **Task T3.5.5**
- **Description**: Implement the `onSend` handler and session token management in `ChatWidget.tsx`.
- **Input**: The `ChatWidget` component and NextAuth session.
- **Output**: A functional chat widget that sends messages to the backend and displays responses.
- **Dependencies**: T3.5.3.
- **Acceptance Criteria**: Typing a message and hitting send results in the assistant's response appearing in the chat history.
- **Complexity**: Complex

### **Task T3.5.6**
- **Description**: Test the full end-to-end chat UI flow.
- **Input**: A fully running application stack.
- **Output**: Confirmation of successful interaction.
- **Dependencies**: T3.5.5.
- **Acceptance Criteria**: A user can type "add a task", see the response, and see the task list UI update accordingly.
- **Complexity**: Medium

---

## Phase 6: Testing & Documentation (6 tasks)

### **Task T3.6.1**
- **Description**: Finalize and run all unit tests for the MCP tools.
- **Input**: `mcp-server/test_tools.py`.
- **Output**: Passing test suite.
- **Dependencies**: T3.2.7.
- **Acceptance Criteria**: `pytest` runs with 100% pass rate for the MCP server tests.
- **Complexity**: Medium

### **Task T3.6.2**
- **Description**: Write and run conversation tests for the AI agent.
- **Input**: `ai-agent/test_cli.py` or a new test file.
- **Output**: Scripts that test various conversational flows (e.g., create, list, update, delete tasks via language).
- **Dependencies**: T3.3.6.
- **Acceptance Criteria**: The agent correctly interprets commands and uses the right tools in all test cases.
- **Complexity**: Complex

### **Task T3.6.3**
- **Description**: Perform manual end-to-end testing of the entire application.
- **Input**: The full running application.
- **Output**: A list of bugs or confirmation of stability.
- **Dependencies**: T3.5.6.
- **Acceptance Criteria**: The application is stable and key user journeys are working as expected.
- **Complexity**: Complex

### **Task T3.6.4**
- **Description**: Update the root `README.md` with detailed setup and run instructions.
- **Input**: The existing `README.md`.
- **Output**: A comprehensive `README.md` that allows a new developer to set up and run the project.
- **Dependencies**: All previous implementation tasks.
- **Acceptance Criteria**: A team member can follow the README and successfully start all services.
- **Complexity**: Medium

### **Task T3.6.5**
- **Description**: Create a demo script outlining a compelling user journey.
- **Input**: The finished application.
- **Output**: A script that showcases the AI chatbot's capabilities.
- **Dependencies**: T3.6.3.
- **Acceptance Criteria**: The script covers listing, adding, updating, and deleting tasks using natural language.
- **Complexity**: Simple

### **Task T3.6.6**
- **Description**: Record a high-quality demo video of the application.
- **Input**: The demo script and a running application.
- **Output**: An `.mp4` video file.
- **Dependencies**: T3.6.5.
- **Acceptance Criteria**: The video clearly and concisely demonstrates the project's functionality.
- **Complexity**: Medium
