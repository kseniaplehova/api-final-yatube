# Yatube API (final)

REST API for Yatube, a small social network: posts, groups, comments and author subscriptions, with JWT authentication.

> Educational project — Yandex Practicum, Python Developer course.

## Features

- **JWT authentication** via Djoser + Simple JWT (`Authorization: Bearer <access>`); user registration through Djoser endpoints.
- **Posts**: full CRUD, optional image upload and optional group; author is set automatically from the token.
- **Groups**: read-only (list and detail).
- **Comments**: full CRUD nested under a post (`/posts/{post_id}/comments/`).
- **Follows**: list the current user's subscriptions and subscribe to an author; supports search by the followed username (`?search=`). Validation forbids following yourself and duplicate subscriptions (plus a DB-level unique constraint).
- **Permissions**: anyone can read; creating requires authentication; editing and deleting posts and comments is allowed only to their author (custom `IsAuthenticatedAuthorOrReadOnly`). Subscriptions are available to authenticated users only.
- **Pagination**: `limit` / `offset` on the posts list.
- ReDoc API documentation served at `/redoc/`.

## Endpoints

All paths are prefixed with `/api/v1/`.

| Method | Path | Description |
| --- | --- | --- |
| POST | `users/` | Register a user (Djoser) |
| POST | `jwt/create/`, `jwt/refresh/`, `jwt/verify/` | Obtain, refresh, verify JWT |
| GET, POST | `posts/` | List (optionally paginated) / create posts |
| GET, PUT, PATCH, DELETE | `posts/{id}/` | Post detail (write: author only) |
| GET | `groups/`, `groups/{id}/` | Groups |
| GET, POST | `posts/{post_id}/comments/` | Comments of a post |
| GET, PUT, PATCH, DELETE | `posts/{post_id}/comments/{id}/` | Comment detail (write: author only) |
| GET, POST | `follow/` | Own subscriptions / follow an author |

## Tech stack

- Python, Django 5.1.1, Django REST Framework 3.15.2
- Djoser 2.3.1, djangorestframework-simplejwt 5.4.0
- SQLite, Pillow 11.0.0
- pytest 8.3.3, pytest-django 4.9.0, flake8

## Getting started

```bash
git clone https://github.com/kseniaplehova/api-final-yatube.git
cd api-final-yatube
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd yatube_api
python manage.py migrate
python manage.py runserver
```

The API is then available at `http://127.0.0.1:8000/api/v1/`, documentation at `http://127.0.0.1:8000/redoc/`.

## Usage example

```bash
# register
curl -X POST http://127.0.0.1:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "password": "your_password_123"}'

# get a token
curl -X POST http://127.0.0.1:8000/api/v1/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "password": "your_password_123"}'

# create a post
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"text": "My first post"}'

# paginated list (no token needed)
curl "http://127.0.0.1:8000/api/v1/posts/?limit=10&offset=0"
```

## Tests

From the repository root:

```bash
pytest
```

The `tests/` directory covers JWT, posts, groups, comments and follows. A Postman collection is available in `postman_collection/`.

## Author

Ksenia Plehova — [GitHub](https://github.com/kseniaplehova)
