import requests
from config import TINKOFF_API_KEY, TINKOFF_SECRET_KEY


class TinkoffPay:
    API_URL = "https://securepay.tinkoff.ru/"

    @staticmethod
    def create_payment(amount: int):
        # Integrate Tinkoff Pay API here
        pass