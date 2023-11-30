from django.core.exceptions import ValidationError
from django.test import TestCase

from ratings.models import Rating
from shop.models import Product


class TestModels(TestCase):
    fixtures = ['shop/fixtures/shop_data_fixtures.json']

    def setUp(self):
        self.product = Product.objects.first()

    def test_validators(self):
        for i in (7, -1):
            with self.assertRaises(ValidationError, msg=f'Rating value:{i} not raised exception.'):
                rating = Rating.objects.create(
                    ip='125.86.0.15',
                    product=self.product,
                    value=i
                )
                rating.full_clean()
