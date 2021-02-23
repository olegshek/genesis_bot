from aiogram.types import ContentType
from django.conf import settings

from apps.bot import callback_filters as bot_callback_filters, bot, keyboards, messages
from apps.bot import dispatcher as dp
from apps.bot.telegram_views import send_main_menu
from apps.bot.tortoise_models import Button
from apps.lead import callback_filters
from apps.lead.states import CustomerForm
from apps.lead.telegram_views.lead import create_lead
from apps.lead.tortoise_models import Customer, Feedback


async def create_feedback(user_id, state, locale, message_id=None):
    feedback = await Feedback.create(customer_id=user_id)

    if settings.SEND_TO_BITRIX:
        await feedback.send_feedback_to_bitrix()

    message_text = await messages.get_message('request_accepted', locale)

    if state != CustomerForm.full_name.state and message_id:
        await bot.edit_message_text(message_text, user_id, message_id)
    else:
        await bot.send_message(user_id, message_text, reply_markup=keyboards.remove_keyboard)

    message = await messages.get_message('request_number', locale) + f' {feedback.number}'
    await bot.send_message(user_id, message, reply_markup=keyboards.remove_keyboard)

    customer = await Customer.get(id=user_id)
    await send_main_menu(customer, locale, state)


@dp.message_handler(callback_filters.language_choice, state=CustomerForm.language_choice.state)
async def language_choice_processing(message, locale, state):
    user_id = message.from_user.id
    customer = await Customer.get(id=user_id)
    text = message.text
    en_button = await Button.get(code='en')
    ru_button = await Button.get(code='ru')
    language = en_button.code if text == en_button.text_en else ru_button.code if text == ru_button.text_ru else 'uz'
    customer.language = language
    await customer.save()

    await bot.send_message(user_id, '✔', reply_markup=keyboards.remove_keyboard)
    await send_main_menu(customer, locale, state)


@dp.message_handler(state=CustomerForm.phone_number, content_types=[ContentType.CONTACT])
async def phone_number_save(message, locale, state):
    user_id = message.from_user.id
    customer = await Customer.get(id=user_id)
    contact = message.contact

    if contact.user_id == user_id:
        customer.phone_number = contact.phone_number
        await customer.save()

    await bot.send_message(user_id, '✔', reply_markup=keyboards.remove_keyboard)
    await send_main_menu(customer, locale, state)


@dp.message_handler(bot_callback_filters.message_is_not_command, bot_callback_filters.message_is_not_back,
                    state=CustomerForm.full_name.state, content_types=[ContentType.TEXT])
async def full_name_save(message, locale, state):
    user_id = message.from_user.id
    customer = await Customer.get(id=user_id)
    full_name = message.text
    customer.full_name = full_name
    await customer.save()

    async with state.proxy() as data:
        user_state = data['state']
    if user_state == 'feedback':
        await create_feedback(user_id, state, locale)

    if user_state == 'lead_request':
        await create_lead(user_id, state, locale)
