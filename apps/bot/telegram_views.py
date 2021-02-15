from aiogram import types

from apps.bot import dispatcher as dp, bot, messages, keyboards, callback_filters
from apps.bot.messages import get_message
from apps.bot.states import BotForm
from apps.lead.states import CustomerForm, LeadForm
from apps.lead.tortoise_models import Customer
from apps.lead.utils import delete_unconfirmed_leads


async def send_main_menu(customer, locale):
    if not customer.phone_number:
        message_title = 'phone_number'
        keyboard = keyboards.phone_number
        state = CustomerForm.phone_number
    else:
        message_title = 'main_menu'
        keyboard = keyboards.main_menu
        state = BotForm.main_menu

    await bot.send_message(
        customer.id,
        await messages.get_message(message_title, locale),
        reply_markup=await keyboard(locale)
    )
    await state.set()


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, locale):
    user_id = message.from_user.id
    customer = await Customer.filter(id=user_id).first()
    if not customer:
        await Customer.create(id=user_id, username=message.from_user.username)

    await bot.send_message(user_id, await messages.get_message('greeting', locale),
                           reply_markup=keyboards.remove_keyboard)

    if not customer.language:
        await CustomerForm.language_choice.set()
        return await bot.send_message(user_id, await messages.get_message('language_choice', locale),
                                      reply_markup=await keyboards.language_choice(locale, False))

    await send_main_menu(customer, locale)


@dp.callback_query_handler(callback_filters.main_menu, state=BotForm.main_menu)
async def main_menu(query, locale):
    user_id = query.from_user.id

    await delete_unconfirmed_leads(user_id)

    if query.data == 'residence_choice':
        message = get_message('residence_choice', locale)
        keyboard = keyboards.residence_choice(locale)
        state = LeadForm.residence_choice

        await bot.edit_message_text(await message, user_id, query.message.message_id, reply_markup=await keyboard)
        await state.set()
