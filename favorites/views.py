from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _

from favorites.utils import Favorite
from shop.models import Product


class AddToFavoritesView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('id')
        favorites = Favorite(request)
        favorites.add(product_id)
        response_data = {
            'id': request.POST.get('id'),
        }
        return JsonResponse(data=response_data)


class RemoveFromFavoritesView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('id')
        favorites = Favorite(request)
        favorites.remove(product_id)
        response_data = {
            'id': request.POST.get('id'),
        }
        return JsonResponse(data=response_data)


class FavoritesView(ListView):
    template_name = 'favorites/favorites_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        favorites = self.request.session.get('favorites')
        queryset = Product.objects.filter(id__in=favorites). \
            select_related('category').prefetch_related('images', 'ratings').annotate(
            avg_rating=Avg('ratings__value'),
            users_count=Count('ratings__ip')
        ).only('category', 'ratings', 'images', 'name', 'price', 'slug', 'status')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Shop|Favorites')
        return context


def favorites_api(request):
    """Sends actual favorites to JS."""
    return JsonResponse(request.session.get('favorites'), safe=False)
