from datetime import timedelta
import asyncio

import aioredis
import asyncpg

from bot.utils import check_expiration_date, get_new_expiration_date
from config import (PG_PORT, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                    POSTGRES_USER, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, FREE_REQUESTS_AMOUNT,
                    IS_FREE_REQUESTS)


async def get_redis():
    redis = await aioredis.create_redis_pool(
        (REDIS_HOST, REDIS_PORT),
        password=REDIS_PASSWORD,
        encoding='utf-8'
    )
    return redis


async def create_pg_connection():
    conn = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        port=PG_PORT
    )
    return conn


async def create_table_if_not_exists():
    conn = await create_pg_connection()
    is_exist = await conn.fetchval(
        "SELECT EXISTS (SELECT FROM pg_tables "
        "WHERE schemaname = 'public' AND tablename  = 'users');"
    )
    if not is_exist:
        await conn.execute(
            'CREATE TABLE users ('
            'user_id BIGINT PRIMARY KEY, '
            'requests_count INTEGER, '
            'subscription_end TIMESTAMP);'
        )
    await conn.close()


async def create_user(user_id: int):
    conn = await create_pg_connection()
    user = await conn.fetchrow(
        "SELECT * FROM users WHERE user_id = $1", user_id)
    if not user:
        await conn.execute(
            "INSERT INTO users ("
            "user_id, requests_count, subscription_end) VALUES ($1, $2, $3)",
            user_id, 0, None
        )
    await conn.close()


async def update_requests_count(user_id: int):
    conn = await create_pg_connection()
    await conn.execute(
        "UPDATE users SET requests_count = "
        "requests_count + 1 WHERE user_id = $1",
        user_id
    )
    requests_count = await conn.fetchval(
        "SELECT requests_count FROM users WHERE user_id = $1",
        user_id
    )
    await conn.close()
    return requests_count


async def check_subscription(user_id: int):
    conn = await create_pg_connection()
    subscription_end = await conn.fetchval(
        "SELECT subscription_end FROM users WHERE user_id = $1",
        user_id
    )
    requests_count = await conn.fetchval(
        "SELECT requests_count FROM users WHERE user_id = $1", user_id
    )
    if subscription_end is None:
        if requests_count is None or IS_FREE_REQUESTS or requests_count < FREE_REQUESTS_AMOUNT:
            return True
        else:
            return False
    return check_expiration_date(subscription_end)


async def process_successful_payment(user_id: int):
    conn = await create_pg_connection()
    subscription_end = await conn.fetchval(
        "SELECT subscription_end FROM users WHERE user_id = $1",
        user_id
    )

    if subscription_end is None or not check_expiration_date(subscription_end):
        new_subscription_end = get_new_expiration_date()
    else:
        new_subscription_end = subscription_end + timedelta(days=30)

    await conn.execute(
        "UPDATE users SET subscription_end = $1 WHERE user_id = $2",
        new_subscription_end, user_id
    )
    await conn.close()
