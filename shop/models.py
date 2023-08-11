import stripe
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from orders.models import OrderItem
from ratings.models import Rating

stripe.api_key = settings.STRIPE_SECRET_KEY


def user_directory_path(instance, filename):
    model_name = instance.content_type.model
    product_id = instance.object_id
    return f'images/products/{model_name}/{product_id}/{filename}'


class HomepageProductsManager:

    @staticmethod
    def get_products(*args):
        products = []
        content_type_models = ContentType.objects.filter(model__in=args)
        for ct_model in content_type_models:
            # TODO: Сделать фильтрацию по новинкам и популярным.
            model_products = ct_model.model_class().objects.all().order_by('-created')[:4]
            products.extend(model_products)
        return products


class HomepageProduct:
    objects = HomepageProductsManager()


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    """ Table for upload multiple images"""

    _MAX_WIDTH = 300

    image = models.ImageField(upload_to=user_directory_path, default='static/assets/images/errors-images/no-image.png')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    # def save(self, *args, **kwargs):
    #     # Сначала - обычное сохранение
    #     super().save(*args, **kwargs)
    #     filepath = self.image.path
    #     width = self.logo.width
    #     height = self.logo.height
    #
    #     max_size = max(width, height)
    #
    #     # Может, и не надо ничего менять?
    #     if max_size > _MAX_SIZE:
    #         # Надо, Федя, надо
    #         image = Image.open(filename)
    #         # resize - безопасная функция, она создаёт новый объект, а не
    #         # вносит изменения в исходный, поэтому так
    #         image = image.resize(
    #             (round(width / max_size * _MAX_SIZE),  # Сохраняем пропорции
    #              round(height / max_size * _MAX_SIZE)),
    #             Image.ANTIALIAS
    #         )
    #         # И не забыть сохраниться
    #         image.save(filename)


class BaseProduct(models.Model):
    STATUS_CHOICES = (
        (0, 'out stock'),
        (1, 'in stock'),
        (2, 'running out'),
        (3, 'coming soon'),
    )

    class Meta:
        abstract = True

    sku = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    brand = models.CharField(max_length=100)
    country = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    status = models.PositiveSmallIntegerField(default=0, choices=STATUS_CHOICES)
    stock_qty = models.IntegerField('Stock quantity', default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    gallery = GenericRelation(Gallery, related_query_name='product')
    ratings = GenericRelation(Rating, related_query_name='product')
    order_items = GenericRelation(OrderItem, related_query_name='product')

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'ct_model': self._meta.model_name, 'slug': self.slug})

    @property
    def model_name(self):
        ct = ContentType.objects.get_for_model(self)
        return ct.model

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(
            name=self.name,
            images=[f'{settings.DOMAIN_NAME}/{gallery.image.url}' for gallery in self.gallery.all()]
        )
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=(self.price * 100),
            currency='uah'
        )
        return stripe_product_price

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Tyre(BaseProduct):
    VEHICLE_CHOICES = (
        (1, 'Motorcycle'),
        (2, 'Car'),
        (3, 'Truck'),
        (4, 'Special transports'),
    )

    SEASON_CHOICES = (
        (1, 'All season'),
        (2, 'Summer'),
        (3, 'Winter'),
    )

    vehicle_type = models.PositiveSmallIntegerField('Vehicle type', choices=VEHICLE_CHOICES)
    profile = models.DecimalField(max_digits=4, decimal_places=1)
    season = models.PositiveSmallIntegerField(choices=SEASON_CHOICES)
    diameter = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()
    load_index = models.PositiveSmallIntegerField(blank=True)
    speed_index = models.CharField(max_length=3, blank=True)
    spikes = models.BooleanField(default=False)
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return f'Tire: {self.name}'


class Wheel(BaseProduct):
    TYPE_CHOICES = (
        (1, 'Alloy'),
        (2, 'Steel'),
    )

    model = models.CharField(max_length=100, blank=True)
    et = models.PositiveSmallIntegerField(blank=True, null=True)
    diameter = models.PositiveSmallIntegerField()
    pcd = models.CharField(max_length=20, blank=True, null=True)
    width = models.DecimalField(max_digits=4, decimal_places=2)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    dia = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'Wheel: {self.name}'


class Product(models.Model):
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': ('tyre', 'wheel')}
                                     )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
