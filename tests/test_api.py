from fastapi import FastAPI
from fastapi.testclient import TestClient
from app_initialization import create_app

client = TestClient(create_app)


def test_vehicles():
    response = client.get("/vehicles")
    assert response.status_code == 200

def test_drivers():
    response = client.get("/drivers")
    assert response.status_code == 200