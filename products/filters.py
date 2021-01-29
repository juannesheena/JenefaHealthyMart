import django_filters as filters
from django_filters import CharFilter, ChoiceFilter,  ModelChoiceFilter
from .models import *


class ProductFilter(filters.FilterSet):
    CHOICES = (
                ('ascending', 'Ascending'),
                ('descending', 'Descending')

    )
    P_CHOICES = (
        ('lowest', 'Lowest Price'),
        ('highest', 'Highest Price')

    )

    search_name = CharFilter(field_name='name', lookup_expr='icontains')
    # search_description = CharFilter(field_name='description', lookup_expr='icontains')
    # product_type = ChoiceFilter(label='Order by', field_name='category', choices=CHOICES, method='filter_by_order')
    price = ChoiceFilter(field_name='price', choices=P_CHOICES, label='Sort by', method='filter_by_range',)

    class Meta:
        model = Product

        # fields = '__all__'
        fields = ['price']

    def filter_by_range(self, queryset, price, value):
        expression = 'price' if value == 'lowest' else '-price'
        return queryset.order_by(expression)

    # def filter_by_order(self, queryset, name, value):
    #   expression = 'name' if value == 'ascending' else '-name'
    #    return queryset.order_by(expression)
