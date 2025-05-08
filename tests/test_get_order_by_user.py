import allure
import requests

from data import UserData, ResponseStatus, ResponseMessages
from urls import BASE_URL, LOGIN_USER_ENDPOINT, GET_USER_ORDERS


class TestGetUserOrder:
    @allure.title("Успешное получение списка заказов авторизированного пользователя ")
    @allure.description("Проверка успешного получения списка заказов авторизированного пользователя")
    def test_get_orders_auth_user(self):
        with allure.step("Авторизация пользователя и получение токена"):
            login_data = {
                "email": UserData.EXISTING_USER_EMAIL,
                "password": UserData.EXISTING_USER_PASSWORD
            }
            login_response = requests.post(f"{BASE_URL}{LOGIN_USER_ENDPOINT}", json=login_data)
            assert login_response.status_code == ResponseStatus.OK
            access_token = login_response.json()["accessToken"]

        with allure.step("Получение заказов пользователя"):
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }
            response = requests.get(f"{BASE_URL}{GET_USER_ORDERS}", headers=headers)
            json_data = response.json()

            assert response.status_code == ResponseStatus.OK
            assert json_data["success"] is True
            assert isinstance(json_data["orders"], list)

    @allure.title("Попытка получить заказ без авторизации")
    @allure.description("Ожидаемый код 401 и сообщение об отсутсвии авторизации")
    def test_get_order_without_auth(self):
        with allure.step("Запрос заказов без авторизационного токена"):
            response = requests.get(f"{BASE_URL}{GET_USER_ORDERS}")
            json_data = response.json()

            assert response.status_code == ResponseStatus.UNAUTHORIZED
            assert json_data["success"] is False
            assert json_data["message"] == ResponseMessages.NEED_AUTH_FOR_ORDER_CREATION

