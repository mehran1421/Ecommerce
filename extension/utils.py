import random
import string
from . import jalali
from django.utils import timezone
from django.core.cache import caches, cache
from django.utils.text import slugify


def persian_number_converter(mystr):
    # در محیطی که اعداد فارسی را پشتیبانی کند کار میکند
    numbers = {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
    }
    for e, p in numbers.items():
        mystr = mystr.replace(e, p)

    return mystr


def jalaly_converter(time):
    jmonth = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند", ]
    time = timezone.localtime(time)
    time_to_string = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_string).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = "{} {} {} , ساعت {} : {} ".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        time.minute,
        time.hour,
    )
    return persian_number_converter(output)


def cacheProduct(request, name, model):
    """
    cache products,category,figureField in database
    for products ===> name='products'
    for category ===> name='category'
    for figure ===> name='figure'
    :param request:
    :param name:
    :param model:
    :return:
    """
    obj = caches['products'].get(name, None)
    if obj is None:
        obj = model.objects.all()
        caches['products'].set(name, obj)
    return obj


def cacheCart(request, name, model, user):
    """
    cache cart object in memcached
    for example:
    {
            'cart-m.kamrani1421@gmail.com':[object1,object2,...],
            ...
    }
    :param request:
    :param name:
    :param model:
    :param user:
    :return:
    """
    obj = cache.get(name, None)
    print(obj)
    print("-------------")
    if obj is None:
        obj = model.objects.filter(user=user)
        cache.set(f"cart_{user.email}", obj)
    return obj


def cacheCartItem(request, name, model):
    """
    caching in the fileSystem
    security is loss ===> change in cartItem cant change cart objects that is_pay=True
    :param request:
    :param name:
    :param model:
    :return:
    """
    obj = caches['cartItems'].get(name, None)
    if obj is None:
        obj = model.objects.all()
        caches['cartItems'].set(name, obj)
    return obj


'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
