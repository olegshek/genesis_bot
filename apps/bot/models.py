from django.db import models
from django.utils.translation import gettext_lazy as _


class Button(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Code'))
    text = models.CharField(max_length=50, unique=True, verbose_name=_('Text'))

    class Meta:
        verbose_name = _('Button')
        verbose_name_plural = _('Buttons')

    def __str__(self):
        return self.code


class Keyboard(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Code'))
    buttons = models.ManyToManyField(Button, related_name='keyboards', through='KeyboardButtonsOrdering',
                                     verbose_name=_('Buttons'))

    class Meta:
        verbose_name = _('Keyboard')
        verbose_name_plural = _('Keyboards')


class KeyboardButtonsOrdering(models.Model):
    keyboard = models.ForeignKey(Keyboard, on_delete=models.CASCADE, related_name='buttons_ordering',
                                 verbose_name=_('Keyboard'))
    button = models.ForeignKey(Button, on_delete=models.CASCADE, related_name='ordering', verbose_name=_('Keyboard'))
    ordering = models.PositiveIntegerField(verbose_name='Ordering')

    class Meta:
        verbose_name = _('Keyboard buttons ordering')
        verbose_name_plural = _('Keyboard buttons orderings')


class Message(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name=_('Code'))
    text = models.TextField()

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return self.code
