from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')

    code = models.CharField(verbose_name=_('Code'), max_length=50, unique=True)
    valid_from = models.DateTimeField(verbose_name=_('Valid from'))
    valid_to = models.DateTimeField(verbose_name=_('Valid to'))
    discount = models.IntegerField(
        verbose_name=_('Discount amount'),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_('Percentage value (0 to 100)')
    )
    active = models.BooleanField(verbose_name=_('Active'))

    def __str__(self):
        return f'{self.code} [-{self.discount}%]'
