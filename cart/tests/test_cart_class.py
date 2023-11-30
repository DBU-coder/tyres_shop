from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.signed_cookies import SessionStore
from django.http import HttpRequest
from django.test import TestCase

from cart.cart import Cart
from shop.models import Product


class TestCartClass(TestCase):
    fixtures = ['shop/fixtures/shop_data_fixtures.json']

    def setUp(self):
        self.fake_request = HttpRequest()
        self.fake_request.user = AnonymousUser()

        fake_session = SessionStore()
        fake_session.create()
        self.fake_request.session = fake_session

        self.cart = Cart(self.fake_request)
        self.product1 = Product.objects.get(pk=5)
        self.product2 = Product.objects.get(pk=6)

    def test_add_method(self):
        self.cart.add(self.product1)
        self.cart.add(self.product2)
        self.assertEqual(self.cart.cart_data, {
            '5': {'quantity': 1, 'price': '36.72'},
            '6': {'quantity': 1, 'price': '89.34'}
        })
        self.cart.add(self.product1)
        self.cart.add(
            product=self.product2,
            quantity=7,
            update_quantity=True
        )
        self.assertEqual(self.cart.cart_data, {
            '5': {'quantity': 2, 'price': '36.72'},
            '6': {'quantity': 7, 'price': '89.34'}
        })

    def test_remove_method(self):
        self.cart.add(self.product1)
        self.cart.remove(self.product1)
        self.assertEqual(self.cart.cart_data, {})

    def test_clear_method(self):
        self.cart.add(self.product2)
        self.cart.clear()
        self.assertEqual(self.fake_request.session.get(settings.CART_SESSION_ID), None)

    def test_get_total_price(self):
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product2, quantity=3)
        self.assertEqual(self.cart.get_total_price(), Decimal('341.46'))

    def test_len_method(self):
        self.cart.add(self.product1, quantity=7)
        self.cart.add(self.product2, quantity=15)
        self.assertEqual(len(self.cart), 22)
