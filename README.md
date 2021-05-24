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
4. [User](#philosophy)

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
            {
                "url": "http://localhost:8000/cart/cartItem/71/",
                "cart": 11,
                "item": {
                    "url": "http://localhost:8000/product/shirt/",
                    "slug": "shirt",
                   ....
            }
        ],
        "products": [
            {
                "url": "http://localhost:8000/product/shirt/",
                "slug": "shirt",
                ....
            },
            {
                "url": "http://localhost:8000/product/shirt/",
                "slug": "shirt",
                ....
            }
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
            "title": "shirt",
           ....
        },
        "quantity": 4,
        "line_item_total": "0.44"
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
##### `views.py:`
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
