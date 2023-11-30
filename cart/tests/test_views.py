from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse


class TestCartView(TestCase):

    fixtures = ['shop/fixtures/shop_data_fixtures.json']

    def setUp(self):
        self.client = Client()
        self.client.login(email='test_user1@example.com', password='Test9PassworD')

    def test_add_to_cart(self):
        """Test adding and updating products to cart"""
        viewname = 'cart:add'
        response = self.client.post(
            path=reverse(viewname, kwargs={'slug': 'test-tyre-product-1'}),
            data={'quantity': 2, 'update': False}
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.post(
            path=reverse(viewname, kwargs={'slug': 'goodyear-18560r14-82h-efficientgrip-performance'}),
            data={'quantity': 3, 'update': False}
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.post(
            path=reverse(viewname, kwargs={'slug': 'goodyear-18560r14-82h-efficientgrip-performance'}),
            data={'quantity': 1, 'update': True}
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_cart_detail(self):
        response = self.client.get(path=reverse('cart:detail'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
