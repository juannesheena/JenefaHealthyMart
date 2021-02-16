from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from products.forms import CreateUserForm
from django.contrib import messages
from products.models import Product, OrderItem, Order, BillingAddress, Payment, Offer, Category, \
    TrendingProduct, Wallpaper, Question
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm, CouponForm
from .filters import ProductFilter
from itertools import chain
from rest_framework import filters, generics
from django.conf import settings
import stripe

stripe.api_key = 'sk_test_7ldOddTn4RhtJOa5FAiUX9tF00juWf04DG'


def index(request):
    try:

        if request.user.is_authenticated:
            order = Order.objects.get(user=request.user, ordered=False)
            count = order.items.count
        else:
            count = 0

    except ObjectDoesNotExist:
        count = 0

    category = Category.objects.all()
    item = Product.objects.all()
    trending_product = TrendingProduct.objects.all()
    wallpaper = Wallpaper.objects.all()
    context = {'categories': category, 'items': item, 'count': count,
               'wallpapers': wallpaper, 'trending_products': trending_product}
    return render(request, 'home.html', context)


def faq_user(request):
    question = Question.objects.all()
    context = {'questions': question}
    return render(request, 'FAQ.html', context)


def about_us(request):
    return render(request, 'aboutus.html')


def privacy(request):
    return render(request, 'privacy.html')


def profile(request):
    user = User.objects.get(username=request.user)
    billing = BillingAddress.objects.get(user=request.user)
    context = {'user': user, 'billing': billing}
    return render(request, 'profile.html', context)


class SearchView(ListView):
    # template_name = 'search/products_view.html'
    template_name = 'view.html'
    # paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context
        # render(self.request, 'view.html', context)

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            product_results = Product.objects.search(query)
            # lesson_results = Lesson.objects.search(query)
            # profile_results = Profile.objects.search(query)

            # combine querysets
            queryset_chain = chain(
                product_results,
                # lesson_results,
                # profile_results
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)  # since qs is actually a list
            return qs
            # return render(request, 'view.html', qs)
        return Product.objects.none()


def category_view(request, cats):
    category_products = Product.objects.filter(category__title=cats)
    # products = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset=category_products)
    category_products = myFilter.qs
    context = {'cats': cats.title, 'category_products': category_products, 'myFilter': myFilter}
    return render(request, 'categories.html', context)


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, 'Successfully created an Account for ' + username)
            login(request, user)  # automatic login
            # return redirect('product_urls:login-page')
            return redirect('/')

    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            # form = AuthenticationForm(request.POST)
            # return render(request, 'login.html', {'form': form})
            messages.info(request, 'Username or password is incorrect')
    # else:
    # form = AuthenticationForm()
    # return render(request, 'login.html', {'form': form})
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False

            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(self.request, "You have not added a billing address")
            return redirect("product_urls:checkout-page")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source="tok_visa"  # token
            )
            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order was successful !")
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Not Authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(self.request, "Something went wrong, You were not charged. Please try again")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.warning(self.request, "A serious error occurred. We have been notified")
            return redirect("/")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm,
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("product_urls:checkout-page")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if self.request.method == 'POST':
            form = CheckoutForm(self.request.POST or None)
            try:

                # print(self.request.POST)
                if form.is_valid():
                    phone_number = form.cleaned_data.get('phone_number')
                    street_address = form.cleaned_data.get('street_address')
                    apartment_address = form.cleaned_data.get('apartment_address')
                    city = form.cleaned_data.get('city')
                    zip_no = form.cleaned_data.get('zip')
                    # same_billing_address = form.cleaned_data.get('same_billing_address')
                    # save_info = form.cleaned_data.get('save_info')
                    payment_option = form.cleaned_data.get('payment_option')
                    billing_address = BillingAddress(
                        user=self.request.user,
                        phone_number=phone_number,
                        street_address=street_address,
                        apartment_address=apartment_address,
                        city=city,
                        zip=zip_no,
                        # same_billing_address=same_billing_address,
                        # save_info=save_info
                    )
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                    if payment_option == 'C':
                        user = User.objects.get(username=self.request.user)
                        context = {'order': order, 'user': user}
                        return redirect('product_urls:payment-page', context, payment_option='direct_pay')
                    elif payment_option == 'D':
                        return redirect('product_urls:payment-page', payment_option='cash')
                    else:
                        messages.warning(
                            self.request, "Please select a payment method")
                        return redirect("product_urls:checkout-page")
                        # return redirect("product_urls:checkout-page")
                        # return render(self.request, 'checkout.html', {'form': form})

            except ObjectDoesNotExist:
                messages.warning(self.request, "You do not have an active order")
                return redirect("product_urls:cart-page")
            # messages.warning(self.request, "Please fill up the entire form")
            # return redirect("product_urls:checkout-page")

        else:
            # messages.warning(self.request, "Please fill up the entire form")
            #  form = CheckoutForm()
            print('something went wrong')

        context = {'form': form,
                   'couponform': CouponForm,
                   'order': order,
                   'DISPLAY_COUPON_FORM': True
                   }
        return render(self.request, 'checkout.html', context)


class ItemDetailView(DetailView):
    model = Product
    template_name = "products_view.html"


class CartSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "cart.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("product_urls:cart-page")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("product_urls:cart-page")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("product_urls:product-page", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("product_urls:product-page", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product_urls:product-page", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product_urls:product-page", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("product_urls:cart-page")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product_urls:product-page", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product_urls:product-page", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Offer.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("product_urls:checkout-page")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("product_urls:checkout-page")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("product_urls:checkout-page")
