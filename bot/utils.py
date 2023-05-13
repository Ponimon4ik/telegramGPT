import time

import openai

from config import config


async def gpt_conversation(conversation: list):
    openai.api_key = config.gpt_token
    for _ in range(4):
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=conversation
            )
            break
        except Exception:
            time.sleep(2)
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
