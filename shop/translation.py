from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, ProductType, ProductSpecification, ProductSpecificationValue


class AbstractTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Category)
class CategoryTranslationOptions(AbstractTranslationOptions):
    pass


@register(ProductType)
class ProductTypeTranslationOptions(AbstractTranslationOptions):
    pass


@register(ProductSpecification)
class SpecificationTranslationOptions(AbstractTranslationOptions):
    pass


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('country', 'description')


@register(ProductSpecificationValue)
class ProductSpecificationValueTranslationOptions(TranslationOptions):
    fields = ('value',)
