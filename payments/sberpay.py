import requests
from config import SBERPAY_API_KEY, SBERPAY_SECRET_KEY


class SberPay:
    API_URL = "https://api.sberbank.ru/"

    @staticmethod
    def create_payment(amount: int):
        # Integrate SberPay API here
        pass