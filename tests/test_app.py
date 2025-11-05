import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    for activity in data.values():
        assert "description" in activity
        assert "participants" in activity

def test_signup_and_unregister():
    # Use a unique email for testing
    test_email = "pytest_user@example.com"
    activity_name = list(client.get("/activities").json().keys())[0]

    # Sign up
    signup_url = f"/activities/{activity_name}/signup?email={test_email}"
    response = client.post(signup_url)
    assert response.status_code == 200
    assert "message" in response.json()

    # Duplicate signup should fail
    response = client.post(signup_url)
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

    # Unregister
    unregister_url = f"/activities/{activity_name}/unregister?email={test_email}"
    response = client.post(unregister_url)
    assert response.status_code == 200
    assert "message" in response.json()

    # Unregister again should fail
    response = client.post(unregister_url)
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"
