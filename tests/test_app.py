import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities dict before each test to ensure isolation."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)

def test_get_activities():
    """Test GET /activities returns the activities dict."""
    # Arrange: No special setup needed

    # Act: Make the GET request
    response = client.get("/activities")

    # Assert: Check status and response content
    assert response.status_code == 200
    assert response.json() == activities

def test_signup_happy_path():
    """Test successful signup for an activity."""
    # Arrange: Choose an email and activity
    email = "new@mergington.edu"
    activity_name = "Chess Club"

    # Act: Make the POST request
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check status, message, and that email was added
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert email in activities[activity_name]["participants"]

def test_signup_activity_not_found():
    """Test signup for a nonexistent activity."""
    # Arrange: Use an invalid activity name
    email = "test@mergington.edu"
    activity_name = "Nonexistent"

    # Act: Make the POST request
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check for 404 and error message
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_signup_already_signed_up():
    """Test signup when already signed up."""
    # Arrange: Use an email already in the activity
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    # Act: Make the POST request
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check for 400 and error message
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_remove_happy_path():
    """Test successful removal from an activity."""
    # Arrange: Use an existing participant
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    # Act: Make the DELETE request
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check status, message, and that email was removed
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]
    assert email not in activities[activity_name]["participants"]

def test_remove_activity_not_found():
    """Test removal from a nonexistent activity."""
    # Arrange: Use an invalid activity name
    email = "test@mergington.edu"
    activity_name = "Nonexistent"

    # Act: Make the DELETE request
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check for 404 and error message
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_remove_not_signed_up():
    """Test removal when not signed up."""
    # Arrange: Use an email not in the activity
    email = "notsigned@mergington.edu"
    activity_name = "Chess Club"

    # Act: Make the DELETE request
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check for 400 and error message
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]