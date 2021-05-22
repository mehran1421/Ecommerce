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
3. [Payment](#programming)
4. [User](#philosophy)

# products

* ### **models.py**
####formField:
set field from each category for example:
Mobile phones and shoes have different features
####category:
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

####product:
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
####images:
for product have many image 

* ### **permissions.py**
#####IsSuperUserOrIsSeller  and  IsSuperUserOrIsSellerProductOrReadOnly:
for create or update product that each product must change or create by owner product or super user
```
obj.seller == request.user
```
#####IsSuperUserOrReadonly:
for create,update,destroy category by superuser and users just can 
show list 

* ### **signals.py**
#####pre_save_receiver:
for auto fill slug product by `unique_slug_generator()` in utils.py
#####pre_delete_receiver_product  and  pre_delete_receiver_category:
for use in caching after delete/update product or category
As such `cache.delete('category-list')` and in the views.py create again cache

