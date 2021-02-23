from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.lead.models import File, Photo, Video


class InformationText(models.Model):
    text = models.CharField(max_length=4000, verbose_name=_('Text'))

    class Meta:
        verbose_name = _('Information text')
        verbose_name_plural = _('Information text')

    def __str__(self):
        return self.text_ru


class InformationFile(models.Model):
    file = models.OneToOneField(File, on_delete=models.CASCADE, related_name='information_file', verbose_name=_('File'))

    class Meta:
        verbose_name = _('Information file')
        verbose_name_plural = _('Information files')

    def __str__(self):
        return self.file.file.name


class InformationPhoto(models.Model):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, related_name='information_photo',
                                 verbose_name=_('Photo'))

    class Meta:
        verbose_name = _('Information photo')
        verbose_name_plural = _('Information photos')

    def __str__(self):
        return self.photo.photo.name


class InformationVideo(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name='information_video',
                                 verbose_name=_('Video'))

    class Meta:
        verbose_name = _('Information video')
        verbose_name_plural = _('Information videos')

    def __str__(self):
        return self.video.video.name
