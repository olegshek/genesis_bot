from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, unique=True)
    username = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Username'))
    full_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Full name'))
    phone_number = models.CharField(max_length=20, null=True, verbose_name=_('Phone number'))
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, null=True, verbose_name=_('Language'))

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
