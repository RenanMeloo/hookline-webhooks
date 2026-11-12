import pytest


@pytest.mark.django_db
def test_user_can_register(api_client):
    url = "/api/auth/register/"
    data = {
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "TestPassword123",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201

    login_url = "/api/auth/token/"
    login_data = {
        "username": "testuser",
        "password": "TestPassword123",
    }
    login_response = api_client.post(login_url, login_data, format="json")
    assert login_response.status_code == 200