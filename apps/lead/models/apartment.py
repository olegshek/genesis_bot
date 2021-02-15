from django.db import models
from django.utils.translation import gettext_lazy as _


class Residence(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Residence')
        verbose_name_plural = _('Residences')


class RoomQuantity(models.Model):
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))

    class Meta:
        verbose_name = _('Room quantity')
        verbose_name_plural = _('Room quantities')


class Photo(models.Model):
    photo = models.ImageField(verbose_name=_('Photo'))


class File(models.Model):
    file = models.FileField(verbose_name=_('File'))


class Apartment(models.Model):
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE, related_name='apartments',
                                  verbose_name=_('Residence'))
    room_quantity = models.ForeignKey(RoomQuantity, on_delete=models.CASCADE, related_name='apartments',
                                      verbose_name=_('Room quantity'))
    square = models.FloatField(verbose_name=_('Square'))
    description = models.CharField(max_length=4000, verbose_name=_('Description'))
    photos = models.ManyToManyField(Photo, related_name='apartments', verbose_name=_('Photos'))
    files = models.ManyToManyField(File, related_name='apartments', verbose_name=_('Files'))
