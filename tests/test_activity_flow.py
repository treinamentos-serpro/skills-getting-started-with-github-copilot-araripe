from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_updates_activity_participants_immediately():
    activity_name = "Soccer Club"
    email = "newstudent@mergington.edu"

    activity_url = f"/activities/{quote(activity_name, safe='')}/participants?email={quote(email, safe='')}"
    if email in client.get("/activities").json()[activity_name]["participants"]:
        response = client.delete(activity_url)
        assert response.status_code == 200

    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup?email={quote(email, safe='')}"
    )

    assert response.status_code == 200, response.text

    updated_activity = client.get("/activities").json()[activity_name]
    assert email in updated_activity["participants"]

    cleanup = client.delete(activity_url)
    assert cleanup.status_code == 200, cleanup.text
