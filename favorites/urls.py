from django.urls import path

from favorites.views import AddToFavoritesView, FavoritesListView, RemoveFromFavoritesView


app_name = 'favorites'

urlpatterns = [
    path('', FavoritesListView.as_view(), name='list'),
    path('add/<str:ct_model>/<int:pk>', AddToFavoritesView.as_view(), name='add'),
    path('remove/<str:ct_model>/<int:pk>', RemoveFromFavoritesView.as_view(), name='remove'),
]

