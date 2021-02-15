import os

from tortoise import models, fields

from apps.lead import app_name


class Residence(models.Model):
    name = fields.CharField(max_length=100)


class RoomQuantity(models.Model):
    quantity = fields.IntField()


class Photo(models.Model):
    photo = fields.TextField()

    def get_url(self):
        return f"https://{os.environ['PRODUCTION_HOST']}/{self.photo}"


class File(models.Model):
    file = fields.TextField()

    def get_url(self):
        return f"https://{os.environ['PRODUCTION_HOST']}/{self.file}"


class Apartment(models.Model):
    residence = fields.ForeignKeyField(f'{app_name}.Residence', on_delete=fields.CASCADE, related_name='apartments')
    room_quantity = fields.ForeignKeyField(f'{app_name}.RoomQuantity', on_delete=fields.CASCADE,
                                           related_name='apartments')
    square = fields.FloatField()
    description = fields.CharField(max_length=4000)
    photos = fields.ManyToManyField(f'{app_name}.Photo', related_name='apartments')
    files = fields.ManyToManyField(f'{app_name}.Photo', related_name='apartments')
