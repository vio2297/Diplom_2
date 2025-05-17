import allure
import pytest
import requests
from data import UserData, IngredientsData, ResponseStatus, ResponseMessages
from helpers import IngredientsHelper
from urls import BASE_URL, LOGIN_USER_ENDPOINT, CREATE_ORDER_ENDPOINT


class TestCreateOrder:
    @allure.title("Создание заказа авторизированным пользователем с ингредиентами ")
    @allure.description("Авторизирование в системе и создание заказа, получение кода 200 ")
    def test_success_order_creation_with_auth_user(self, create_and_login_user):
        token = create_and_login_user[0]

        headers = {
                "Authorization": token,
                "Content-Type": "application/json"
        }

        with allure.step("Получение валидных ингредиентов"):
            ingredients = IngredientsHelper.get_valid_ingredients()
            assert len(ingredients) >= 2, "Недостаточно ингредиентов для создания заказа"

        with allure.step("Создание заказа с валидными ингредиентами"):
            order_data = {"ingredients": ingredients[:2]}
            response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=order_data, headers=headers)

            assert response.status_code == 200, f"Ожидался 200, получен: {response.status_code}, ответ: {response.text}"
            json_data = response.json()
            assert json_data["success"] is True, f"Заказ не был успешно создан: {json_data}"




    @allure.title("Создание заказа без авторизации но с ингредиентами")
    @allure.description("Создание заказа для неавторизованного пользователя, ожидаем успешный ответ (200) без токена.")
    def test_create_order_without_auth(self):
        with allure.step("Получение валидных ингредиентов"):
            ingredients = IngredientsHelper.get_valid_ingredients()
            assert len(ingredients) >= 2, "Недостаточно ингредиентов для создания заказа"

        with allure.step("Попытка создания заказа с валидными ингредиентами"):
            order_data = {"ingredients": ingredients[:2]}
            response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=order_data, headers={"Content-Type":"application/json"})


            assert response.status_code == ResponseStatus.OK
            json_data = response.json()
            assert response.status_code == 200, f"Ожидался 200, получен: {response.status_code}"
            assert json_data["success"] is True, f"Заказ не был успешно создан: {json_data}"




    @allure.title("Создание заказа с авторизированным пользователям но без ингредиентов ")
    @allure.description("Авторизированный пользователь создает заказ без ингредиентов")
    def test_create_order_with_auth_user_without_ingredients(self,create_and_login_user):
        token = create_and_login_user[0]

        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        with allure.step("Создание заказа без ингредиентов"):
            order_data = {"ingredients":[]}
            response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=order_data, headers=headers)
            json_data = response.json()
            assert response.status_code == ResponseStatus.BAD_REQUEST, (f"Ожидался 400, получен: {response.status_code}, ответ: {json_data}"
                                                                        )
            assert json_data["success"] is False, "Ожидалось success = False"




    @allure.title("Создание заказа без авторизации и без ингредиентов")
    @allure.description("Создание заказа с неавторизованным пользователем и без ингредиентов, проверка на наличие ошибки и текста ошибки")
    def test_create_order_without_auth_and_ingredients(self):
        with allure.step("Отправка запроса без авторизации и без ингредиентов"):
            data = {"ingredients": []}
            response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=data)
            json_data = response.json()
            assert response.status_code == ResponseStatus.BAD_REQUEST
            assert json_data["success"] is False




    @allure.title("Создание заказа для авторизированного пользователя и с невалидным ингредиентом ")
    @allure.description("Проверка наличия сообщение об ошибке и коде 500 при попытке создать заказ с невалидным ингредиентом")
    def test_create_order_with_invalid_ingredient(self,create_and_login_user):
        token = create_and_login_user[0]

        with allure.step("Создание заказа"):
            headers = {
                "Authorization": token,
                "Content-Type": "application/json"
            }
            order_data = {"ingredients": IngredientsData.INVALID_INGREDIENTS}
            response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=order_data, headers=headers)
            assert response.status_code == ResponseStatus.INTERNAL_SERVER_ERROR
