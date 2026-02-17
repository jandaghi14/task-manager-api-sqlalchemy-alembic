from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from DataAccess.database import get_db, Base
import pytest
import os


TEST_DB_FILE = "test_tasks.db"
TEST_DATABASE_URL = f"sqlite:///./{TEST_DB_FILE}"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=test_engine,autoflush=False, autocommit= False)
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def setup_test_db():
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
        
        
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db

    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()

    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
    
@pytest.fixture
def client(setup_test_db):
    return TestClient(app)

    
        
# =========================================
# =========================================
def test_create_new_user(client):
    response = client.post('/app/users/',json={
        'name': 'Ali',
        'email': 'ali@email.com'
    })
    assert response.status_code == 200
    assert response.json()['name'] == 'Ali'
    assert response.json()['email'] == 'ali@email.com'
    assert response.json()['id'] == 1
# =========================================
def test_create_duplicate_user(client):
    response = client.post('/app/users/',json={
        'name': 'Ali',
        'email': 'ali@email.com'
    })
    response = client.post('/app/users/',json={
        'name': 'Ali',
        'email': 'ali@email.com'
    })
    assert response.status_code == 409
    assert response.json()['detail'] == 'Already exists'
    
# =========================================

def test_create_task(client):
    response = client.post('/app/users/',json={
        'name': 'Ali',
        'email': 'ali@email.com'
    })
    assert response.json()['name'] == 'Ali'
    assert response.json()['id'] == 1
    
    
    response = client.post('/app/users/1/tasks', json={
        'title' : 'testtitle',
        'completed' : False,
        'owner_id' : 1,
        'description' : 'testdesc',
        'priority' : 3,
    })
    assert response.status_code == 200
    assert response.json()['completed'] == False
    assert response.json()['description'] == 'testdesc'
    assert response.json()['priority'] == 3
# =========================================

def test_create_task_user_not_found(client):
    response = client.post('/app/users/1/tasks', json={
        'title' : 'testtitle',
        'completed' : False,
        'owner_id' : 1,
        'description' : 'testdesc',
        'priority' : 3,
    })
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'

# =========================================
def test_show_all_task(client):
    client.post('/app/users/',json={
        'name': 'Ali',
        'email': 'ali@email.com'
    })
       
    client.post('/app/users/1/tasks', json={
        'title' : 'testtitle1',
        'completed' : False,
        'owner_id' : 1,
        'description' : 'testdesc1',
        'priority' : 3,
    })
    client.post('/app/users/1/tasks', json={
        'title' : 'testtitle2',
        'completed' : False,
        'owner_id' : 1,
        'description' : 'testdesc2',
        'priority' : 3,
    })
    response = client.get('/app/tasks/1')
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['description'] == 'testdesc1'
    assert response.json()[0]['title'] == 'testtitle1'
    assert response.json()[1]['description'] == 'testdesc2'
    assert response.json()[1]['title'] == 'testtitle2'
# =========================================
def test_show_all_task_user_not_found(client):
    
    client.post('/app/users/1/tasks', json={
        'title' : 'testtitle2',
        'completed' : False,
        'owner_id' : 1,
        'description' : 'testdesc2',
        'priority' : 3,
    })
    response = client.get('/app/tasks/1')
    
    assert response.status_code == 404
    assert response.json()['detail'] == 'Tasks not found'
# =========================================
def test_update_task(client):
    client.post('/app/users/',json={
        'name': 'Ali',
        'email': 'ali@email.com'
    })
       
    client.post('/app/users/1/tasks', json={
        'title' : 'testtitle1',
        'completed' : False,
        'owner_id' : 1,
        'description' : 'testdesc1',
        'priority' : 3,
    })
    response = client.put('/app/tasks/1',json={
        'title' : 'updatetest',
        'completed' : False,
        'priority' : 4,
        'description' : 'updatedesc'
    })
    assert response.status_code == 200
    assert response.json()['completed'] == False
    assert response.json()['description'] == 'updatedesc'
    assert response.json()['priority'] == 4
    assert response.json()['title'] == 'updatetest'
# =========================================
def test_delete(client):
    client.post('/app/users/',json={
        'name': 'Ali',
        'email': 'ali@email.com'
    })
       
    client.post('/app/users/1/tasks', json={
        'title' : 'testtitle1',
        'completed' : False,
        'owner_id' : 1,
        'description' : 'testdesc1',
        'priority' : 3,
    })
    response = client.delete('/app/tasks/1')
    assert response.status_code == 200
    assert response.json() == 'deletion was done successfully'
# =========================================
def test_delete_user_not_found(client):
          
    client.post('/app/users/1/tasks', json={
        'title' : 'testtitle1',
        'completed' : False,
        'owner_id' : 1,
        'description' : 'testdesc1',
        'priority' : 3,
    })
    response = client.delete('/app/tasks/1')
    assert response.status_code == 404



