import random
import string
import uuid

import requests

from urls import GET_INGREDIENTS, BASE_URL, CREATE_USER_ENDPOINT, LOGIN_USER_ENDPOINT


class Helpers:
    @staticmethod
    def generate_user_email():
        return f"test_{uuid.uuid4().hex[:12]}@example.com"

    @staticmethod
    def generate_user_password():
        length = 6
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


    @staticmethod
    def generate_user_name():
        length = 4
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


    @staticmethod
    def generate_user_body():
        return {
            "email": Helpers.generate_user_email(),
            "password": Helpers.generate_user_password(),
            "name": Helpers.generate_user_name()
        }


class ChangeTestDataHelper:
    @staticmethod
    def modify_create_user_body(key, value):
        body = Helpers.generate_user_body()
        body[key] = value
        return body

class IngredientsHelper:
    @staticmethod
    def get_valid_ingredients():
        response = requests.get(f"{BASE_URL}{GET_INGREDIENTS}")
        assert response.status_code == 200, f"Не удалось получить ингредиенты: {response.text}"
        data = response.json()
        return [item["_id"] for item in data["data"]]

class RegisterAndLogin:
    @staticmethod
    def register_and_login_user():
        new_user_data = Helpers.generate_user_body()
        register_response = requests.post(f"{BASE_URL}{CREATE_USER_ENDPOINT}", json=new_user_data)
        login_data = {
            "email": new_user_data["email"],
            "password": new_user_data["password"]
        }
        login_response = requests.post(f"{BASE_URL}{LOGIN_USER_ENDPOINT}", json=login_data)
        return register_response, login_response, new_user_data