# Task Manager API

A REST API for managing users and tasks, built with FastAPI, SQLAlchemy, SQLite, and Alembic database migrations.

## Features

- Create and manage users
- Full task CRUD (Create, Read, Update, Delete)
- One-to-many relationship (User → Tasks)
- Database migrations with Alembic
- Input validation with Pydantic
- Cascade deletes

## Tech Stack

- FastAPI
- SQLAlchemy ORM
- SQLite
- Alembic
- Pydantic

## Project Structure
```
├── main.py
├── DataAccess/
│   ├── database.py
│   └── models.py
├── Business/
│   ├── crud.py
│   └── schemas.py
├── alembic/
│   └── versions/
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Apply database migrations:
```bash
   alembic upgrade head
```
4. Run the server:
```bash
   uvicorn main:app --reload
```
5. Open docs at `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/app/users/` | Create a new user |
| POST | `/app/users/{user_id}/tasks` | Create a task for a user |
| GET | `/app/tasks/{user_id}` | Get all tasks for a user |
| PUT | `/app/tasks/{task_id}` | Update a task |
| DELETE | `/app/tasks/{task_id}` | Delete a task |