import allure
import pytest
import requests
from data import UserData, ResponseStatus, ResponseMessages
from helpers import Helpers
from urls import BASE_URL, LOGIN_USER_ENDPOINT, CHANGE_USER_DATA, CREATE_USER_ENDPOINT


class TestChangeUserData:
    @allure.title("Проверка успешного изменения email для авторизированного пользователя")
    def test_change_user_email(self, create_and_login_user):
        token, email, password, *_ = create_and_login_user
        new_email = Helpers.generate_user_email()
        headers = {"Authorization": token}
        update_payload = {"email": new_email}

        with allure.step("Изменяем email пользователя"):
            update_response = requests.patch(f"{BASE_URL}{CHANGE_USER_DATA}", json=update_payload, headers=headers)
            assert update_response.status_code == 200

        json_data = update_response.json()
        assert json_data.get("success") is True

        # Проверяем, что можем залогиниться с новым email и старым паролем
        login_data = {"email": new_email, "password": password}
        login_response = requests.post(f"{BASE_URL}{LOGIN_USER_ENDPOINT}", json=login_data)
        assert login_response.status_code == 200, "Не удалось авторизоваться с новым email"

    @allure.title("Проверка успешного изменения пароля для авторизированного пользователя")
    def test_change_user_password(self, create_and_login_user):
        token, email, password, *_ = create_and_login_user
        new_password = Helpers.generate_user_password()
        headers = {"Authorization": token}
        update_payload = {"password": new_password}

        with allure.step("Изменяем пароль пользователя"):
            update_response = requests.patch(f"{BASE_URL}{CHANGE_USER_DATA}", json=update_payload, headers=headers)
            assert update_response.status_code == 200

        json_data = update_response.json()
        assert json_data.get("success") is True

        # Проверяем, что можем залогиниться с тем же email и новым паролем
        login_data = {"email": email, "password": new_password}
        login_response = requests.post(f"{BASE_URL}{LOGIN_USER_ENDPOINT}", json=login_data)
        assert login_response.status_code == 200, "Не удалось авторизоваться с новым паролем"

    @allure.title("Проверка успешного изменения имени для авторизированного пользователя")
    def test_change_user_name(self, create_and_login_user):
        token, email, password, *_ = create_and_login_user
        new_name = Helpers.generate_user_name()
        headers = {"Authorization": token}
        update_payload = {"name": new_name}

        with allure.step("Изменяем имя пользователя"):
            update_response = requests.patch(f"{BASE_URL}{CHANGE_USER_DATA}", json=update_payload, headers=headers)
            assert update_response.status_code == 200

        json_data = update_response.json()
        assert json_data.get("success") is True
        assert "user" in json_data, f"Ключ 'user' не найден в ответе: {json_data}"
        assert json_data["user"]["name"] == new_name, (
            f"Имя не обновилось. Ожидалось: {new_name}, получено: {json_data['user'].get('name')}"
        )



    @allure.title("Проверка изменения данных без авторизации")
    @allure.description("Попытка изменить email, password или name без токена авторизации должна завершиться ошибкой 401 и соответствующим сообщением")
    @pytest.mark.parametrize("key, value", [
        ("email", Helpers.generate_user_email()),
        ("password", Helpers.generate_user_password()),
        ("name", Helpers.generate_user_name())
    ])
    def test_change_data_without_auth(self, key, value):
        updated_payload = {key: value}

        with allure.step("Отправка PATCH-запроса без заголовка авторизации"):
            response = requests.patch(f"{BASE_URL}{CHANGE_USER_DATA}", json=updated_payload)

        with allure.step("Проверка, что статус ответа — 401 Unauthorized"):
            assert response.status_code == ResponseStatus.UNAUTHORIZED, (
                f"Ожидался статус 401, получен: {response.status_code}"
            )

        with allure.step("Проверка тела ответа и сообщения об ошибке"):
            json_data = response.json()
            assert json_data.get("success") is False, "Ожидался success=False"
            assert json_data.get("message") == ResponseMessages.NEED_AUTH_FOR_USER_UPDATES, (
                f"Ожидалось сообщение: '{ResponseMessages.NEED_AUTH_FOR_USER_UPDATES}', получено: '{json_data.get('message')}'"
            )



