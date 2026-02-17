from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from DataAccess.database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, index=True, autoincrement=True, primary_key=True)
    name = Column(String, index=True, nullable=False)
    # family = Column(String,index=True)
    email = Column(String, index=True, unique=True, nullable=False) 

    tasks = relationship("Task", back_populates='owner' , cascade='all, delete-orphan')

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, index=True, autoincrement=True, primary_key=True)
    title = Column(String, index=True, nullable=False)
    completed = Column(Boolean,default=False,nullable=False)

    owner_id = Column(Integer, ForeignKey('users.id'),nullable=False)
    description = Column(String, index=True)
    owner = relationship("User", back_populates='tasks')
    priority = Column(Integer, default= 1,nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
