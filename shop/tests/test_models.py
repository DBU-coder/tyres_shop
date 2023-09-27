import datetime

from django.test import TestCase

from shop.models import Tyre, Wheel, HomepageProduct, Category, ProductStatistic


class TestModels(TestCase):

    def setUp(self):
        self.cat_wheels = Category.objects.create(name='Wheels', slug='wheels')
        self.cat_tyres = Category.objects.create(name='Tyres', slug='tyres')
        self.wheel1 = Wheel.objects.create(
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
        self.tyre1 = Tyre.objects.create(
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

    def test_model_name(self):
        self.assertEqual(self.tyre1.model_name, 'tyre')
        self.assertEqual(self.wheel1.model_name, 'wheel')

    def test_get_new_products(self):
        new_products = HomepageProduct.objects.get_new_products('tyre', 'wheel')
        self.assertEqual(new_products[0], self.wheel1)
        self.assertEqual(new_products[1], self.tyre1)

    def test_get_popular_products(self):
        now = datetime.datetime.now()
        ProductStatistic.objects.create(
            content_object=self.wheel1,
            date=(now - datetime.timedelta(days=5)),
            sales_quantity=2
        )
        ProductStatistic.objects.create(
            content_object=self.tyre1,
            date=(now - datetime.timedelta(days=4)),
            sales_quantity=30
        )
        ProductStatistic.objects.create(
            content_object=self.wheel1,
            date=(now - datetime.timedelta(days=3)),
            sales_quantity=5
        )
        ProductStatistic.objects.create(
            content_object=self.tyre1,
            date=(now - datetime.timedelta(days=1)),
            sales_quantity=4
        )
        popular_set1 = HomepageProduct.objects.get_popular_products(days=3)
        self.assertEqual(popular_set1, [self.wheel1, self.tyre1])
        popular_set2 = HomepageProduct.objects.get_popular_products(days=5)
        self.assertEqual(popular_set2, [self.tyre1, self.wheel1])
        popular_set3 = HomepageProduct.objects.get_popular_products()
        self.assertEqual(popular_set3, [])
