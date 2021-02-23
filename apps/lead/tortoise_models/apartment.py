from tortoise import models, fields

from apps.lead import app_name


class Residence(models.Model):
    name_en = fields.CharField(max_length=100)
    name_ru = fields.CharField(max_length=100)
    name_uz = fields.CharField(max_length=100)
    photo = fields.ForeignKeyField(f'{app_name}.Photo', on_delete=fields.CASCADE)

    class Meta:
        table = f'{app_name}_residence'


class RoomQuantity(models.Model):
    quantity = fields.IntField()

    class Meta:
        table = f'{app_name}_roomquantity'


class Photo(models.Model):
    photo = fields.TextField()
    description_en = fields.CharField(max_length=198)
    description_ru = fields.CharField(max_length=198)
    description_uz = fields.CharField(max_length=198)

    class Meta:
        table = f'{app_name}_photo'

    def get_path(self):
        return f"media/{self.photo}"


class File(models.Model):
    file = fields.TextField()
    description_en = fields.CharField(max_length=198)
    description_ru = fields.CharField(max_length=198)
    description_uz = fields.CharField(max_length=198)

    class Meta:
        table = f'{app_name}_file'

    def get_path(self):
        return f"media/{self.file}"


class Video(models.Model):
    video = fields.TextField()
    description_en = fields.CharField(max_length=198)
    description_ru = fields.CharField(max_length=198)
    description_uz = fields.CharField(max_length=198)

    class Meta:
        table = f'{app_name}_video'

    def get_path(self):
        return f"media/{self.video}"


class Apartment(models.Model):
    residence = fields.ForeignKeyField(f'{app_name}.Residence', on_delete=fields.CASCADE, related_name='apartments')
    room_quantity = fields.ForeignKeyField(f'{app_name}.RoomQuantity', on_delete=fields.CASCADE,
                                           related_name='apartments')
    description_en = fields.CharField(max_length=4000)
    description_ru = fields.CharField(max_length=4000)
    description_uz = fields.CharField(max_length=4000)

    class Meta:
        table = f'{app_name}_apartment'


class LeadApartmentFile(models.Model):
    apartment = fields.ForeignKeyField(f'{app_name}.Apartment', on_delete=fields.CASCADE)
    file = fields.ForeignKeyField(f'{app_name}.File', on_delete=fields.CASCADE)

    class Meta:
        table = f'{app_name}_apartment_files'


class LeadApartmentPhoto(models.Model):
    apartment = fields.ForeignKeyField(f'{app_name}.Apartment', on_delete=fields.CASCADE)
    photo = fields.ForeignKeyField(f'{app_name}.Photo', on_delete=fields.CASCADE)

    class Meta:
        table = f'{app_name}_apartment_photos'


class LeadApartmentVideo(models.Model):
    apartment = fields.ForeignKeyField(f'{app_name}.Apartment', on_delete=fields.CASCADE)
    video = fields.ForeignKeyField(f'{app_name}.Video', on_delete=fields.CASCADE)

    class Meta:
        table = f'{app_name}_apartment_videos'
