from .models import News, Category
from modeltranslation.translator import translator, TranslationOptions, register

@register(News)

class NewsTranslationOptions(TranslationOptions):
    fields=('title', 'body')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields=('name',)