from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.core.validators import RegexValidator
from phonenumbers import phonenumber
import re

PAYMENT_CHOICES = (
    ('C', 'Debit or Credit Card'),
    ('D', 'Cash on Delivery')
)

CITY_CHOICES = (
    ('Colombo 1', 'Colombo 1'),
    ('Colombo 2', 'Colombo 2'),
    ('Colombo 3', 'Colombo 3'),
    ('Colombo 4', 'Colombo 4'),
    ('Colombo 5', 'Colombo 5'),
    ('Colombo 6', 'Colombo 6'),
    ('Colombo 7', 'Colombo 7'),
    ('Colombo 8', 'Colombo 8'),
    ('Colombo 9', 'Colombo 9'),
    ('Colombo 10', 'Colombo 10'),
    ('Colombo 11', 'Colombo 11'),
    ('Colombo 12', 'Colombo 12'),
    ('Colombo 13', 'Colombo 13'),
    ('Colombo 14', 'Colombo 14'),
    ('Colombo 15', 'Colombo 15'),
)

phone_regex = RegexValidator(
    regex=r'^(?:0|94|\+94|0094)?(?:(11|21|23|24|25|26|27|31|32|33|34|35|36|37|38|41|45|47|51|52|54|55|57|63|65|66|67'
          r'|81|91)(0|2|3|4|5|7|9)|7(0|1|2|5|6|7|8)\d)\d{6}$',
    message="Phone number must be entered in the format: '+ 94 07 y zzzzzz'. Up to 10 digits allowed.",
    code='invalid_phone'
)


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class CheckoutForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control w-50', 'placeholder': '07x 123 1234'}),
        max_length=10, min_length=9, required=True,
    )
    street_address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Street Address'}), required=True, )
    apartment_address = forms.CharField(required=False,
                                        widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Apartment Address'}), )
    """country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
            'id': 'zip'

        }))"""
    # city = forms.CharField(widget=forms.Select(choices=CITY_CHOICES))
    city = forms.CharField(widget=forms.Select(
        attrs={'class': 'custom-select d-block w-100', 'id': 'city'}, choices=CITY_CHOICES))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True,)
    # default_billing_address = forms.BooleanField(required=False)  # --don't need
    save_info = forms.BooleanField(required=False)  # --don't need
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES,
        error_messages={'required': 'Please select a payment option'}, required=True)

    """def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        
        if not phone_number.isdigit() and len(phone_number) != 10:
            raise forms.ValidationError(_('Invalid mobile number'), code='invalid')

        if not zip.isdigit():
            raise forms.ValidationError(_('Invalid zip'), code='invalid')"""

    # rule = re.compile(r'/^(?:0|94|\+94|0094)?(?:(11|21|23|24|25|26|27|31|32|33|34|35|36|37|38|41|'
    # r'45|47|51|52|54|55|57|63|65|66|67'
    # r'|81|91)(0|2|3|4|5|7|9)|7(0|1|2|5|6|7|8)\d)\d{6}$/')
    # if not rule.search(phone_number):
    # msg = "Invalid mobile number."
    # raise forms.ValidationError(msg)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))
