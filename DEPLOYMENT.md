# Deployment Guide

## Environment Setup

### 1. Copy Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and set your values:

```env
DJANGO_SECRET_KEY=your-secure-random-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com

CORS_ALLOWED_ORIGINS=https://your-frontend.com

DJANGO_LOG_LEVEL=INFO
```

### 2. Generate Secure Secret Key

For production, generate a secure secret key:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

## Production Deployment

### Gunicorn (Recommended for Linux)

```bash
pip install gunicorn

gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Waitress (Recommended for Windows)

```bash
pip install waitress

waitress-serve --port=8000 config.wsgi:application
```

### Static Files

```bash
python manage.py collectstatic --noinput
```

## Security Checklist

- [ ] Set `DJANGO_DEBUG=False`
- [ ] Set strong `DJANGO_SECRET_KEY`
- [ ] Configure `DJANGO_ALLOWED_HOSTS`
- [ ] Enable HTTPS
- [ ] Set up CORS properly
- [ ] Use production database (PostgreSQL/MySQL)
- [ ] Configure rate limiting
- [ ] Set up logging monitoring
- [ ] Regular security updates

## Database Migration (SQLite → PostgreSQL)

1. Install PostgreSQL adapter:
```bash
pip install psycopg2-binary
```

2. Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

3. Set environment variables:
```env
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Monitoring

Logs are written to `django.log` in the project root. Monitor for:
- Error patterns
- Unusual request volumes
- Performance degradation

## API Rate Limits

- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour

Adjust in `settings.py` under `REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']`.