from aiogram import types

from apps.bot.tortoise_models import Button, KeyboardButtonsOrdering
from apps.lead.tortoise_models import Residence, Apartment, RoomQuantity


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


async def residence_choice(locale):
    name_field = f'name_{locale}'
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    for residence in await Residence.all().order_by(name_field):
        keyboard.row(
            types.InlineKeyboardButton(getattr(residence, name_field), callback_data=f'residence:{residence.pk}')
        )

    back_button_obj = await get_back_button_obj()
    keyboard.add(
        types.InlineKeyboardButton(getattr(back_button_obj, f'text_{locale}'), callback_data=back_button_obj.code)
    )
    return keyboard


async def room_quantity_choice(residence_id, locale):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    room_quantities = await RoomQuantity.filter(apartments__residence_id=residence_id).distinct().order_by('quantity')
    buttons = []
    for room_quantity in room_quantities:
        buttons.append(types.InlineKeyboardButton(
            str(room_quantity.quantity),
            callback_data=f'quantity:{room_quantity.pk}'
        ))

    keyboard.add(*buttons)

    back_button_obj = await get_back_button_obj()
    keyboard.add(
        types.InlineKeyboardButton(getattr(back_button_obj, f'text_{locale}'), callback_data=back_button_obj.code)
    )
    return keyboard


async def apartment_choice(residence_id, quantity_id, locale):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    buttons = []
    for apartment in await Apartment.filter(residence_id=residence_id, room_quantity_id=quantity_id).order_by('square'):
        buttons.append(types.InlineKeyboardButton(
            str(apartment.square),
            callback_data=f'apartment:{apartment.pk}'
        ))

    keyboard.add(*buttons)

    back_button_obj = await get_back_button_obj()
    keyboard.add(
        types.InlineKeyboardButton(getattr(back_button_obj, f'text_{locale}'), callback_data=back_button_obj.code)
    )
    return keyboard


async def back_keyboard(locale):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = await get_back_button_obj()
    keyboard.add(types.KeyboardButton(getattr(button, f'text_{locale}')))
    return keyboard


async def lead_request(apartment_id, locale):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    lead_button = await Button.get(code='lead_request')
    keyboard.add(types.InlineKeyboardButton(
        getattr(lead_button, f'text_{locale}'),
        callback_data=f'lead_request:{apartment_id}')
    )

    back_button_obj = await get_back_button_obj()
    keyboard.add(
        types.InlineKeyboardButton(getattr(back_button_obj, f'text_{locale}'), callback_data=back_button_obj.code)
    )

    return keyboard


remove_keyboard = types.ReplyKeyboardRemove()
