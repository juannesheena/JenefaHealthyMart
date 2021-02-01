from django import template
from products.models import Category
register = template.Library()


@register.simple_tag
def category_list(request):
    category = Category.objects.all()
    context = {'categories': category}
    return context