from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from coupons.models import Coupon


class TestCouponModel(TestCase):
    def test_validators(self):
        coupons_data = {'Summer35': -35, 'Fall225': 225}
        for code, discount in coupons_data.items():
            with self.assertRaises(ValidationError, msg=f'Coupon discount:{discount} not raised exception.'):
                coupon = Coupon.objects.create(
                    code=code,
                    valid_from=timezone.now(),
                    valid_to=(timezone.now() + timedelta(days=10)),
                    discount=discount,
                    active=True
                )
                coupon.full_clean()
