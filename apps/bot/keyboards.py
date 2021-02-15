from aiogram import types

from apps.bot.tortoise_models import Button, KeyboardButtonsOrdering


async def get_back_button_obj():
    return await Button.get(code='back')


async def language_choice(locale='ru', change=False):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    buttons = []
    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='language_choice').order_by(
            'ordering'):
        button = await keyboard_button.button
        code = button.code
        buttons.append(types.InlineKeyboardButton(
            button.text_ru if code == 'ru' else button.text_uz if code == 'uz' else button.text_en
        ))

    if change:
        back_button_obj = await get_back_button_obj()
        buttons.append(types.KeyboardButton(getattr(back_button_obj, f'text_{locale}')))

    keyboard.add(*buttons)
    return keyboard


async def phone_number(locale):
    back_button_obj = await get_back_button_obj()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='phone_number').order_by('ordering'):
        button = await keyboard_button.button
        keyboard.add(types.KeyboardButton(
            getattr(button, f'text_{locale}'),
            request_contact=True if button.code == 'phone_number' else None
        ))
    keyboard.add(types.KeyboardButton(getattr(back_button_obj, f'text_{locale}')))
    return keyboard


async def main_menu(locale):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='main_menu').order_by('ordering'):
        button = await keyboard_button.button
        tg_button = types.InlineKeyboardButton(getattr(button, f'text_{locale}'), callback_data=button.code)
        keyboard.row(tg_button)

    return keyboard


async def confirm(locale):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    confirm_button = await Button.get(code='confirm')
    back_button = await get_back_button_obj()
    keyboard.add(*[types.KeyboardButton(getattr(button, f'text_{locale}')) for button in [confirm_button, back_button]])
    return keyboard


async def back_keyboard(locale):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = await get_back_button_obj()
    keyboard.add(types.KeyboardButton(getattr(button, f'text_{locale}')))
    return keyboard


remove_keyboard = types.ReplyKeyboardRemove()
