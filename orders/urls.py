from django.urls import path

from orders.views import *


app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('list/', OrdersListView.as_view(), name='order_list'),
    path('details/<int:order_id>/', OrderDetailsView.as_view(), name='order_details'),
    path('shipping/<int:order_id>/', ShippingChoiceView.as_view(), name='order_shipping'),
    path('admin/order/<int:order_id>/', admin_order_details, name='admin_order_details'),

    # path('order-canceled/', CancelView.as_view(), name='order_canceled'),
    # path('order-created/', SuccessView.as_view(), name='order_success'),
    # path('admin/order/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
]

