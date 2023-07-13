# telegramGPT
Телеграм бот для взаимодействия с чат ботом GPT


### Установка Docker:

Установите Docker
```
sudo apt install docker
```

Установите docker-compose, с этим вам поможет [официальная документация](https://docs.docker.com/compose/install/)

### Как запустить проект:

Клонировать репозиторий и перейти в директорию с репозиторием:
```
cd telegramGPT
```

Создать env-файл и прописать переменные окружения в нём:

```
touch .env
```
```
BOT_TOKEN=1848758819:AAE-43QpuXm5W31wEIPbTGe6xidI5phoMpc
CHATGPT_TOKENS=["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", "sk-24PTUUkvi3z5lznFP7nwT3BlbkFJIwpHmuSM5zCnVLdwdroHHy", ...]

POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_DB=name
PG_PORT=5432

REDIS_HOST=redis_db
REDIS_PORT=6379
REDIS_PASSWORD=password

ADMIN_IDS=[1299121, 102003012, ...]

```

Запустить docker-compose
```
docker-compose up -d
```
