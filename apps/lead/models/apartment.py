from django.db import models
from django.utils.translation import gettext_lazy as _


class Photo(models.Model):
    photo = models.ImageField(verbose_name=_('Photo'))
    description = models.CharField(max_length=198, null=True, blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def __str__(self):
        return self.photo.name


class File(models.Model):
    file = models.FileField(verbose_name=_('File'))
    description = models.CharField(max_length=198, null=True, blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def __str__(self):
        return self.file.name


class Video(models.Model):
    video = models.FileField(verbose_name=_('Video'))
    description = models.CharField(max_length=198, null=True, blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    def __str__(self):
        return self.video.name


class Residence(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    photo = models.ForeignKey(Photo, on_delete=models.RESTRICT, related_name='residences', verbose_name=_('Photo'))
    apartment_choice_photo = models.OneToOneField(Photo, on_delete=models.SET_NULL, related_name='residence', null=True,
                                                  verbose_name=_('Apartment choice photo'))

    class Meta:
        verbose_name = _('Residence')
        verbose_name_plural = _('Residences')

    def __str__(self):
        return self.name_ru


class RoomQuantity(models.Model):
    quantity = models.PositiveIntegerField(unique=True, verbose_name=_('Quantity'))

    class Meta:
        verbose_name = _('Room quantity')
        verbose_name_plural = _('Room quantities')

    def __str__(self):
        return str(self.quantity)


class Apartment(models.Model):
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE, related_name='apartments',
                                  verbose_name=_('Residence'))
    room_quantity = models.ForeignKey(RoomQuantity, on_delete=models.CASCADE, related_name='apartments',
                                      verbose_name=_('Room quantity'))
    description = models.CharField(max_length=4000, verbose_name=_('Description'))
    photos = models.ManyToManyField(Photo, related_name='apartments', verbose_name=_('Photos'))
    files = models.ManyToManyField(File, blank=True, related_name='apartments', verbose_name=_('Files'))
    videos = models.ManyToManyField(Video, blank=True, related_name='apartments', verbose_name=_('Videos'))

    class Meta:
        verbose_name = _('Apartment')
        verbose_name_plural = _('Apartments')

    def __str__(self):
        return f'{self.residence.name_ru}-{self.room_quantity.quantity}'
