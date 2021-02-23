from modeltranslation import translator

from apps.lead.models import Residence, Apartment, Photo, Video, File
from core.translation import TranslationOptionsMixin


@translator.register(Residence)
class ButtonOptions(TranslationOptionsMixin):
    fields = ('name', )


@translator.register(Apartment)
class MessageOptions(TranslationOptionsMixin):
    fields = ('description', )


@translator.register(Photo)
class PhotoOptions(TranslationOptionsMixin):
    fields = ('description', )


@translator.register(Video)
class VideoOptions(TranslationOptionsMixin):
    fields = ('description', )


@translator.register(File)
class FileOptions(TranslationOptionsMixin):
    fields = ('description', )
