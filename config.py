import json
from dataclasses import dataclass

from environs import Env


@dataclass
class DatabaseConfig:
    pg_user: str
    pg_password: str
    pg_host: str
    pg_database: str
    pg_port: str


@dataclass
class RedisConfig:
    rd_host: str
    rd_port: str
    rd_password: str


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    redis: RedisConfig
    gpt_tokens: list


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        db=DatabaseConfig(
            pg_user=env('POSTGRES_USER'),
            pg_password=env('POSTGRES_PASSWORD'),
            pg_database=env('POSTGRES_DB'),
            pg_host=env('POSTGRES_HOST'),
            pg_port=env('PG_PORT')
        ),
        redis=RedisConfig(
            rd_host=env('REDIS_HOST'),
            rd_password=env('REDIS_PASSWORD'),
            rd_port=env('REDIS_PORT')
        ),
        gpt_tokens=json.loads(env('CHATGPT_TOKEN'))
    )


config = load_config()
