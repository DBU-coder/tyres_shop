from http import HTTPStatus

from django import forms
from django.conf import settings
from django.db.models import Q
from django.test import TestCase, override_settings
from django.urls import reverse

from ratings.models import Rating
from shop.filters import TyreFilter, WheelFilter
from shop.models import ProductStatistic, Product


class TestShopViews(TestCase):
    fixtures = ['shop/fixtures/shop_data_fixtures.json']

    def setUp(self):
        self.test_product1 = Product.objects.get(id=7)
        self.test_product2 = Product.objects.get(id=8)
        ProductStatistic.objects.create(
            product=self.test_product1,
            purchases_quantity=10
        )
        ProductStatistic.objects.create(
            product=self.test_product2,
            purchases_quantity=25
        )
        Rating.objects.create(
            ip='125.86.0.1',
            product=self.test_product1,
            value=5
        )
        Rating.objects.create(
            ip='125.86.0.2',
            product=self.test_product1,
            value=4
        )

    def test_shop_correct_templates(self):
        templates_urls = {
            'shop/index.html': reverse('shop:index'),
            'shop/search_results.html': reverse('shop:search'),
            'shop/delivery_detail.html': reverse('shop:delivery'),
            'shop/about_us.html': reverse('shop:about'),
            'shop/contact_us.html': reverse('shop:contacts'),
            'shop/category_products.html': reverse('shop:category_products', kwargs={'slug': 'tyres'}),
            'shop/product_detail.html': (
                reverse('shop:product_detail', kwargs={'slug': 'funtoma-roadfun-20565-r15-94v'})
            ),
        }
        for template, url in templates_urls.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    @override_settings(CACHES=settings.TEST_CACHES)
    def test_index_correct_context(self):
        response = self.client.get(reverse('shop:index'))
        new_products = response.context.get('new_products')
        self.assertQuerySetEqual(new_products, Product.objects.order_by('-created')[:len(new_products)])
        popular_products = response.context.get('popular_products')
        self.assertQuerySetEqual(popular_products, [self.test_product2, self.test_product1])

    @override_settings(CACHES=settings.TEST_CACHES)
    def test_search_queryset(self):
        url = reverse('shop:search')
        response = self.client.get(url, data={'cat': 1, 'q': 'roadfun'})
        self.assertSequenceEqual(response.context['products'], [self.test_product1])
        response = self.client.get(url, data={'cat': '', 'q': 'test product'})
        self.assertSequenceEqual(response.context['products'], [self.test_product2])
        response = self.client.get(url, data={'cat': '', 'q': 'test'})
        self.assertQuerySetEqual(response.context['products'],
                                 Product.objects.filter(Q(name__icontains='test') | Q(description__icontains='test')),
                                 ordered=False
                                 )

    def test_has_avg_rating(self):
        response = self.client.get(reverse('shop:category_products', kwargs={'slug': 'tyres'}))
        product = response.context['products'][1]
        self.assertEqual(product.avg_rating, 4.5)
        self.assertEqual(product.users_count, 2)
        self.assertIsInstance(product, Product)

    def test_category_products_paginator(self):
        response = self.client.get(
            reverse('shop:category_products', kwargs={'slug': 'tyres'}),
            data={'paginate_by': 3, 'page': 2})
        self.assertEqual(len(response.context['products']), 2)

    def test_category_products_filter(self):
        cat_filters = {
            'tyres': TyreFilter,
            'wheels': WheelFilter
        }
        for cat_name, expected_filter in cat_filters.items():
            with self.subTest(cat_name=cat_name):
                response = self.client.get(reverse('shop:category_products', kwargs={'slug': cat_name}))
                view_filter = response.context['filter']
                self.assertIsInstance(view_filter, expected_filter)

    def test_product_detail_context(self):
        response = self.client.get(
            reverse('shop:product_detail', kwargs={'slug': 'goodyear-18560r14-82h-efficientgrip-performance'})
        )
        form_fields = {
            'quantity': forms.fields.TypedChoiceField,
            'update': forms.fields.BooleanField
        }
        for field_name, expected_field in form_fields.items():
            with self.subTest(field_name=field_name):
                form_field = response.context['form'].declared_fields.get(field_name)
                self.assertIsInstance(form_field, expected_field)
