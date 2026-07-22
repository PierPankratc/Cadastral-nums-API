# Test Case: FastAPI service with PostgreSQL and fake external service

Этот проект реализует простой сервис, который принимает кадастровый номер, широту и долготу, отправляет запрос во внешний эмулируемый сервис, сохраняет данные запроса и ответ в PostgreSQL и возвращает результат клиенту.

## Что делает сервис

- принимает запрос на эндпоинте `/query`
- вызывает внешний сервис на `/result`
- сохраняет запрос и ответ в таблицу `cadastral_info`
- возвращает историю запросов по эндпоинту `/history`
- позволяет проверить доступность сервиса через `/ping`

## Стек

- Python 3.13+
- FastAPI
- PostgreSQL
- asyncpg
- Docker
- Docker Compose
- Pytest

## API

### POST `/query`

Принимает JSON с полями:

```json
{
  "cadastral_number": "12345678",
  "latitude": 55.75,
  "longitude": 37.61
}
```

Ответ:

```json
{
  "status": "success",
  "result": true
}
```

### GET `/ping`

Проверяет доступность сервиса и внешнего обработчика.

### GET `/history`

Возвращает список всех сохранённых запросов.

### GET `/result`

Эндпоинт эмулируемого внешнего сервиса. Возвращает случайное значение `true` или `false`.

## База данных

Проект использует PostgreSQL. При запуске приложения выполняется инициализация таблицы `cadastral_info` через raw SQL.

Таблица содержит:

- `id`
- `cadastral_number`
- `latitude`
- `longitude`
- `created_at`
- `server_response`

## Запуск через Docker Compose

Из корня проекта выполните:

```bash
docker compose up --build
```

После запуска будут доступны:

- API: http://localhost:8000
- fake service: http://localhost:8001
- PostgreSQL: localhost:5432

## Локальный запуск без Docker

### 1. Установка зависимостей

```bash
python -m pip install -e .
```

### 2. Настройка переменных окружения

```bash
set DSN=postgresql://postgres:postgres@localhost:5432/test_case
set FAKE_SERVICE_URL=http://127.0.0.1:8001
```

### 3. Запуск базы данных

Нужно запустить PostgreSQL и создать базу `test_case`.

### 4. Запуск сервисов

```bash
uvicorn fake_servis:fake_servis --host 127.0.0.1 --port 8001
uvicorn main:app --host 127.0.0.1 --port 8000
```

## Пример запроса

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"cadastral_number":"12345678","latitude":55.75,"longitude":37.61}'
```


## Примечание

В текущей реализации реализованы основной API, эмулируемый внешний сервис и запуск через Docker Compose. Дополнительные задачи, такие как авторизация или полноценные Alembic-миграции, можно добавить позднее.
