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
# Apps

1. [Products](#products)
2. [Cart](#carts)
3. [Payment](#payment)
4. [User](#user)

# Directory
1. [extension](#extension)

# Caching query by:
1. [memcached](#memcached)
2. [database](#database)
3. [filesystem](#filesystem)


# products

* ### **models.py**
#### `formField:`
set field from each category for example:
Mobile phones and shoes have different features
#### `category:`
each product have many category and each category has just one form field
```
    {
        "title": "mobile",
        "slug": "mobile",
        "product_category": "http://localhost:8000/category/mobile/product_category/",
        "status": true,
        "forms_field": [
            "os"
        ],
        "position": 1
    }
```
in product_category, you can See all products in the category.
for more speed request to database use index 'slug'

#### `product:`
products ordering by created and use index 'slug' for more speed,
each product have many category and for Property use **jsonField**,
```
product list
    {
        "url": "http://localhost:8000/product/t-shirt/",
        "slug": "t-shirt",
        "title": "t shirt",
        "thumbnail": "http://localhost:8000/media/images/%D8%AA_UIPlvMd.jpg",
        "price": "0.21",
        "persian_publish": "1 خرداد 1400 , ساعت 11 : 14 "
    },
```
```
product detail
 {
        "title": "t shirt",
        "slug": "t-shirt",
        "seller": 1,
        "description": "color:black",
        "category": [
            {
                "title": "shirt",
                "slug": "shirt",
                "product_category": "http://localhost:8000/category/shirt/product_category/",
                "status": true,
                "forms_field": [
                    "color"
                ],
                "position": 1
            }
        ],
        "thumbnail": "http://localhost:8000/media/images/%D8%AA_UIPlvMd.jpg",
        "images": {},
        "persian_publish": "1 خرداد 1400 , ساعت 11 : 14 ",
        "price": "0.21",
        "status": true,
        "choice": "p"
    }
```
#### `images:`
for product have many image 

* ### **permissions.py**
##### `IsSuperUserOrIsSeller  and  IsSuperUserOrIsSellerProductOrReadOnly:`
for create or update product that each product must change or create by owner product or super user
```
obj.seller == request.user
```
##### `IsSuperUserOrReadonly:`
for create,update,destroy category by superuser and users just can 
show list 

* ### **signals.py**
##### `pre_save_receiver:`
for auto fill slug product by unique_slug_generator() in utils.py
##### `pre_delete_receiver_product  and  pre_delete_receiver_category:`
for use in caching after delete/update product or category
As such cache.delete('category-list') and in the views.py create again cache

# carts
* ### **models.py**
##### `Cart:`
```
list cart:
{
        "detail": "http://localhost:8000/cart/cart/11/",
        "user": 1,
        "subtotal": "1.87",
        "total": 0,
        "timestamp": "2021-05-24T06:20:40.196934Z",
        "updated": "2021-05-24T06:53:00.445960Z"
    }
```
```
detail cart:
{
        "user": 1,
        "cart_item": [
            {
                "url": "http://localhost:8000/cart/cartItem/70/",
                "cart": 11,
                "item": {
                    "url": "http://localhost:8000/product/shirt/",
                    "slug": "shirt",
                    ....
            },
        ],
        "products": [
            {
                "url": "http://localhost:8000/product/shirt/",
                "slug": "shirt",
                ....
            },
        ],
        "subtotal": "1.87",
        ....
    }
```
the function **update_subtotal** run each save or update cart and update subtotal field in cart model 
##### `CartItem:`
there are each cart many cartItem object
```
{
list cartItem:
        "url": "http://localhost:8000/cart/cartItem/70/",
        "cart": 11,
        "item": {
            "url": "http://localhost:8000/product/shirt/",
            "slug": "shirt",
           ....
        },
        "quantity": 4,
         ...
    },
   
```

* ### **permissions.py**
##### `IsSuperUser:`
check use that is he super user? if yes: ok
this permission use when show list all cart 
```
views.py:
def list(self, request):
```
##### `IsSuperUserOrSelfObject:`
if cart object is for **request.user** or user is superuser return true
```
use this permission:
def retrieve(self, request, pk=None):
def destroy(self, request, pk=None):
def create(self, request):
def update(self, request, pk=None):
```  
* ### **signals.py**
use signal for pre_save or pre_delete for change cart object
##### `def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):`
run before save cartItem object and update cartItem for each quantity
that's mean multi quantity with price product and update cartItem
##### `def cart_item_pre_delete_receiver(sender, instance, *args, **kwargs):`
when user delete cartItem, update subtotal price in cart
##### `def cart_item_post_save_receiver(sender, instance, *args, **kwargs):`
when user add cartItem, update subtotal price in cart
and delete cache 
##### `def cart_post_save_receiver(sender, instance, *args, **kwargs):`
for delete cache cart and cartItem for more speed query to database
* ### **views.py**
in views.py, use viewset for api,
and cache by **REDIS** for more speed
```
for example:
    def list(self, request):
        try:
            =======================================
            =           use cache with redis      =
            =        and Django self cache system = 
            =======================================
            obj = cache.get('cartItem-list', None)
            """
                obj=[None,list]
            """
            cart = Cart.objects.all()
            cart_obj = cart.filter(user=request.user).first()
            if obj is None:
                obj = CartItem.objects.all()
                cache.set('cart-list', cart)
                cache.set('cartItem-list', obj)
            query = obj.filter(cart=cart_obj)
            serializer = CartItemListSerializers(query, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)
```
this code show list cartItem for user 
for caching use this functions and for les than code
```
def cacheops(request, name, model):
    obj = cache.get(name, None)
    if obj is None:
        obj = model.objects.all()
        cache.set(name, obj)
    return obj
```
# payment
for payment user and show list carts with **is_pay=True**
just superuser can run it
* ### **views.py**
###### def list(self, request):
for shows carts list with **is_pay=True**
###### def retrieve(self, request, pk=None):
for detail cart 
###### def pay_search(self, request):
search in carts with **is_pay=True**
* query for search:
```
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(products__title__icontains=query) |
            Q(products__title__icontains=query),
            is_pay=True
```

# user
* ### **models.py**
inheritance AbstractUser for add custom field
```
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    is_seller=models.BooleanField(default=False,verbose_name='آیا کاربر فروشنده است')
```
password reset and register by email, then email is be different

* ### **admin.py**
by **UserAdmin.fieldsets[2][1]['fields']**, put Special field(email,is_seller)  in the desired places

* ### **serializers.py**
######`UserListSerializers:`
for list user and Has fields (email,detail,is_seller,username)
 
######`UserDetailSerializers:`
all detail user for super user

* ### **views.py**
show list and detail user information by caching for superuser
```
    def list(self, request):
        obj = cacheops(request, 'user-list', User)
        serializer = UserListSerializers(obj, context={'request': request}, many=True)
        return Response(serializer.data)
```
for Registration user by jwt show list with Low access for change data 
```
http://localhost:8000/api/rest-auth/user/
```
for use jwt:
```
https://www.rootstrap.com/blog/registration-and-authentication-in-django-apps-with-dj-rest-auth/
https://dev.to/jkaylight/django-rest-framework-authentication-with-dj-rest-auth-4kli
```

# extension
* ### **utils.py**
there are two function:
```
def jalaly_converter(time):
def cacheops(request, name, model):
```
`jalaly_converter:`
###### this function convert Miladi date for jalali date
for example : **2021-05-23** ==========> **2 خرداد 1400 , ساعت 40 : 20**

`cacheops:`
###### use cache in views.py for Low code

# memcached
##### use way **cache-Aside**: in this way first request to cache if exist information read it but if not exist, request to database and read query  
###### caching cart object in to memcached. memcached key must less than 500 Kb and value must less than 1 MB
###### any cart cache in memcached with ``cart-{user.email}``that is mean all carts caching that user create
even carts that ``is_pay=True``
```
{
'cart-m.kamrani1421@gmail.com':[
                                cart1,
                                cart2,...
                               ],
...
}
```
# database
###### caching products in database because products change less.
###### use **Read-Through cache**: in this way database and cache are aligned and request all time sending to cache other than first time
```
CACHES = {
    'products': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'items',
    }
}
```
# filesystem
###### caching cartItem 
###### low security
###### suitable for trivial data
```
CACHES = {
    'cartItems': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'd:/cartItem',
    },
}
```
