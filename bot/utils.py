import openai

from config import config


async def gpt_conversation(conversation: list):
    openai.api_key = config.gpt_token
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=conversation
        )
    except Exception as mistake:
        raise ConnectionError(mistake)
    conversation.append(
        {
            'role': response.choices[0].message.role,
            'content': response.choices[0].message.content
        }
    )
    total_tokens = response['usage']['total_tokens']
    if total_tokens > 3800:
        del conversation[0]
    return conversation
