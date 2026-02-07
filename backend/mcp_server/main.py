from typing import List, Optional
import requests
from fastmcp import FastMCP
from pydantic import BaseModel

# --- Pydantic Models for Task Schema ---
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# Initialize FastAPI app
app = FastMCP()
mcp = app

BACKEND_URL = "http://localhost:8000/api/v1"

# Helper to get auth headers
def _get_auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}

@app.tool()
def get_tasks(
    user_id: int,
    token: str,
    query: Optional[str] = None
) -> List[TaskResponse]:
    """
    Retrieves a list of tasks for a user. Can optionally filter by a search query.
    """
    params = {}
    if query:
        params["query"] = query
    
    response = requests.get(
        f"{BACKEND_URL}/users/{user_id}/tasks",
        headers=_get_auth_headers(token),
        params=params,
    )
    response.raise_for_status()
    return response.json()

@app.tool()
def create_task(
    user_id: int,
    token: str,
    title: str,
    description: Optional[str] = None
) -> TaskResponse:
    """
    Creates a new task for a user.
    """
    task_data = TaskCreate(title=title, description=description)
    response = requests.post(
        f"{BACKEND_URL}/users/{user_id}/tasks",
        headers=_get_auth_headers(token),
        json=task_data.model_dump(),
    )
    response.raise_for_status()
    return response.json()

@app.tool()
def update_task(
    user_id: int,
    token: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
) -> TaskResponse:
    """
    Updates an existing task for a user.
    """
    task_data = TaskUpdate(
        title=title, description=description, completed=completed
    ).model_dump(exclude_unset=True)

    if not task_data:
        raise ValueError("No fields to update.")

    response = requests.put(
        f"{BACKEND_URL}/users/{user_id}/tasks/{task_id}",
        headers=_get_auth_headers(token),
        json=task_data,
    )
    response.raise_for_status()
    return response.json()

@app.tool()
def delete_task(
    user_id: int,
    token: str,
    task_id: int
) -> dict:
    """
    Deletes a task by its ID for a user.
    """
    response = requests.delete(
        f"{BACKEND_URL}/users/{user_id}/tasks/{task_id}",
        headers=_get_auth_headers(token),
    )
    response.raise_for_status()
    return {"message": "Task deleted successfully"}

# The MCP server will automatically generate the /mcp endpoint
# with the tools defined above.

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)