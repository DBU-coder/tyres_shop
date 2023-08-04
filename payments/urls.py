from django.urls import path

from payments.views import *

app_name = 'payments'

urlpatterns = [
    path('create_payment/<int:order_id>/', CreatePaymentView.as_view(), name='create'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]
