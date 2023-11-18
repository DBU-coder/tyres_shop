from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from orders.views import StripeWebhookView
from shop.views import get_specifications


urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('ratings/', include('ratings.urls', namespace='ratings')),
    path('webhooks/stripe/', StripeWebhookView.as_view(), name='stripe_webhook'),
    path('get_specifications/<int:product_type_id>/', get_specifications, name='get_specifications'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('i18n/', include("django.conf.urls.i18n")),
    path('customers/', include('customers.urls', namespace='customers')),
    path('accounts/', include('allauth.urls')),  # Allauth
    path('shop/', include('shop.urls', namespace='shop')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('favorites/', include('favorites.urls', namespace='favorites')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
