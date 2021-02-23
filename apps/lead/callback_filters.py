from apps.bot.tortoise_models import Button
from apps.lead.tortoise_models import Residence, RoomQuantity, Apartment
from core.filters import message_filter


async def language_choice(message):
    en_text = (await Button.get(code='en')).text_en
    ru_text = (await Button.get(code='ru')).text_ru
    uz_text = (await Button.get(code='uz')).text_uz
    return message.text in [en_text, ru_text, uz_text]


async def residence_choice(query):
    data = query.data
    data = data.split(':')

    if 'residence' in data and len(data) > 1 and int(data[1]) in await Residence.all().values_list('id', flat=True):
        return True

    return False


async def room_quantity_choice(query):
    data = query.data
    data = data.split(':')

    if 'quantity' in data and len(data) > 1 and int(data[1]) in await RoomQuantity.all().values_list('id', flat=True):
        return True

    return False


async def apartment_choice(query):
    data = query.data
    data = data.split(':')

    if 'apartment' in data and len(data) > 1 and int(data[1]) in await Apartment.all().values_list('id', flat=True):
        return True

    return False


async def lead_request(query):
    data = query.data
    data = data.split(':')

    if 'lead_request' in data and len(data) > 1 and int(data[1]) in await Apartment.all().values_list('id', flat=True):
        return True

    return False
