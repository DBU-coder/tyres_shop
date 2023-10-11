from django.urls import path

from favorites.views import AddToFavoritesView, FavoritesView, RemoveFromFavoritesView, favorites_api

app_name = 'favorites'

urlpatterns = [
    path('', FavoritesView.as_view(), name='list'),
    path('add/', AddToFavoritesView.as_view(), name='add'),
    path('remove/', RemoveFromFavoritesView.as_view(), name='remove'),
    path('api/', favorites_api, name='api'),
]

