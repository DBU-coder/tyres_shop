from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from orders.views import StripeWebhookView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('accounts/', include('allauth.urls')),  # Allauth
    path('shop/', include('shop.urls', namespace='shop')),
    path('customers/', include('customers.urls', namespace='customers')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('ratings/', include('ratings.urls', namespace='ratings')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('webhooks/stripe/', StripeWebhookView.as_view(), name='stripe_webhook')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
