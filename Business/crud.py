from Business.schemas import TaskCreate,TaskUpdate,TaskShow,UserBase,UserCreate,TaskUpdate
from sqlalchemy.orm import Session
from DataAccess.models import Task,User
from datetime import datetime

def create_user(user:UserCreate, db:Session):
    check= db.query(User).filter(User.email == user.email).first()
    
    if check:
        return None
    
    user_db = User(name=user.name,email= user.email)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db
    
def create_task(task:TaskCreate, user_id:int,db:Session):
    user= db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    
    created_at= datetime.now()
    task_db= Task(
        title = task.title,
        owner = user,
        description  = task.description,
        completed = task.completed,
        priority = task.priority,
        created_at = created_at
        )

    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db

def show_all_tasks(user_id:int, db:Session):
    user= db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    result = db.query(Task).filter(Task.owner_id == user_id).all()
    return result

def update_task(task_id:int,task_update:TaskUpdate ,db:Session):
    task_db = db.query(Task).filter(Task.id == task_id).first()
    if not task_db:
        return None
    if task_update.title is not None:
        task_db.title = task_update.title
    if task_update.description is not None:
        task_db.description = task_update.description
    if task_update.completed is not None:
        task_db.completed = task_update.completed
    if task_update.priority is not None:
        task_db.priority = task_update.priority

    db.commit()
    db.refresh(task_db)
    return task_db
    
def delete_task(task_id:int,db:Session):
    task_db = db.query(Task).filter(Task.id == task_id).first()
    if not task_db:
        return None
    db.delete(task_db)
    db.commit()
    return task_db

    