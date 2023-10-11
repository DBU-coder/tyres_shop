
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView, ListView

from favorites.utils import Favorite


class AddToFavoritesView(View):
    def post(self, request, *args, **kwargs):
        product_type = request.POST.get('type')
        product_id = request.POST.get('id')
        favorites = Favorite(request)
        favorites.add(product_type, product_id)
        response_data = {
            'type': request.POST.get('type'),
            'id': request.POST.get('id'),
        }
        return JsonResponse(data=response_data)


class RemoveFromFavoritesView(View):
    def post(self, request, *args, **kwargs):
        product_type = request.POST.get('type')
        product_id = request.POST.get('id')
        favorites = Favorite(request)
        favorites.remove(product_type, product_id)
        response_data = {
            'type': request.POST.get('type'),
            'id': request.POST.get('id'),
        }
        return JsonResponse(data=response_data)


class FavoritesView(ListView):
    template_name = 'favorites/favorites_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        favorites = self.request.session.get('favorites')
        queryset = []
        if favorites:
            for key, value in favorites.items():
                ct_model = ContentType.objects.get(model=key)
                products = ct_model.model_class().objects.filter(id__in=value).\
                    select_related('category').prefetch_related('gallery', 'ratings').annotate(
                    avg_rating=Avg('ratings__value'),
                    users_count=Count('ratings__ip')
                ).only('category', 'ratings', 'gallery', 'name', 'price', 'slug', 'status')
                queryset.extend(products)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop|Favorites'
        return context


def favorites_api(request):
    """Sends actual favorites to JS."""
    return JsonResponse(request.session.get('favorites'), safe=False)
