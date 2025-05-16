import allure
import pytest
import requests
import data
from conftest import create_and_login_user
from data import ResponseStatus, UserData
from helpers import Helpers
from urls import BASE_URL, CREATE_USER_ENDPOINT

class TestUserRegister:
    @allure.title("Успешная регистрация пользователя")
    @allure.description("Создание пользователя. Проверка статуса ответа и тела ответа")
    def test_success_registration(self, create_and_login_user):
        token, email, password, register_response, login_response, user_data = create_and_login_user
        with allure.step("Проверка успешного ответа"):
            assert register_response.status_code == ResponseStatus.OK, f"Статус: {register_response.status_code}, текст: {register_response.text}"
            assert register_response.json().get("success") is True, f"Ответ: {register_response.json()}"


    @allure.title("Получение ошибки при попытке создать уже зарегистриованого пользователя")
    @allure.description("Проверка создания существующего пользователя повторно и проверка кода и текста ошибки")
    def test_error_duplicate_user(self):
        with allure.step("Формирование данных уже существующего пользователя"):
            existing_user = {
                "email": UserData.EXISTING_USER_EMAIL,
                "password": UserData.EXISTING_USER_PASSWORD,
                "name": UserData.EXISTING_USER_NAME
            }

        with allure.step("Регистрация пользователя (первый запрос)"):
            requests.post(f"{BASE_URL}{CREATE_USER_ENDPOINT}", json=existing_user)

        with allure.step("Попытка повторной регистрации того же пользователя"):
            response = requests.post(f"{BASE_URL}{CREATE_USER_ENDPOINT}", json=existing_user)
            json_data = response.json()

        with allure.step("Проверка кода ответа и текста ошибки"):
            assert response.status_code == ResponseStatus.FORBIDDEN, f"Ожидаемый статус 403, получен {response.status_code}, текст: {response.text}"
            assert json_data.get("success") is False, "Ожидаемый success=False"
            assert json_data.get("message") == data.ResponseMessages.EXISTING_USER_REGISTRATION, f"Ожидаемое сообщкеие {data.ResponseMessages.EXISTING_USER_REGISTRATION}, получено :{json_data.get("message")}"



    @allure.title("Получение сообщения об ошибке при попытке создать пользователя без одного из обязательных полей: email, password, name")
    @allure.description("Запрос на создание пользователя без обязательного поля и проверка наличия кода 403 и текста ошибки")
    @pytest.mark.parametrize('key, value',
                             [
                                 ("email", ""),
                                 ("password", ""),
                                 ("name", "")
                             ])
    def test_failed_user_creation_without_data(self, key, value):
        user_data = Helpers.generate_user_body()
        user_data[key] = value
        with allure.step(f"Отправка запроса на создание пользователя без поля '{key}'"):
            response = requests.post(f"{BASE_URL}{CREATE_USER_ENDPOINT}", json=user_data)

        with allure.step("Проверка, что возвращён статус-код 403 и сообщение об ошибке"):
            assert response.status_code == ResponseStatus.FORBIDDEN, f"Ожидаемый статус 403, получен {response.status_code}, текст: {response.text}"
            json_data = response.json()
            assert json_data.get("success") is False, "Ожидаемый success=False"
            assert json_data.get("message") == data.ResponseMessages.MISSING_DATA_USER_REGISTRATION, f"Ожидаемое сообщение: {data.ResponseMessages.MISSING_DATA_USER_REGISTRATION}, получено: {json_data.get('message')}"
