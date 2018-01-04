from django.template.response import TemplateResponse
from cartridge.shop.models import Category


def direct_to_template(request, template, extra_context=None, **kwargs):
    """
    Replacement for Django's ``direct_to_template`` that uses
    ``TemplateResponse`` via ``mezzanine.utils.views.render``.
    """
    context = extra_context or {}
    context["params"] = kwargs
    context["homepage_products"] = get_products()
    for (key, value) in context.items():
        if callable(value):
            context[key] = value()
    return TemplateResponse(request, template, context)


def get_products():
    try:
        category = Category.objects.get(slug='shop')
        products = category.products.filter(available=True).order_by('-publish_date')
    except Category.DoesNotExist:
        products = []
    return products
