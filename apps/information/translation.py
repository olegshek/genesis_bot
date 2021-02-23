from modeltranslation import translator

from apps.bot.models import Button, Message
from apps.information.models import InformationText
from core.translation import TranslationOptionsMixin


@translator.register(InformationText)
class ButtonOptions(TranslationOptionsMixin):
    fields = ('text',)
