import json
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from ratings.models import Rating
from shop.models import Category, Wheel


class TestRatingsViews(TestCase):
    url_name = 'ratings:set_rating'

    @classmethod
    def setUpTestData(cls):
        Customer.objects.create(email='user1@example.com', password='SimpleTestPassword')
        Category.objects.create(name='Wheels', slug='wheels')
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

    def setUp(self):
        self.user = Customer.objects.get(pk=1)
        self.wheel_product = Wheel.objects.first()
        Rating.objects.create(
            ip='125.86.0.1',
            content_object=self.wheel_product,
            value=3
        )
        self.test_data = {
            'user_rating': 1,
            'product_model': 'wheel',
            'product_id': self.wheel_product.id
        }

    def test_access(self):
        response = self.client.post(reverse(self.url_name),
                                    data=json.dumps(self.test_data),
                                    content_type='application/json',
                                    )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_set_rating(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse(self.url_name),
                                    data=json.dumps(self.test_data),
                                    content_type='application/json',
                                    )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        rating = self.wheel_product.ratings.last()
        self.assertEqual(rating.value, 1)
