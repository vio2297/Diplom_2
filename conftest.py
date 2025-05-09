from helpers import Helpers
import pytest
import requests
from urls import CREATE_USER_ENDPOINT, BASE_URL, LOGIN_USER_ENDPOINT, DELETE_USER


@pytest.fixture(scope='function')
def create_and_login_user():
    # создает нового пользователя и авторизует его, возвращая токен для использования в тестах.
    new_user_data = Helpers.generate_user_body()
    # Регистрация нового пользователя
    register_response = requests.post(f"{BASE_URL}{CREATE_USER_ENDPOINT}", json=new_user_data)
    assert register_response.status_code == 200, f"Ошибка при регистрации: {register_response.text}"

    login_data = {
        "email": new_user_data["email"],
        "password": new_user_data["password"]
    }

    login_response = requests.post(f"{BASE_URL}{LOGIN_USER_ENDPOINT}", json=login_data)
    assert login_response.status_code == 200, f"Ошибка при авторизации: {login_response.text}"

    token = login_response.json().get("accessToken")
    assert token, "Токен не получен"

    yield token, new_user_data["email"], new_user_data["password"]
    # Очистка после теста - удаление пользователя
    headers = {"Authorization": token}
    requests.delete(f"{BASE_URL}{DELETE_USER}", headers=headers)

