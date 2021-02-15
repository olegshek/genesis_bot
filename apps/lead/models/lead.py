from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.lead.models import Customer


class Lead(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='leads', verbose_name=_('Customer'))

    completed_at = models.DateTimeField(null=True, verbose_name=_('Completed at'))
    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
