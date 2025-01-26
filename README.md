# API Yatube

## Описание
API для социальной сети Yatube. Позволяет управлять постами, комментариями, подписками.

## Установка
1. Клонируйте репозиторий:
git clone <URL>

markdown
Копировать
Редактировать
2. Установите зависимости:
pip install -r requirements.txt

markdown
Копировать
Редактировать
3. Выполните миграции:
python manage.py migrate

markdown
Копировать
Редактировать
4. Запустите сервер:
python manage.py runserver

bash
Копировать
Редактировать

## Примеры запросов
### Получение списка подписок:
`GET /api/v1/follow/`
Authorization: Bearer <токен>

bash
Копировать
Редактировать

### Добавление подписки:
`POST /api/v1/follow/`
{ "following": "username" }