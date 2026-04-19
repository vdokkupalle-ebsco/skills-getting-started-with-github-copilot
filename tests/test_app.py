def test_root_redirects_to_index(client):
    # Arrange
    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_data(client):
    # Arrange
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_new_participant(client):
    # Arrange
    new_email = "test.student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": new_email},
    )

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    activity_data = client.get("/activities").json()
    assert new_email in activity_data["Chess Club"]["participants"]


def test_duplicate_signup_returns_bad_request(client):
    # Arrange
    duplicate_email = "duplicate.student@mergington.edu"
    first_response = client.post(
        "/activities/Gym Class/signup",
        params={"email": duplicate_email},
    )
    assert first_response.status_code == 200

    # Act
    second_response = client.post(
        "/activities/Gym Class/signup",
        params={"email": duplicate_email},
    )

    # Assert
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up"

    activity_data = client.get("/activities").json()
    assert activity_data["Gym Class"]["participants"].count(duplicate_email) == 1


def test_delete_participant_removes_participant(client):
    # Arrange
    email_to_remove = "michael@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": email_to_remove},
    )

    # Assert
    assert response.status_code == 200
    assert email_to_remove not in client.get("/activities").json()["Chess Club"]["participants"]


def test_delete_missing_participant_returns_not_found(client):
    # Arrange
    missing_email = "missing@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": missing_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
