# Memes API

Memes API - это веб-приложение на базе FastAPI, предоставляющее API для работы с коллекцией мемов. Приложение позволяет добавлять, обновлять, получать и удалять мемы, а также хранить изображения мемов в S3-совместимом хранилище (например, MinIO).

## Функциональность

- **Добавить мем**: POST `/memes/` - Добавляет новый мем с картинкой и текстом.
- **Обновить мем**: PUT `/memes/{id}` - Обновляет существующий мем по его ID.
- **Получить мем**: GET `/memes/{id}` - Получает конкретный мем по его ID.
- **Список мемов**: GET `/memes/` - Получает список всех мемов с поддержкой пагинации.
- **Удалить мем**: DELETE `/memes/{id}` - Удаляет мем по его ID.

## Требования

- Python 3.10+
- PostgreSQL
- MinIO (или другое S3-совместимое хранилище)

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/memes-api.git
cd memes-api

### 2. Создание и активация виртуального окружения

bash

python -m venv venv
source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`

### 3. Установка зависимостей

bash

pip install -r requirements.txt


### 4. Настройка окружения

Создайте файл .env в корневой директории проекта и добавьте следующие переменные окружения:

makefile

DATABASE_URL=postgresql://user:password@localhost/dbname
AWS_ACCESS_KEY_ID=your_minio_access_key
AWS_SECRET_ACCESS_KEY=your_minio_secret_key
S3_BUCKET_NAME=your_bucket_name
S3_ENDPOINT_URL=http://localhost:9000

### 5. Запуск MinIO

Скачайте и установите MinIO, затем запустите его:

bash

minio server /data

Создайте бакет, указанный в S3_BUCKET_NAME, через консоль MinIO или с помощью mc (MinIO Client).

### 6. Инициализация базы данных

Примените миграции Alembic для создания необходимых таблиц в базе данных:

bash

alembic upgrade head

### 7. Запуск приложения

bash

uvicorn public_api.main:app --reload

## Приложение будет доступно по адресу http://127.0.0.1:8000.

Тестирование

Запуск тестов

Используйте pytest для запуска тестов:

bash

pytest