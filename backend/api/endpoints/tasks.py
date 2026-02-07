# from fastapi import APIRouter, Depends, HTTPException
# from sqlmodel import Session
# from typing import List
# import uuid

# from api import deps
# from models import User
# from services.task_service import task_service
# from schemas.task import TaskCreate, TaskUpdate, TaskResponse

# router = APIRouter()

# @router.get("/{user_id}/tasks", response_model=List[TaskResponse])
# def read_tasks(
#     user_id: int,
#     search: Optional[str] = None,
#     completed: Optional[bool] = None,
#     db: Session = Depends(deps.get_db),
#     current_user: User = Depends(deps.get_current_user),
# ):
#     """
#     Retrieve all tasks for a specific user, with optional search and filter.
#     """
#     if current_user.id != user_id:
#         raise HTTPException(status_code=403, detail="Not authorized to access these tasks")
#     return task_service.get_user_tasks(db, user=current_user, search=search, completed=completed)

# @router.post("/{user_id}/tasks", response_model=TaskResponse)
# def create_task(
#     user_id: int,
#     *,
#     db: Session = Depends(deps.get_db),
#     task_in: TaskCreate,
#     current_user: User = Depends(deps.get_current_user),
# ):
#     """
#     Create new task.
#     """
#     if current_user.id != user_id:
#         raise HTTPException(status_code=403, detail="Not authorized to create tasks for this user")
#     return task_service.create_task(db=db, user=current_user, task_data=task_in.model_dump())

# @router.get("/{user_id}/tasks/{id}", response_model=TaskResponse)
# def read_task(
#     user_id: int,
#     id: int,
#     db: Session = Depends(deps.get_db),
#     current_user: User = Depends(deps.get_current_user),
# ):
#     """
#     Get task by ID.
#     """
#     if current_user.id != user_id:
#         raise HTTPException(status_code=403, detail="Not authorized to access this task")
#     return task_service.get_task(db, user=current_user, task_id=id)

# @router.put("/{user_id}/tasks/{id}", response_model=TaskResponse)
# def update_task(
#     user_id: int,
#     id: int,
#     *,
#     db: Session = Depends(deps.get_db),
#     task_in: TaskUpdate,
#     current_user: User = Depends(deps.get_current_user),
# ):
#     """
#     Update a task.
#     """
#     if current_user.id != user_id:
#         raise HTTPException(status_code=403, detail="Not authorized to update this task")
#     return task_service.update_task(db=db, user=current_user, task_id=id, task_data=task_in.model_dump(exclude_unset=True))

# @router.delete("/{user_id}/tasks/{id}")
# def delete_task(
#     user_id: int,
#     id: int,
#     *,
#     db: Session = Depends(deps.get_db),
#     current_user: User = Depends(deps.get_current_user),
# ):
#     """
#     Delete a task.
#     """
#     if current_user.id != user_id:
#         raise HTTPException(status_code=403, detail="Not authorized to delete this task")
#     task_service.delete_task(db=db, user=current_user, task_id=id)
#     return {"ok": True}

# @router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskResponse)
# def toggle_task_completion(
#     user_id: int,
#     id: int,
#     db: Session = Depends(deps.get_db),
#     current_user: User = Depends(deps.get_current_user),
# ):
#     """
#     Toggle a task's completion status.
#     """
#     if current_user.id != user_id:
#         raise HTTPException(status_code=403, detail="Not authorized to modify this task")
#     task = task_service.get_task(db, user=current_user, task_id=id)
#     task_update = {"completed": not task.completed}
#     return task_service.update_task(db=db, user=current_user, task_id=id, task_data=task_update)



from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List, Optional  # ← Optional add kiya
import uuid

from api import deps
from models import User
from services.task_service import task_service
from schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()

@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
def read_tasks(
    user_id: int,
    search: Optional[str] = None,
    completed: Optional[bool] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Retrieve all tasks for a specific user, with optional search and filter.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access these tasks")
    return task_service.get_user_tasks(db, user=current_user, search=search, completed=completed)

@router.post("/{user_id}/tasks", response_model=TaskResponse)
def create_task(
    user_id: int,
    *,
    db: Session = Depends(deps.get_db),
    task_in: TaskCreate,
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create new task.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create tasks for this user")
    return task_service.create_task(db=db, user=current_user, task_data=task_in.model_dump())

@router.get("/{user_id}/tasks/{id}", response_model=TaskResponse)
def read_task(
    user_id: int,
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get task by ID.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return task_service.get_task(db, user=current_user, task_id=id)

@router.put("/{user_id}/tasks/{id}", response_model=TaskResponse)
def update_task(
    user_id: int,
    id: int,
    *,
    db: Session = Depends(deps.get_db),
    task_in: TaskUpdate,
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update a task.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    return task_service.update_task(db=db, user=current_user, task_id=id, task_data=task_in.model_dump(exclude_unset=True))

@router.delete("/{user_id}/tasks/{id}")
def delete_task(
    user_id: int,
    id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Delete a task.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    task_service.delete_task(db=db, user=current_user, task_id=id)
    return {"ok": True}

@router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    user_id: int,
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Toggle a task's completion status.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this task")
    task = task_service.get_task(db, user=current_user, task_id=id)
    task_update = {"completed": not task.completed}
    return task_service.update_task(db=db, user=current_user, task_id=id, task_data=task_update)