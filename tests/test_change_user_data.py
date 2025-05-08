import allure
import pytest
import requests
from data import UserData, ResponseStatus, ResponseMessages
from helpers import Helpers
from urls import BASE_URL, LOGIN_USER_ENDPOINT, CHANGE_USER_DATA, CREATE_USER_ENDPOINT


class TestChangeUserData:
    @allure.title("Проверка успешного изменения данных для авторизированного пользователя")
    @allure.description("Для авторизированного пользователя успешно редактируем данные : email, password, name, проверка тела ответа и сообщение ")
    @pytest.mark.parametrize("key, value_generator",[
        ("email", Helpers.generate_user_email),
        ("password", Helpers.generate_user_password),
        ("name", Helpers.generate_user_name)
    ])

    def test_success_user_data_updates(self, key, value_generator, create_and_login_user):
        token, email, password = create_and_login_user
        new_value = value_generator()
        headers = {"Authorization": token}
        update_payload = {key: new_value}

        with allure.step(f"Отправка запроса на изменение поля '{key}' пользователя"):
            update_response = requests.patch(f"{BASE_URL}{CHANGE_USER_DATA}", json=update_payload, headers=headers)
            assert update_response.status_code == 200, f"Ожидался статус 200, получен: {update_response.status_code}"

        json_data = update_response.json()
        assert json_data.get("success") is True, f"Ожидался success=True, получен: {json_data.get('success')}"

        if key == "password":
            login_data = {
                "email": email,
                "password": new_value
            }
            login_response = requests.post(f"{BASE_URL}{LOGIN_USER_ENDPOINT}", json=login_data)
            assert login_response.status_code == 200, "Не удалось авторизоваться с новым паролем"

        elif key == "email":
            login_data = {
                "email": new_value,
                "password": password
            }
            login_response = requests.post(f"{BASE_URL}{LOGIN_USER_ENDPOINT}", json=login_data)
            assert login_response.status_code == 200, "Не удалось авторизоваться с новым email"

        else:  # name
            assert "user" in json_data, f"Ключ 'user' не найден в ответе: {json_data}"
            assert json_data["user"][key] == new_value, (
                f"{key} не обновился. Ожидалось: {new_value}, получено: {json_data['user'].get(key)}"
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

        with allure.step(f"Формируем тело запроса с изменением поля '{key}'"):
            pass

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



