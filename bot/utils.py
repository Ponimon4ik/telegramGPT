import time

import openai

from config import config

MAX_RETRIES = len(config.gpt_tokens) + 10

api_keys = config.gpt_tokens  # список ваших API-ключей
current_key_index = 0  # индекс текущего используемого ключа
last_request_time = 0  # время последнего запроса


def _get_api_key(next_key=False):
    global current_key_index, last_request_time

    current_time = time.time()
    elapsed_time = current_time - last_request_time

    if elapsed_time >= 20 and not next_key:  # если прошло 20 секунд или более с предыдущего запроса
        last_request_time = current_time  # обновляем время последнего запроса
        return api_keys[current_key_index]

    if current_key_index == len(api_keys) - 1:
        current_key_index = 0  # начинаем с начала списка ключей
        time.sleep(20)
    else:
        current_key_index += 1
    return api_keys[current_key_index]


async def gpt_conversation(conversation: list):
    openai.api_key = _get_api_key()
    for _ in range(MAX_RETRIES):
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=conversation
            )
            break
        except Exception:
            openai.api_key = _get_api_key(next_key=True)
    else:
        raise ConnectionError()
    conversation.append(
        {
            'role': response.choices[0].message.role,
            'content': response.choices[0].message.content
        }
    )
    total_tokens = response['usage']['total_tokens']
    if total_tokens > 3800:
        del conversation[:2]
    return conversation
