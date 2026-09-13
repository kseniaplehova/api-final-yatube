# Проект Yatube API

### Описание

REST API для социальной сети Yatube. Проект позволяет управлять публикациями, группами и комментариями через HTTP-запросы. Пользователи могут получать список постов и комментариев, а авторизованные пользователи — создавать новые записи, редактировать и удалять собственный контент. Аутентификация реализована с использованием JWT-токенов (Djoser + SimpleJWT).

### Технологический стек

* **Python** 3.9+
* **Django** 3.2+
* **Django REST Framework** (DRF)
* **Djoser / Simple-JWT** (JWT-аутентификация)

---

### Как запустить проект локально

1. **Клонировать репозиторий и перейти в него:**

   ```bash
   git clone https://github.com/yandex-praktikum/api-final-yatube
cd api-final-yatube
   ```

2. **Создать и активировать виртуальное окружение:**

   *Linux / macOS:*

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   *Windows (PowerShell):*

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Установить зависимости:**

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Выполнить миграции:**

   ```bash
   python manage.py migrate
   ```

5. **Создать суперпользователя (администратора):**

   ```bash
   python manage.py createsuperuser
   ```

6. **Запустить сервер разработки:**

   ```bash
   python manage.py runserver
   ```

   Сервер запустится по адресу: http://127.0.0.1:8000/

---

### Сценарий работы с API (регистрация и выполнение запросов)

После запуска сервера выполните шаги ниже (через cURL, Postman или Insomnia), чтобы зарегистрироваться, получить JWT-токен и выполнить запросы к API.

#### Шаг 1. Регистрация нового пользователя

Отправьте POST-запрос на эндпоинт `/api/v1/users/`:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/ \
     -H "Content-Type: application/json" \
     -d '{"username": "test_user", "password": "your_password_123"}'
```

Ответ сервера (201 Created):

```json
{
    "email": "",
    "id": 1,
    "username": "test_user"
}
```

#### Шаг 2. Получение JWT-токена

Для аутентификации и выполнения запросов получите access-токен:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/jwt/create/ \
     -H "Content-Type: application/json" \
     -d '{"username": "test_user", "password": "your_password_123"}'
```

Ответ сервера (200 OK):

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Скопируйте значение поля `access`.

#### Шаг 3. Выполнение авторизованных запросов

Передавайте полученный токен в заголовке `Authorization` с префиксом `Bearer`:

**Создание поста:**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
     -H "Authorization: Bearer <ваш_access_token>" \
     -H "Content-Type: application/json" \
     -d '{"text": "Мой первый пост через Yatube API!"}'
```

Ответ сервера (201 Created):

```json
{
    "id": 1,
    "author": "test_user",
    "text": "Мой первый пост через Yatube API!",
    "pub_date": "2026-03-30T12:00:00Z",
    "image": null,
    "group": null
}
```

**Получение списка постов (доступно без токена):**

```bash
curl -X GET http://127.0.0.1:8000/api/v1/posts/
```

**Подписка на автора:**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/follow/ \
     -H "Authorization: Bearer <ваш_access_token>" \
     -H "Content-Type: application/json" \
     -d '{"following": "author_username"}'
```