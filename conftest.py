
import pytest
import requests
from helpers import RegisterAndLogin
from urls import BASE_URL,  DELETE_USER



@pytest.fixture(scope='function')
def create_and_login_user():
    register_response, login_response, new_user_data = RegisterAndLogin.register_and_login_user()
    token = login_response.json().get("accessToken")
    yield token, new_user_data["email"], new_user_data["password"], register_response, login_response, new_user_data

    headers = {"Authorization": token}
    requests.delete(f"{BASE_URL}{DELETE_USER}", headers=headers)

