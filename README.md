# telegramGPT
Телеграм бот для взаимодействия с чат ботом GPT

CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    requests_count INTEGER,
    subscription_end TIMESTAMP
);
