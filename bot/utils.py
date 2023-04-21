from datetime import datetime, timedelta

import openai

from config import CHATGPT_TOKEN


async def gpt_request(prompt: str):
    openai.api_key = CHATGPT_TOKEN
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.8,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response["choices"][0]["text"].strip()
    except Exception:
        return "Извините, произошла ошибка при обработке вашего запроса."


def check_expiration_date(expiration_date: datetime):
    return datetime.now() < expiration_date


def get_new_expiration_date():
    return datetime.now() + timedelta(days=30)
