from apps.bot.tortoise_models import Button
from core.callback_filters import callback_filter


async def keyboard_back(message):
    back_button = await Button.get(name='back')
    return message.text in [getattr(back_button, f'text_{locale}') for locale in ['ru', 'uz']]


async def inline_back(query):
    return query.data == 'back'


async def message_is_not_command(message):
    if message.text:
        return not message.text.startswith('/')
    return True


async def main_menu(query):
    return await callback_filter(query, 'main_menu')
