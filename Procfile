release: python manage.py migrate --noinput && python manage.py check --deploy --fail-level ERROR
web: gunicorn planex.app.wsgi
worker: celery worker --events --app=planex.app.celery.app --loglevel=debug
