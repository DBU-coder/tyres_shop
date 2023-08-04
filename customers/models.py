from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from customers.manager import CustomUserManager


class Customer(AbstractUser):
    class Meta:
        ordering = ['email']

    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Telephone number')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Address')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('customers:details', kwargs={'pk': self.pk})
