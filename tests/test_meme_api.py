import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from public_api.main import app
from public_api.database import Base, get_db

# Используем in-memory SQLite для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем тестовую базу данных
Base.metadata.create_all(bind=engine)

# Заменяем зависимость get_db для использования тестовой базы данных
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

def test_create_meme(test_client):
    response = test_client.post(
        "/memes/",
        data={"title": "Test Meme", "description": "Test Description"},
        files={"file": ("test.jpg", open("test.jpg", "rb"), "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Meme"
    assert data["description"] == "Test Description"
    assert "image_url" in data

def test_get_meme(test_client):
    # Создаем мем, чтобы было что получать
    response = test_client.post(
        "/memes/",
        data={"title": "Test Meme", "description": "Test Description"},
        files={"file": ("test.jpg", open("test.jpg", "rb"), "image/jpeg")}
    )
    meme_id = response.json()["id"]
    
    response = test_client.get(f"/memes/{meme_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == meme_id
    assert data["title"] == "Test Meme"
    assert data["description"] == "Test Description"

def test_update_meme(test_client):
    # Создаем мем, чтобы было что обновлять
    response = test_client.post(
        "/memes/",
        data={"title": "Test Meme", "description": "Test Description"},
        files={"file": ("test.jpg", open("test.jpg", "rb"), "image/jpeg")}
    )
    meme_id = response.json()["id"]
    
    response = test_client.put(
        f"/memes/{meme_id}",
        data={"title": "Updated Title", "description": "Updated Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"

def test_delete_meme(test_client):
    # Создаем мем, чтобы было что удалять
    response = test_client.post(
        "/memes/",
        data={"title": "Test Meme", "description": "Test Description"},
        files={"file": ("test.jpg", open("test.jpg", "rb"), "image/jpeg")}
    )
    meme_id = response.json()["id"]
    
    response = test_client.delete(f"/memes/{meme_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == meme_id
    
    # Проверяем, что мем был удален
    response = test_client.get(f"/memes/{meme_id}")
    assert response.status_code == 404
