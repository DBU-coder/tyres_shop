from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from shop.models import Product


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    ip = models.CharField(max_length=15)
    value = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )

    def __str__(self):
        return f'ip={self.ip} value:{self.value}'
