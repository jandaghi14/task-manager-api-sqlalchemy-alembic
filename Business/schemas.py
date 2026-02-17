from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: str
    completed: Optional[bool] = False
    priority : int = 1
    @model_validator(mode='before')
    def description_required_if_priority_high(cls, v):
        if not isinstance(v, dict):
            return v
        priority = v.get('priority', 0)
        description = v.get('description')
        if priority > 5 and not description:
            raise ValueError('Description is required if priority > 5')
        return v

class TaskCreate(TaskBase):
    
    pass
            

class TaskUpdate(BaseModel):
    completed:Optional[bool]= None
    title: Optional[str]= None
    description: Optional[str]= None
    priority: Optional[int]= None
    
class TaskShow(TaskBase):
    id:int
    completed:bool
    priority: int
    created_at: datetime
    class Config:
        from_attributes = True
    
    
class UserBase(BaseModel):
    name:str
    # family:str
    email:str
    class Config:
        from_attributes = True
    
class UserCreate(UserBase):
    pass

class UserShow(UserBase):
    id : int
    class Config:
        from_attributes = True