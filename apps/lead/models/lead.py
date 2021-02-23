from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.lead.models import Customer, Apartment
from core.utils import generate_number


class Lead(models.Model):
    number = models.IntegerField(default=generate_number)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='leads', verbose_name=_('Customer'))
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='lead', verbose_name=_('Apartment'))

    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
