from django.urls import path

from orders.views import OrderDetailsView, OrderCreateView, OrdersListView, admin_order_details, OrderDeleteView, \
    SuccessView, CancelView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('list/', OrdersListView.as_view(), name='order_list'),
    path('details/<int:order_id>/', OrderDetailsView.as_view(), name='order_details'),
    path('admin/order/<int:order_id>/', admin_order_details, name='admin_order_details'),
    path('<pk>/delete/', OrderDeleteView.as_view(), name='delete'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel')
]

