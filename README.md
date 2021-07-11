<<<<<<< HEAD
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
=======
# Directory
1. [extension](#extension)

# Performance
1. [django-silk](#django-silk)

# extension
* ### **productCacheDatabase**
### cache inside database:
##### for search product and list product
`
    caches['all_products'].set(name, obj)
`
* ### **cacheDetailProduct**
###### caching into redis detail product
`
obj = model.objects.get(slug=slug, status=True, choice='p')
`

* ### **cacheCategoryOrFigur**
###### cache all category and figur field into redis
###### Because they are less than 512 MB
`cache.set(name, obj)`


* ### **cacheCart**
`cache.set(f"cart_{user.email}", obj)`

* ### **cacheCartItem**
###### caching cartItems for each cart to redis
```
     obj = model.objects.filter(cart=cart)
     cache.set(name, obj)
```

# django-silk
* ### **list products**
###### /product/
###### 164ms overall
###### 8ms on querie

* ### **detail products**
###### /product/apple/
###### 164ms overall
###### 22ms on queries

* ### **list category**
###### /category/
###### 149ms overall
###### 9ms on queries

* ### **detail category**
###### /category/mobile/
###### 145ms overall
###### 15ms on queries

* ### **list cartItem**
###### /cart/cartItem/
###### 178ms overall
###### 22ms on queries

* ### **detail cartItem**
###### /cart/cartItem/6/
###### 194ms overall
###### 38ms on queries

* ### **list cart**
###### /cart/cart/
###### 174ms overall
###### 12ms on queries

* ### **detail cart**
###### /cart/cart/3/
###### 189ms overall
###### 26ms on queries
>>>>>>> rediscache
