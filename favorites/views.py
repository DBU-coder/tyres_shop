from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from favorites.utils import Favorite


class AddToFavoritesView(View):
    product = None
    favorites = None

    def dispatch(self, request, *args, **kwargs):
        self.favorites = Favorite(request)
        content_type = ContentType.objects.get(model=kwargs.get('ct_model'))
        self.product = content_type.model_class().objects.get(pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.favorites.add(self.product)
        return redirect(self.request.META.get('HTTP_REFERER'))


class FavoritesListView(TemplateView):
    template_name = 'favorites/favorites_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RemoveFromFavoritesView(View):
    pass
