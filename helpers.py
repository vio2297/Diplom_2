import random
import string
import uuid

import requests

from urls import GET_INGREDIENTS, BASE_URL


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