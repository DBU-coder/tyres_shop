from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.signed_cookies import SessionStore
from django.http import HttpRequest
from django.test import TestCase

from cart.cart import Cart
from shop.models import Wheel, Category, Tyre


class TestCartClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Wheels', slug='wheels')
        Category.objects.create(name='Tyres', slug='tyres')
        Wheel.objects.create(
            sku='02548WR',
            name='Test Wheel product 1 V.1',
            slug='test-wheel-product-1-v1',
            brand='Wheel brand',
            price=1200,
            status=1,
            category=Category.objects.get(name='Wheels'),
            stock_qty=10,
            diameter=19,
            width=45.5,
            type=1,
            stripe_product_price_id='test_fake_stripe_id12345'
        )
        Tyre.objects.create(
            sku='RT756029',
            name='Test Tyre product 1 V.1',
            slug='test-tyre-product-1-v1',
            brand='Tyre brand',
            price=800,
            status=1,
            category=Category.objects.get(name='Tyres'),
            stock_qty=10,
            vehicle_type=2,
            profile=45.2,
            season=2,
            diameter=16,
            width=70,
            spikes=False,
            stripe_product_price_id='test_fake_stripe_id12346'
        )

    def setUp(self):
        self.fake_request = HttpRequest()
        self.fake_request.user = AnonymousUser()

        fake_session = SessionStore()
        fake_session.create()
        self.fake_request.session = fake_session

        self.cart = Cart(self.fake_request)
        self.product1 = Wheel.objects.get(pk=1)
        self.product2 = Tyre.objects.get(pk=1)

    def test_add_method(self):
        self.cart.add(self.product1)
        self.cart.add(self.product2)
        self.assertEqual(self.cart.cart_data, {
            'wheel': {'1': {'quantity': 1, 'price': 1200}},
            'tyre': {'1': {'quantity': 1, 'price': 800}}
        })
        self.cart.add(self.product1)
        self.cart.add(
            product=self.product2,
            quantity=7,
            update_quantity=True
        )
        self.assertEqual(self.cart.cart_data, {
            'wheel': {'1': {'quantity': 2, 'price': 1200}},
            'tyre': {'1': {'quantity': 7, 'price': 800}}
        })

    def test_remove_method(self):
        self.cart.add(self.product1)
        self.cart.remove(self.product1)
        self.assertEqual(self.cart.cart_data, {'wheel': {}})

    def test_clear_method(self):
        self.cart.add(self.product2)
        self.cart.clear()
        self.assertEqual(self.fake_request.session.get(settings.CART_SESSION_ID), None)

    def test_get_total_price(self):
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product2, quantity=3)
        self.assertEqual(self.cart.get_total_price(), 4800)

    def test_len_method(self):
        self.cart.add(self.product1, quantity=7)
        self.cart.add(self.product2, quantity=15)
        self.assertEqual(len(self.cart), 22)
