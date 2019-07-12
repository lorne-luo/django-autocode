from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import EmailField
from django.db.models import URLField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields

from core.constants import AU_STATE_CHOICES, SEX_CHOICES, USER_STATUS_CHOICES
from core.django.models import BaseModel


class Customer(BaseModel):
    # Fields
    name = models.CharField(max_length=255, blank=False, null=False)
    status = models.CharField(max_length=30, blank=False, null=False, choices=USER_STATUS_CHOICES)
    sign_up_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=False, null=False)
    gender = models.EmailField(blank=False, null=False, choices=SEX_CHOICES)
    phone_number = models.CharField(max_length=30)
    photo_url = models.URLField(blank=True, null=False)

    # Relationship Fields
    shipping_address = models.ForeignKey(
        'customer.Address',
        on_delete=models.CASCADE, related_name="shipping_customers", blank=True, null=True
    )
    billing_address = models.ForeignKey(
        'customer.Address',
        on_delete=models.CASCADE, related_name="billing_customers", blank=True, null=True
    )
    auth0_user = models.OneToOneField(
        'social_django.UserSocialAuth',
        on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('customer_customer_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('customer_customer_update', args=(self.pk,))


class Address(BaseModel):
    # Fields
    street_number_name = models.CharField(max_length=255, blank=True, null=False)
    suburb = models.CharField(max_length=255, blank=True, null=False)
    state = models.CharField(max_length=255, blank=True, null=False, choices=AU_STATE_CHOICES)
    country = models.CharField(max_length=255, blank=True, null=False)

    # Relationship Fields
    # customer = models.ForeignKey(
    #     'customer.Customer',
    #     on_delete=models.CASCADE, related_name="addresss", blank=True, null=True
    # )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('customer_address_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('customer_address_update', args=(self.pk,))
