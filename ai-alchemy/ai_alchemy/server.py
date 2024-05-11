import requests

class PhoneNumberValidator:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.api_url = "https://api.numlookupapi.com/v1/validate/"


    def validate(self, phone_number: str, country_code: str = None) -> bool:
        if not phone_number:
            raise ValueError("Phone Number cannot be empty!")
        response = self._make_api_call(phone_number, country_code)
        if response.ok:
            return response.json()["valid"]
        else:
            response.raise_for_status()

    def _make_api_call(self, phone_number: str, country_code: str = None):
        params = {"apikey": self.api_key}
        if country_code:
            params["country_code"] = country_code
        response = requests.get(self.api_url + phone_number, params=params)
        return response