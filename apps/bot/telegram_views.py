from aiogram import types

from apps.bot import dispatcher as dp, bot, messages, keyboards
from apps.lead.states import CustomerForm
from apps.lead.tortoise_models import Customer


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
