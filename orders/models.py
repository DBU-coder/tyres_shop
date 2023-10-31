from decimal import Decimal

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from customers.models import Customer
from coupons.models import Coupon


class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE, verbose_name=_('Customer'))
    first_name = models.CharField(_('First name'), max_length=100)
    last_name = models.CharField(_('Last name'), max_length=100)
    email = models.EmailField()
    phone = models.CharField(_('Phone'), max_length=50)
    country = models.CharField(_('Country'), max_length=70)
    zip = models.IntegerField(_('Zip'))
    address = models.TextField(_('Address'), max_length=300)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    paid = models.BooleanField(_('Paid'), default=False)
    delivery = models.ForeignKey('Delivery', related_name='orders', on_delete=models.CASCADE, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    discount = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def stripe_products(self):
        products = self.items.all()
        line_items = []
        for product in products:
            item = {
                'price': product.content_object.stripe_product_price_id,
                'quantity': product.quantity
            }
            line_items.append(item)
        return line_items

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'OrderItem: {self.id}'

    def get_cost(self):
        return self.price * self.quantity


class Delivery(models.Model):
    method = models.CharField(_('Method'), max_length=50)
    cost = models.PositiveSmallIntegerField(_('Cost'), default=0)

    class Meta:
        verbose_name = _('Delivery')
        verbose_name_plural = _('Deliveries')

    def __str__(self):
        return f'{self.method}\t+{self.cost}$/pcs.'
