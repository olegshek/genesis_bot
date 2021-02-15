from django.utils import timezone
from tortoise import models, fields

from apps.lead import app_name


class Lead(models.Model):
    customer = fields.ForeignKeyField(f'{app_name}.Customer', on_delete=fields.CASCADE, related_name='leads')

    completed_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(default=timezone.now, blank=True, editable=False)
    updated_at = fields.DatetimeField(auto_now=True)
