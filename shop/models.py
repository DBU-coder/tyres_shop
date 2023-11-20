import stripe

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum, Avg, Count, UniqueConstraint, Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_resized import ResizedImageField

stripe.api_key = settings.STRIPE_SECRET_KEY


def user_directory_path(instance, filename):
    """Setting path to upload product images"""
    product_type = instance.product.product_type.name
    product_name = instance.product.name
    return f'images/products/{product_type}/{product_name}/{filename}'


class HomepageProductsManager(models.Manager):

    @staticmethod
    def get_new_products(quantity=4):
        return Product.objects.select_related('category').order_by('-created')[:quantity]

    @staticmethod
    def get_popular_products(days=0):
        """Returns popular products in the given days range."""
        popular = ProductStatistic.objects.filter(
            date__range=[timezone.now() - timezone.timedelta(days=days), timezone.now()],
        ).annotate(
            total_sales=Sum('purchases_quantity')
        ).order_by('-total_sales').values_list('product_id', flat=True)
        popular_products = Product.objects.filter(id__in=popular).select_related('category').prefetch_related('ratings').annotate(
                avg_rating=Avg('ratings__value'),
                users_count=Count('ratings__ip')
            )
        return popular_products


class HomepageProduct:
    objects = HomepageProductsManager()


class Category(models.Model):
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _('Categories')

    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)
    is_active = models.BooleanField(_('Is Active'), default=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    ProductType Table will provide a list of the different types
    of products that are for sale.
    """

    name = models.CharField(_("Type name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    The Product Specification Table contains product
    specification or features for the product types.
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")
        unique_together = ("product_type", "name")

    def __str__(self):
        return self.name


class Product(models.Model):
    """The Product table containing all product items."""

    STATUS_CHOICES = (
        (0, _('out stock')),
        (1, _('in stock')),
        (2, _('running out')),
        (3, _('coming soon')),
    )
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT, verbose_name=_('Product Type'))
    specification = models.ManyToManyField(ProductSpecification, through='ProductSpecificationValue')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name=_('Category'))
    name = models.CharField(_('Name'), max_length=100, unique=True)
    sku = models.CharField(_('sku'), max_length=10, unique=True)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True, help_text=_('The field is filled in automatically'))
    brand = models.CharField(_('Brand'), max_length=100)
    country = models.CharField(_('Country'), max_length=50, blank=True)
    description = models.TextField(_('Description'), blank=True)
    price = models.DecimalField(
        verbose_name=_('Price'),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 9999.99."),
            },
        },
        max_digits=6,
        decimal_places=2
    )
    stripe_product_price_id = models.CharField(
        max_length=128,
        blank=True,
        help_text=_('The field is filled in automatically')
    )
    status = models.PositiveSmallIntegerField(_('Status'), default=0, choices=STATUS_CHOICES)
    created = models.DateTimeField(_('Created'), auto_now_add=True, editable=False)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    is_active = models.BooleanField(_('Is Active'), default=True, help_text=_('Change product visibility'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(
            name=self.name
        )
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=int(self.price * 100),
            currency='usd'
        )
        return stripe_product_price

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class ProductSpecificationValue(models.Model):
    """
    The Product Specification Value table holds each of the
    products individual specification or bespoke features.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="spec")
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Product specification value (maximum of 255 characters"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")
        unique_together = ("specification", "product", "value")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """The Product Image table."""

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product images')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = ResizedImageField(
        size=[300, 400],
        crop=['middle', 'center'],
        upload_to=user_directory_path,
        verbose_name=_('Image')
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative text"),
        help_text=_("Please add alternative text"),
        max_length=255,
        blank=True,
    )


class ProductStatistic(models.Model):
    """
    Contains information about quantity of purchases for each product.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='statistics')
    date = models.DateField(_('Date'), default=timezone.now)
    purchases_quantity = models.PositiveIntegerField(_('Purchases quantity'), default=0)

    class Meta:
        verbose_name_plural = _('Product statistics')

    def __str__(self):
        return f'{self.product.name} sales: {self.purchases_quantity}'
