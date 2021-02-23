from django.utils import timezone
from tortoise import models, fields

from apps.lead import app_name
from apps.lead.services import send_to_bitrix
from core.utils import generate_number


class Lead(models.Model):
    number = fields.IntField(default=generate_number)
    customer = fields.ForeignKeyField(f'{app_name}.Customer', on_delete=fields.CASCADE, related_name='leads')
    apartment = fields.ForeignKeyField(f'{app_name}.Apartment', on_delete=fields.CASCADE, related_name='leads')

    created_at = fields.DatetimeField(default=timezone.now, blank=True, editable=False)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = f'{app_name}_lead'

    async def send_lead_to_bitrix(self):
        await send_to_bitrix(self)
