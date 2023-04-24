import os

import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHATGPT_TOKEN = os.getenv("CHATGPT_TOKEN")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
PG_PORT = os.getenv("PG_PORT")


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

IS_FREE_REQUESTS = os.getenv("FREE_REQUESTS")
FREE_REQUESTS_AMOUNT = int(os.getenv('FREE_REQUESTS_AMOUNT'))