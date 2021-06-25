# How to RUN
###### first run redis and use celry for send email:
```
python manage.py makemigrations --settings=config.settings.development
python manage.py migrate --settings=config.settings.development
pip install -r requirements.txt
python manage.py runserver --settings=config.settings.development
celery -A config worker -P gevent --loglevel=INFO
celery -A config beat -l info
```