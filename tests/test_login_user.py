import allure
import pytest
import requests

import data
from data import UserData, ResponseStatus, ResponseMessages
from helpers import Helpers
from urls import BASE_URL, LOGIN_USER_ENDPOINT


class TestUserLogin:
    @allure.title("Проверка логина под существующим пользователем")
    @allure.description("Проверка успешной авторизации под существующим пользователем, тело ответа")
    def test_success_user_login(self):
        login_data = {
            "email": UserData.EXISTING_USER_EMAIL,
            "password": UserData.EXISTING_USER_PASSWORD
        }

        with allure.step("Отправка запроса на авторизацию пользователя"):
            response = requests.post(f"{BASE_URL}{LOGIN_USER_ENDPOINT}", json=login_data)

        with allure.step("Проверка кода ответа и структура тела"):
            assert response.status_code == data.ResponseStatus.OK, f"Ожидаемый статус 200, получен {response.status_code}, текст: {response.text}"

            json_data = response.json()
            assert json_data.get("success") is True , f"Ожидаемый success=True"
            assert "accessToken" in json_data, "accessToken отсутствует в теле ответа"
            assert "refreshToken" in json_data, "refreshToken, отсутствует в теле ответа "
            assert "user" in json_data, "user отсутствует в теле ответа"

            user = json_data.get ("user")
            assert user.get("email") == UserData.EXISTING_USER_EMAIL, f"Ожидаемый email: {UserData.EXISTING_USER_EMAIL}, получен: {user.get('email')}"
            assert user.get("name") == UserData.EXISTING_USER_NAME, f"Ожидаемое имя: {UserData.EXISTING_USER_NAME}, получено: {user.get('name')}"



    @allure.title("Проверка получения сообщения об ошибке при попытке авторизации с неверным паролем, логином или отсутствии одного из полей")
    @allure.description("Проверка тела ответа и получения сообщения об ошибке и коде 401 при попытке авторизироватся с неверными данными или отсутствии одного и данных ")
    @pytest.mark.parametrize('email, password, expected_message',
                             [
                                 (UserData.EXISTING_USER_EMAIL, Helpers.generate_user_password(), ResponseMessages.WRONG_DATA_LOGIN),
                                 (Helpers.generate_user_email(), UserData.EXISTING_USER_PASSWORD, ResponseMessages.WRONG_DATA_LOGIN),
                                 ('', UserData.EXISTING_USER_PASSWORD, ResponseMessages.WRONG_DATA_LOGIN),
                                 (UserData.EXISTING_USER_EMAIL, '', ResponseMessages.WRONG_DATA_LOGIN),
                             ])
    def test_user_login_with_wrong_data(self,email, password,expected_message):
        login_data = {
            "email": email,
            "password": password
        }

        with allure.step("Отправка запроса на авторизацию с некорректными данными"):
            response = requests.post(f"{BASE_URL}{LOGIN_USER_ENDPOINT}", json=login_data)

        with allure.step("Проверка ответа и сообщения об ошибке"):
            assert response.status_code == ResponseStatus.UNAUTHORIZED, f"Ожидаемый статус 401, получен {response.status_code}, текст: {response.text}"

            json_data = response.json()
            assert json_data.get("success") is False, "Получено success=True"
            assert json_data.get("message") == expected_message,f"Ожидаемое сообщение: '{expected_message}', получено: '{json_data.get('message')}'"

