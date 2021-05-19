# How to RUN
###### first run redis and:
```
python manage.py makemigrations --settings=config.settings.development
python manage.py migrate --settings=config.settings.development
pip install -r requirements.txt
python manage.py runserver --settings=config.settings.development
```
# for Authorization:
get request to `localhost:8000/api/token/username=mehran password=1234`
and get refresh access token and post request to `localhost:8000/cart/user/`with:
`Authorization Bearer access_token`
# Screen Shots
![ScreenShot](pic/1.jpg)
**http://localhost:8000/list/**
![ScreenShot](pic/2.jpg)
**http://localhost:8000/list/7a1/**
![ScreenShot](pic/3.jpg)
**http://localhost:8000/category/**
![ScreenShot](pic/4.jpg)
**http://localhost:8000/cart/user/**
