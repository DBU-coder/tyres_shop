from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from customers.manager import CustomUserManager


class Customer(AbstractUser):
    class Meta:
        ordering = ['email']
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Telephone number'))
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Address'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'

    def get_absolute_url(self):
        return reverse('customers:details', kwargs={'pk': self.pk})
