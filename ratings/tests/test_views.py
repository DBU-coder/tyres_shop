import json
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from ratings.models import Rating
from shop.models import Product


class TestRatingsViews(TestCase):
    fixtures = ['shop/fixtures/shop_data_fixtures.json']

    @classmethod
    def setUpTestData(cls):
        Customer.objects.create(email='test_user1@example.com', password='Test9PassworD')

    def setUp(self):
        self.user = Customer.objects.first()
        self.product = Product.objects.first()
        Rating.objects.create(
            ip='125.86.0.1',
            product=self.product,
            value=3
        )
        self.test_data = {
            'user_rating': 1,
            'product_id': self.product.id
        }

    def test_access(self):
        response = self.client.post(reverse('ratings:set_rating'),
                                    data=json.dumps(self.test_data),
                                    content_type='application/json',
                                    )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_set_rating(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('ratings:set_rating'),
                                    data=json.dumps(self.test_data),
                                    content_type='application/json',
                                    )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        rating = self.product.ratings.last()
        self.assertEqual(rating.value, 1)
