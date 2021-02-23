from tortoise import models, fields

from apps.information import app_name


class InformationText(models.Model):
    text_ru = fields.CharField(max_length=4000)
    text_en = fields.CharField(max_length=4000)
    text_uz = fields.CharField(max_length=4000)

    class Meta:
        table = f'{app_name}_informationtext'


class InformationFile(models.Model):
    file = fields.OneToOneField('lead.File', on_delete=fields.CASCADE, related_name='information_file')

    class Meta:
        table = f'{app_name}_informationfile'


class InformationPhoto(models.Model):
    photo = fields.OneToOneField('lead.Photo', on_delete=fields.CASCADE, related_name='information_photo')

    class Meta:
        table = f'{app_name}_informationphoto'


class InformationVideo(models.Model):
    video = fields.OneToOneField('lead.Video', on_delete=fields.CASCADE, related_name='information_video')

    class Meta:
        table = f'{app_name}_informationvideo'
