# Directory
1. [extension](#extension)

# Performance
1. [django-silk](#django-silk)

# extension
* ### **cacheProduct**
```
    obj = caches['products'].get(name, None)
    if obj is None:
        obj = model.objects.all()
        caches['products'].set(name, obj)
    return obj
```
###### cache inside database
* ### **cacheCart**
`
cache.set(f"cart-{user.email}", obj)
`
###### caching into memcached cart

* ### **cacheCartItem**
`caches['cartItems'].set(name, obj)`
###### cache cartItem in to filesystem


# django-silk
* ### **list products**
###### /product/
###### 144ms overall
###### 13ms on queries

* ### **detail products**
###### /product/apple/
###### 173ms overall
###### 27ms on queries

* ### **list category**
###### /category/
###### 125ms overall
###### 8ms on queries

* ### **detail category**
###### /category/mobile/
###### 137ms overall
###### 13ms on queries

* ### **list cartItem**
###### /cart/cartItem/
###### 155ms overall
###### 21ms on queries

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