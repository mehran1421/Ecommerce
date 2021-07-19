from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from items.models import Product, Category
from carts.models import CartItem, Cart
from notices.models import Notice
from ticketing.models import Ticket, QuestionAndAnswer


class BaseTest(APITestCase):
    """
    Base test case
    """
    client = APIClient
    token = ''

    def setUp(self):
        """
        setup test data
        """
        self.client.post('/api/rest-auth/registration/', data={
            'username': 'mehran', 'email': 'm.dlfjs@gmail.com', 'password1': 'mehran1421', 'password2': 'mehran1421'
        })
        self.user = get_user_model().objects.get(username='mehran')

        self.cat = Category.objects.create(title='mobile', slug='mobile', status=True, position=1)
        self.product = Product.objects.create(title='samsung j7', description='android app', seller=self.user,
                                              price=1.54,
                                              thumbnail="/media/images/1_d3HHH29.jpg")
        self.product.category.set([self.cat])
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, item=self.product, quantity=5)

        self.notice = Notice.objects.create(email='m.ka@gmail.com')
        self.ticket = Ticket.objects.create(title='please check my payment', status='de', user=self.user)
        self.qa = QuestionAndAnswer.objects.create(description='hello', question=self.ticket, user=self.user)
