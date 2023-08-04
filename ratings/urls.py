from django.urls import path

from ratings.views import SetRatingView


app_name = 'ratings'

urlpatterns = [
    path('set_rating/', SetRatingView.as_view(), name='set_rating'),
]