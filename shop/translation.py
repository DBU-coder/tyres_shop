from modeltranslation.translator import register, TranslationOptions
from .models import Category, Tyre, Wheel


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class AbstractProductTranslationOptions(TranslationOptions):
    fields = ('country', 'description')


@register(Tyre)
class TyreTranslationOptions(AbstractProductTranslationOptions):
    pass


@register(Wheel)
class WheelTranslationOptions(AbstractProductTranslationOptions):
    pass
