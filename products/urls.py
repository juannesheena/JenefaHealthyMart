from django.urls import path
from . import views
from .views import (

    CartSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    CheckoutView,
    PaymentView,
    SearchView,
    ItemDetailView,
    AddCouponView,


)

app_name = 'product_urls'

urlpatterns = [
    path('', views.index, name='home-page'),
    path('category/<str:cats>/', views.category_view, name='category-page'),
    path('search/', SearchView.as_view(), name='search-page'),
    path('login/', views.login_user, name='login-page'),
    path('FAQ/', views.faq_user, name='questions-page'),
    path('about/', views.about_us, name='about-page'),
    path('privacy/', views.privacy, name='privacy-page'),
    path('profile/', views.profile, name='profile-page'),
    path('register/', views.register, name='register-page'),
    path('logout', views.logout_user, name='logout-page'),
    path('cart/', CartSummaryView.as_view(), name='cart-page'),
    path('checkout/', CheckoutView.as_view(), name='checkout-page'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-cart-page'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-cart-page'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-cart-page'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment-page'),  # <payment_option>
    path('add-coupon', AddCouponView.as_view(), name='add-coupon'),
    path('products/<slug>/', ItemDetailView.as_view(), name='product-page')

]
