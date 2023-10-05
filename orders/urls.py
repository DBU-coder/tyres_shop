from django.urls import path

from orders.views import OrderDetailsView, OrderCreateView, OrdersListView, ShippingChoiceView, admin_order_details, \
    OrderDeleteView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('list/', OrdersListView.as_view(), name='order_list'),
    path('details/<int:order_id>/', OrderDetailsView.as_view(), name='order_details'),
    path('shipping/<int:order_id>/', ShippingChoiceView.as_view(), name='order_shipping'),
    path('admin/order/<int:order_id>/', admin_order_details, name='admin_order_details'),
    path('<pk>/delete/', OrderDeleteView.as_view(), name='delete'),
]

