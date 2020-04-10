from django.contrib import admin
from .models import Product, Offer, Order, OrderItem, BillingAddress, Payment


class OfferAdmin(admin.ModelAdmin):
    list_display = ('code','discount')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'slug', 'description')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'ordered_date', 'ordered')


class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'apartment_address', 'country', 'zip')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('stripe_charge_id', 'user', 'amount', 'timestamp')


admin.site.register(Offer, OfferAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress, BillingAddressAdmin)
admin.site.register(Payment, PaymentAdmin)


