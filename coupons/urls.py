from django.urls import path
from coupons.views import CouponApplyView


app_name = 'coupons'

urlpatterns = [
    path('apply/', CouponApplyView.as_view(), name='apply'),
]
