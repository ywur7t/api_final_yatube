# API для Yatube

## Описание
Проект предоставляет API для работы с социальной сетью Yatube. Позволяет управлять постами, комментариями и подписками.

## Установка
1. Клонируйте репозиторий:
    ```
    git clone <URL>
    ```
2. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```
3. Выполните миграции:
    ```
    python manage.py migrate
    ```
4. Запустите сервер разработки:
    ```
    python manage.py runserver
    ```

## Примеры запросов

### Получение списка подписок
`GET /api/v1/follow/`

### Создание подписки
`POST /api/v1/follow/`
```json
{
    "following": "username"
}
