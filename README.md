
# MilesEdu Backend Assignment

This Django project demonstrates backend proficiency using Django, Django REST Framework, PostgreSQL, and Redis. It includes user authentication, a user activity logging system, and API endpoints for managing and querying activity data.

---

## Tech Stack

- Python 3.13
- Django 4.x
- Django REST Framework (DRF)
- PostgreSQL (can swap with SQLite for testing)
- Redis (for caching)

---

## Setup Instructions

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd Miles_Ed
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Redis server**
   ```bash
   redis-server
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

---

## Features

- **Custom User Model**
- **Login / Logout / Registration**
- **Activity Log with Metadata**
- **Status transitions (PENDING → IN_PROGRESS → DONE)**
- **Admin-only log viewing**
- **Filtering by action type, date range**
- **Redis caching for GET list endpoint (1 minute)**
- **Signal-based logging for login/logout**

---

## API Endpoints

| Endpoint                         | Method | Auth | Description                              |
|----------------------------------|--------|------|------------------------------------------|
| `/api/accounts/register/`        | POST   | ❌    | User registration                        |
| `/api/accounts/custom-login/`    | POST   | ❌    | Custom login, returns access/refresh     |
| `/api/accounts/custom-logout/`   | POST   | ✅    | Custom logout (blacklists token)         |
| `/api/actions/activity/`         | GET    | ✅    | List current user's logs (cached)        |
| `/api/actions/activity/`         | POST   | ✅    | Log new activity                         |
| `/api/actions/activity/{id}/transition/` | PATCH | ✅ | Update log status                        |
| `/api/actions/activity/all_logs/`| GET    | ✅ (Admin only) | View all user logs              |

---

## Running Tests

```bash
python manage.py test
```

---

## Optional Deployment (Suggested)

- Use Docker with separate services for Django, PostgreSQL, and Redis
- Add `.env` for managing secrets
- Add Nginx/Gunicorn for production deployment
