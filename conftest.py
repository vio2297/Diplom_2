from data import ResponseStatus, UserData
from helpers import Helpers
import pytest
import requests
from urls import CREATE_USER_ENDPOINT, BASE_URL, LOGIN_USER_ENDPOINT, DELETE_USER


@pytest.fixture
def unique_user():
    user_data = Helpers.generate_user_body()
    response = requests.post(f"{BASE_URL}{CREATE_USER_ENDPOINT}", json=user_data)
    assert response.status_code == ResponseStatus.OK, f"Ошибка при создании пользователя: {response.text}"
    return user_data

@pytest.fixture
def existing_user():
    user_data = {
        "email": UserData.EXISTING_USER_EMAIL,
        "password": UserData.EXISTING_USER_PASSWORD,
        "name": UserData.EXISTING_USER_NAME
    }
    requests.post(f"{BASE_URL}{CREATE_USER_ENDPOINT}", json=user_data)
    return user_data

@pytest.fixture
def missing_field_user(request):
    key_to_remove = request.param
    user_data = Helpers.generate_user_body()
    user_data.pop(key_to_remove)
    return user_data, key_to_remove


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

