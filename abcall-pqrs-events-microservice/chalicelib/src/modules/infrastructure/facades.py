import requests

class Users:
    def __init__(self):
        self.base_url = 'http://users-microservice/api/users'  # URL del microservicio de usuarios

    def get_user_by_sub_or_none(self, user_sub):
        try:
            response = requests.get(f"{self.base_url}/user/{user_sub}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return None


class MicroservicesFacade:
    def __init__(self):
        self.users_service = Users()

    def get_user(self, user_sub):
        return self.users_service.get_user_by_sub_or_none(user_sub)
