import asyncpg

from config import config


async def create_pg_connection():
    conn = await asyncpg.connect(
        user=config.db.pg_user,
        password=config.db.pg_password,
        host=config.db.pg_host,
        database=config.db.pg_database,
        port=config.db.pg_port
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
            'created_date DATE NOT NULL DEFAULT CURRENT_DATE);'
        )
    await conn.close()


async def create_user(user_id: int):
    conn = await create_pg_connection()
    user = await conn.fetchrow(
        "SELECT * FROM users WHERE user_id = $1", user_id)
    if not user:
        await conn.execute(
            "INSERT INTO users ("
            "user_id, requests_count) VALUES ($1, $2)",
            user_id, 0
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


async def get_statistics():
    conn = await create_pg_connection()
    results = await conn.fetch(
        "SELECT created_date, COUNT(*) AS user_count, SUM(requests_count) AS total_requests_count "
        "FROM users "
        "GROUP BY created_date;"
    )
    await conn.close()
    statistics = [['date', 'new_users', 'total_requests']]
    for row in results:
        formatted_row = [
            f"{row['created_date']:%Y-%m-%d}",
            row['user_count'],
            row['total_requests_count']
        ]
        statistics.append(formatted_row)
    return statistics
