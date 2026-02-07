from typing import List, Optional
import datetime
from sqlmodel import Session, select
from sqlalchemy import or_
from fastapi import HTTPException

from models.task import Task
from models.user import User

class TaskService:
    def get_user_tasks(self, db: Session, user: User, search: Optional[str] = None, completed: Optional[bool] = None) -> List[Task]:
        query = select(Task).where(Task.user_id == user.id)
        if search:
            query = query.where(or_(Task.title.ilike(f"%{search}%"), Task.description.ilike(f"%{search}%")))
        if completed is not None:
            query = query.where(Task.completed == completed)
        return db.exec(query).all()

    def get_task(self, db: Session, user: User, task_id: int) -> Task:
        task = db.get(Task, task_id)
        if not task or task.user_id != user.id:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def create_task(self, db: Session, user: User, task_data: dict) -> Task:
        task = Task(**task_data, user_id=user.id)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def update_task(self, db: Session, user: User, task_id: int, task_data: dict) -> Task:
        task = self.get_task(db, user, task_id)
        for key, value in task_data.items():
            setattr(task, key, value)
        task.updated_at = datetime.datetime.utcnow()
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def delete_task(self, db: Session, user: User, task_id: int):
        task = self.get_task(db, user, task_id)
        db.delete(task)
        db.commit()

task_service = TaskService()
