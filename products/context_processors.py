from django.core.exceptions import ObjectDoesNotExist

from products.models import Category, Order


def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}


def cart_items_count_processor(request):
    try:

        if request.user.is_authenticated:
            order = Order.objects.get(user=request.user, ordered=False)
            count = order.items.count
        else:
            count = 0

    except ObjectDoesNotExist:
        count = 0

    return {'count': count}
