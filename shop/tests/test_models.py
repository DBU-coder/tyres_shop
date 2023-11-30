from django.conf import settings
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.utils import timezone

from shop.models import HomepageProduct, ProductStatistic, Product


class TestModels(TestCase):
    fixtures = ['shop/fixtures/shop_data_fixtures.json']

    def setUp(self):
        self.products = Product.objects.order_by('-created')
        self.test_product1 = Product.objects.get(pk=5)
        self.test_product2 = Product.objects.get(pk=6)

    def tearDown(self):
        cache.clear()

    def test_get_new_products(self):
        new_products = HomepageProduct.objects.get_new_products(quantity=4)
        self.assertEqual(new_products[0], self.products[0])
        self.assertEqual(new_products[3], self.products[3])

    @override_settings(CACHES=settings.TEST_CACHES)
    def test_get_popular_products(self):
        now = timezone.now()
        ProductStatistic.objects.create(
            product=self.test_product1,
            date=(now - timezone.timedelta(days=5)),
            purchases_quantity=2
        )
        ProductStatistic.objects.create(
            product=self.test_product2,
            date=(now - timezone.timedelta(days=4)),
            purchases_quantity=30
        )
        ProductStatistic.objects.create(
            product=self.test_product1,
            date=(now - timezone.timedelta(days=3)),
            purchases_quantity=5
        )
        ProductStatistic.objects.create(
            product=self.test_product2,
            date=(now - timezone.timedelta(days=1)),
            purchases_quantity=4
        )
        popular_set1 = HomepageProduct.objects.get_popular_products(days=3)
        self.assertQuerySetEqual(popular_set1, [self.test_product1, self.test_product2])
        popular_set2 = HomepageProduct.objects.get_popular_products(days=5)
        self.assertQuerySetEqual(popular_set2, [self.test_product2, self.test_product1])
        popular_set3 = HomepageProduct.objects.get_popular_products()
        self.assertQuerySetEqual(popular_set3, [])
