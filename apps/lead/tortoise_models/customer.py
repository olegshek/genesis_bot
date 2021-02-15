from enum import Enum

from tortoise import models, fields

from apps.lead import app_name


class Customer(models.Model):
    class Languages(str, Enum):
        RU = 'ru'
        UZ = 'uz'
        EN = 'en'

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, blank=True, null=True)
    full_name = fields.CharField(max_length=200, null=True, blank=True)
    phone_number = fields.CharField(max_length=20, null=True)
    language = fields.CharField(max_length=2, choices=Languages, null=True)

    class Meta:
        table = f'{app_name}_customer'
