from fastapi.testclient import TestClient
from api.main import app, get_db
from api.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)

def test_get_all_items():
    response = client.get("/items")
    assert response.status_code == 200

def test_get_item():
    response = client.get("/item/21")
    assert response.status_code == 200
    assert response.json().get('id') == 21
    assert response.json().get('date') == "21.12.2021"
    assert response.json().get('link') == "https://nbs.sk/en/news/statement-from-the-nbs-bank-boards-25th-meeting-of-2021/"

def test_get_item_invalid_id():
    response = client.get("/item/999999999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Article not found'}

def test_delete_item_invalid_id():
    response = client.delete("/item/99999999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Article not found'}