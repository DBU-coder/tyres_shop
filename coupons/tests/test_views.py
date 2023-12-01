from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from coupons.models import Coupon


class TestCouponView(TestCase):
    viewname = 'coupons:apply'

    def setUp(self):
        self.client = Client()
        self.test_coupon = Coupon.objects.create(
            code='winter30',
            valid_from=timezone.now(),
            valid_to=(timezone.now() + timedelta(days=10)),
            discount=30,
            active=True,
        )

    def test_coupon_apply_redirect(self):
        response = self.client.post(
            path=reverse(self.viewname),
            data={'code': 'WinTer30'},
            HTTP_REFERER=reverse('cart:detail')
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_coupon_valid(self):
        self.client.post(
            path=reverse(self.viewname),
            data={'code': 'WinTer30'},
            HTTP_REFERER=reverse('cart:detail')
        )
        coupon_id = self.client.session['coupon_id']
        self.assertEqual(coupon_id, self.test_coupon.id)

    def test_coupon_invalid(self):
        self.client.post(
            path=reverse(self.viewname),
            data={'code': 'summer10'},
            HTTP_REFERER=reverse('cart:detail')
        )
        coupon_id = self.client.session['coupon_id']
        self.assertIsNone(coupon_id)
