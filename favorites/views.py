import json

from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

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


class FavoritesView(TemplateView):
    template_name = 'favorites/favorites_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def favorites_api(request):
    """Sends actual favorites to JS."""
    return JsonResponse(request.session.get('favorites'), safe=False)
