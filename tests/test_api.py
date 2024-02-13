from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

# python -m pytest ./tests/

# uvicorn --app-dir=. api.main:app --reload

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"hello"}