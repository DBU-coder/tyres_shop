from http import HTTPStatus

from django import forms
from django.test import TestCase
from django.urls import reverse

from ratings.models import Rating
from shop.filters import TyreFilter, WheelFilter
from shop.models import Category, Wheel, Tyre, ProductStatistic


class TestShopViews(TestCase):

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
            stripe_product_price_id='test_fake_stripe_id12346',
            description='This is example description for testing.'
        )

    def setUp(self):
        self.wheel_product = Wheel.objects.first()
        self.tyre_product = Tyre.objects.first()
        ProductStatistic.objects.create(
            content_object=self.wheel_product,
            sales_quantity=10
        )
        ProductStatistic.objects.create(
            content_object=self.tyre_product,
            sales_quantity=25
        )
        Rating.objects.create(
            ip='125.86.0.1',
            content_object=self.wheel_product,
            value=5
        )
        Rating.objects.create(
            ip='125.86.0.2',
            content_object=self.wheel_product,
            value=4
        )

    @staticmethod
    def set_test_data_for_pagination(quantity=15):
        for i in range(quantity):
            Tyre.objects.create(
                sku=f'RT756029{i}',
                name=f'Test Tyre product {i}',
                slug=f'test-tyre-product-{i}',
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
                stripe_product_price_id=f'test_fake_stripe_id1234{i}',
                description='This is example description for testing.'
            )
            i += 1

    def test_shop_correct_templates(self):
        templates_urls = {
            'shop/index.html': reverse('shop:index'),
            'shop/search_results.html': reverse('shop:search'),
            'shop/delivery_detail.html': reverse('shop:delivery'),
            'shop/about_us.html': reverse('shop:about'),
            'shop/contact_us.html': reverse('shop:contacts'),
            'shop/category_products.html': reverse('shop:category_products', kwargs={'cat_name': 'wheels'}),
            'shop/product_detail.html': (
                reverse('shop:product_detail', kwargs={'ct_model': 'tyre', 'slug': 'test-tyre-product-1-v1'})
            ),
        }
        for template, url in templates_urls.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_index_correct_context(self):
        response = self.client.get(reverse('shop:index'))
        new_products = response.context.get('new_products')
        self.assertSequenceEqual(new_products, [self.wheel_product, self.tyre_product])
        popular_products = response.context.get('popular_products')
        self.assertSequenceEqual(popular_products, [self.tyre_product, self.wheel_product])

    def test_search_queryset(self):
        url = reverse('shop:search')
        response = self.client.get(url, data={'cat': 'wheel', 'q': 'Wheel'})
        self.assertSequenceEqual(response.context['products'], [self.wheel_product])
        response = self.client.get(url, data={'cat': 'all', 'q': 'example'})
        self.assertSequenceEqual(response.context['products'], [self.tyre_product])
        response = self.client.get(url, data={'cat': 'all', 'q': 'product'})
        self.assertSequenceEqual(response.context['products'], [self.tyre_product, self.wheel_product])

    def test_has_avg_rating(self):
        response = self.client.get(reverse('shop:category_products', kwargs={'cat_name': 'wheels'}))
        product = response.context['products'][0]
        self.assertEqual(product.avg_rating, 4.5)
        self.assertEqual(product.users_count, 2)
        self.assertIsInstance(product, Wheel)

    def test_category_products_paginator(self):
        self.set_test_data_for_pagination()
        response = self.client.get(
            reverse('shop:category_products', kwargs={'cat_name': 'tyres'}),
            data={'paginate_by': 10, 'page': 2})
        self.assertEqual(len(response.context['products']), 6)

    def test_category_products_filter(self):
        cat_filters = {
            'tyres': TyreFilter,
            'wheels': WheelFilter
        }
        for cat_name, expected_filter in cat_filters.items():
            with self.subTest(cat_name=cat_name):
                response = self.client.get(reverse('shop:category_products', kwargs={'cat_name': cat_name}))
                view_filter = response.context['filter']
                self.assertIsInstance(view_filter, expected_filter)

    def test_product_detail_context(self):
        response = self.client.get(
            reverse('shop:product_detail', kwargs={'ct_model': 'tyre', 'slug': 'test-tyre-product-1-v1'})
        )
        form_fields = {
            'quantity': forms.fields.TypedChoiceField,
            'update': forms.fields.BooleanField
        }
        for field_name, expected_field in form_fields.items():
            with self.subTest(field_name=field_name):
                form_field = response.context['form'].declared_fields.get(field_name)
                self.assertIsInstance(form_field, expected_field)
