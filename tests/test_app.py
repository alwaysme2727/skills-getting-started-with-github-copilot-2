
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

client = TestClient(app)

# Save the initial state of activities
initial_activities = copy.deepcopy(activities)

def test_get_activities():
    # Reset activities to initial state
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_unregister():
    import uuid
    # Use a test activity and unique email
    activity_name = list(client.get("/activities").json().keys())[0]
    test_email = f"pytestuser_{uuid.uuid4().hex[:8]}@mergington.edu"
    # Sign up
    signup_url = f"/activities/{activity_name}/signup?email={test_email}"
    signup_response = client.post(signup_url)
    assert signup_response.status_code == 200, f"Signup failed: {signup_response.text}"
    # Unregister
    unregister_url = f"/activities/{activity_name}/unregister?email={test_email}"
    unregister_response = client.delete(unregister_url)
    assert unregister_response.status_code == 404, f"Unregister failed: {unregister_response.text}"
