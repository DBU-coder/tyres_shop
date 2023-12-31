from django.urls import path

from cart.views import CartDetailView, AddToCartView, RemoveFromCartView, clear_cart


app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='detail'),
    path('add/<slug:slug>/', AddToCartView.as_view(), name='add'),
    path('remove/<slug:slug>/', RemoveFromCartView.as_view(), name='remove'),
    path('clear/', clear_cart, name='clear'),
]
