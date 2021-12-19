import requests
from django.utils.crypto import get_random_string


class OAuth:
    def __init__(self, token_data):
        self.token_data = token_data
        self._salesforce_user = None
        self._password = get_random_string(length=16)

    def _get_salesforce_user(self):
        sf_id_url = self.token_data.get("id")
        access_token = self.token_data.get("access_token")
        response = requests.get(
            sf_id_url, headers={"Authorization": f"Bearer {access_token}"}
        )

        assert (
            response.status_code == 200
        ), f"Could not retrieve user from Salesforce: {response.reason}"
        return response.json()

    @property
    def salesforce_user(self):
        if not self._salesforce_user:
            self._salesforce_user = self._get_salesforce_user()
        return self._salesforce_user

    @property
    def id(self):
        return self.salesforce_user.get("user_id")

    @property
    def first_name(self):
        return self.salesforce_user.get("first_name")

    @property
    def last_name(self):
        return self.salesforce_user.get("last_name")

    @property
    def username(self):
        return self.salesforce_user.get("username")

    @property
    def email(self):
        return self.salesforce_user.get("email")