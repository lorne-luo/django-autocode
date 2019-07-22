from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    """Customer model"""

    # Fields
    first_name = models.CharField(_('first_name'), max_length=255, blank=False, null=False)
    last_name = models.CharField(_('last_name'), max_length=255, blank=True, null=False)
    status = models.CharField(max_length=30, blank=True, null=True)
    sign_up_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=False, null=False)
    email_verified = models.BooleanField(default=False)
    gender = models.EmailField(blank=False, null=False, )
    phone_number = models.CharField(max_length=30, blank=True, null=False)
    photo = models.ImageField(blank=True, null=True)
    same_as_shipping = models.BooleanField(default=True)


class Address(models.Model):
    street_number_name = models.CharField(max_length=255, blank=True, null=False,
                                          verbose_name="Street number and name")
    suburb = models.CharField(max_length=255, blank=True, null=False)
    postcode = models.CharField(max_length=30, blank=True, null=False, validators=[RegexValidator(
        regex='^[0-9]*$',
        message='Postcode must be number',
        code='invalid_postcode'
    )])
    state = models.CharField(max_length=255, blank=True, null=False)
    country = models.CharField(max_length=255, blank=True, null=False)
