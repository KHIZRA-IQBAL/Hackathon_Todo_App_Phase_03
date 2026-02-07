# Phase 3: AI-Powered Todo Chatbot Specification

## 1. Overview
Transform the existing Todo web application (Phase 2) into an AI-native application by adding a conversational chatbot interface that allows users to manage tasks using natural language.

## 2. Architecture

The Phase 3 architecture extends Phase 2 with these new components:

- **/backend** (Copied from Phase 2): FastAPI application with SQLModel, Better Auth, and Neon PostgreSQL database
- **/frontend** (Copied from Phase 2): Next.js 15 application with Better Auth
- **/mcp-server** (New): MCP server that exposes backend CRUD operations as tools using FastMCP
- **/ai-agent** (New): OpenAI Agents SDK service that orchestrates conversations and calls MCP tools

## 3. Technology Stack

- **AI Engine**: OpenAI Agents SDK (Python)
- **Tool Protocol**: Model Context Protocol (MCP) - Official Python SDK
- **MCP Framework**: FastMCP
- **Backend**: FastAPI, SQLModel, Neon Serverless PostgreSQL
- **Frontend**: Next.js 15, React, TypeScript, OpenAI ChatKit
- **Authentication**: Better Auth with JWT
- **Package Manager**: UV (Python), npm (Node.js)
- **AI Model**: GPT-4o-mini

## 4. Functional Requirements

### 4.1 MCP Server
The MCP server exposes these tools for the AI agent:

**get_tasks**
- Parameters: session_token (string)
- Returns: List of task objects
- Description: Retrieve all tasks for authenticated user

**create_task**
- Parameters: session_token (string), title (string), description (optional string)
- Returns: Created task object
- Description: Create a new todo item

**update_task**
- Parameters: session_token (string), task_id (integer), title (optional), status (optional), description (optional)
- Returns: Updated task object
- Description: Update existing task details or toggle completion

**delete_task**
- Parameters: session_token (string), task_id (integer)
- Returns: Deletion confirmation
- Description: Remove a task from the list

### 4.2 AI Agent
- Natural language understanding for task management commands
- Tool orchestration via MCP server connection
- Stateless conversation handling (context managed by frontend)
- Friendly productivity assistant persona
- Error handling and graceful degradation

### 4.3 Frontend Chat Interface
- OpenAI ChatKit component integration
- Chat widget on dashboard page
- Session token management from Better Auth
- Real-time message display
- Loading states and error handling

## 5. Implementation Roadmap

**Phase 1: Foundation Setup**
1. Copy backend and frontend from Phase 2
2. Initialize mcp-server directory structure
3. Initialize ai-agent directory structure
4. Set up environment variables

**Phase 2: MCP Server Development**
1. Implement FastMCP server
2. Create all four CRUD tools
3. Add authentication and error handling
4. Test tools independently

**Phase 3: AI Agent Development**
1. Set up OpenAI Agents SDK
2. Configure MCP server connection
3. Define system instructions
4. Implement chat function
5. Test agent with sample conversations

**Phase 4: Backend Integration**
1. Create /api/chat endpoint in backend
2. Connect endpoint to AI agent
3. Add request/response schemas
4. Test API endpoint

**Phase 5: Frontend Integration**
1. Install ChatKit dependencies
2. Create ChatWidget component
3. Integrate with dashboard
4. Test end-to-end chat flow

**Phase 6: Testing & Documentation**
1. Write unit tests
2. Perform integration testing
3. Update documentation
4. Create demo video
