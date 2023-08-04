from django.urls import path
from .views import *


app_name = 'customers'

urlpatterns = [
    path('profile/<int:pk>/dashboard/', ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/details/', CustomerUpdateView.as_view(), name='details'),
    path('profile/<int:pk>/change-password/', CustomerChangePassword.as_view(), name='change_password'),
]
