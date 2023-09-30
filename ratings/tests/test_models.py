from django.core.exceptions import ValidationError
from django.test import TestCase

from ratings.models import Rating
from shop.models import Tyre, Wheel, Category


class TestModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Tyres', slug='tyres')
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
            stripe_product_price_id='test_fake_stripe_id12346',
            description='This is example description for testing search.'
        )

    def setUp(self):
        self.tyre_product = Tyre.objects.first()

    def test_validators(self):
        for i in (7, -1):
            with self.assertRaises(ValidationError, msg=f'Rating value:{i} not raised exception.'):
                rating = Rating.objects.create(
                    ip='125.86.0.15',
                    content_object=self.tyre_product,
                    value=i
                )
                rating.full_clean()
