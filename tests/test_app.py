from src import app as app_module


def test_get_activities_returns_seeded_activities(client):
    # Arrange
    expected_activity_count = len(app_module.activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == expected_activity_count
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"] == app_module.activities["Chess Club"]["participants"]


def test_signup_adds_new_participant(client, activity_name, new_student_email):
    # Arrange
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_url, params={"email": new_student_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_student_email} for {activity_name}"}
    assert new_student_email in app_module.activities[activity_name]["participants"]


def test_signup_returns_not_found_for_unknown_activity(client, new_student_email):
    # Arrange
    signup_url = "/activities/Unknown Club/signup"

    # Act
    response = client.post(signup_url, params={"email": new_student_email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_rejects_duplicate_participant(client, activity_name, existing_student_email):
    # Arrange
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_url, params={"email": existing_student_email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_removes_existing_participant(client, activity_name, existing_student_email):
    # Arrange
    unregister_url = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(unregister_url, params={"email": existing_student_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {existing_student_email} from {activity_name}"}
    assert existing_student_email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_not_found_for_unknown_activity(client, new_student_email):
    # Arrange
    unregister_url = "/activities/Unknown Club/participants"

    # Act
    response = client.delete(unregister_url, params={"email": new_student_email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_not_found_for_missing_participant(client, activity_name, new_student_email):
    # Arrange
    unregister_url = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(unregister_url, params={"email": new_student_email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in this activity"}