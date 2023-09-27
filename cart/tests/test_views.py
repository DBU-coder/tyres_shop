from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse

from shop.models import Category, Wheel, Tyre


class TestCartView(TestCase):
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
        self.client = Client()
        self.client.login(email='test_user1@example.com', password='Test9PassworD')

    def test_add_to_cart(self):
        """Test adding and updating products to cart"""
        viewname = 'cart:add'
        response = self.client.post(
            path=reverse(viewname, kwargs={'ct_model': 'wheel', 'slug': 'test-wheel-product-1-v1'}),
            data={'quantity': 2, 'update': False}
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.post(
            path=reverse(viewname, kwargs={'ct_model': 'tyre', 'slug': 'test-tyre-product-1-v1'}),
            data={'quantity': 3, 'update': False}
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.post(
            path=reverse(viewname, kwargs={'ct_model': 'tyre', 'slug': 'test-tyre-product-1-v1'}),
            data={'quantity': 1, 'update': True}
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_cart_detail(self):
        response = self.client.get(path=reverse('cart:detail'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
