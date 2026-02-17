from fastapi import FastAPI, HTTPException, Depends
from DataAccess.database import get_db
from sqlalchemy.orm import Session
from Business.crud import create_user,create_task,show_all_tasks,update_task,delete_task
from Business.schemas import UserCreate,UserShow, TaskShow,TaskCreate,TaskUpdate
from DataAccess.database import Base, engine
from DataAccess import models

app = FastAPI()
# Base.metadata.create_all(bind=engine)


@app.post('/app/users/',response_model = UserShow)
def endpoint_create_user(user:UserCreate,db:Session=Depends(get_db) ):
    check = create_user(user, db)
    if check:
        return check
    raise HTTPException(status_code=409,detail='Already exists')

@app.post('/app/users/{user_id}/tasks', response_model=TaskShow)
def endpoint_create_task(user_id:int, task: TaskCreate, db:Session=Depends(get_db)):
    result = create_task(task, user_id,db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@app.get('/app/tasks/{user_id}', response_model=list[TaskShow])
def endpoint_show_all_tasks(user_id:int, db:Session=Depends(get_db)):
    result = show_all_tasks(user_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return result


@app.put('/app/tasks/{task_id}', response_model=TaskShow)
def endpoint_update_task(task_id:int,task_update:TaskUpdate,db:Session=Depends(get_db)):
    result = update_task(task_id,task_update, db)
    if result is None:
        raise HTTPException(status_code=404, detail="task not found")
    return result

@app.delete('/app/tasks/{task_id}',response_model=str)
def endpoint_delete_task(task_id:int, db:Session=Depends(get_db)):
    result = delete_task(task_id,db)
    if not result:
        raise HTTPException(status_code=404, detail="task not found")
    return "deletion was done successfully"