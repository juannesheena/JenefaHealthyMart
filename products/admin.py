from django.contrib import admin
from .models import Product, Offer, Order, OrderItem, BillingAddress, Payment, Category, TrendingProduct, Wallpaper, Question


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'cat_icon')


class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount')


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


class TrendingProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_url')


class WallpaperAdmin(admin.ModelAdmin):
    list_display = ['image_url', 'title', 'description', 'id_num']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress, BillingAddressAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(TrendingProduct, TrendingProductAdmin)
admin.site.register(Wallpaper, WallpaperAdmin)
admin.site.register(Question, QuestionAdmin)

