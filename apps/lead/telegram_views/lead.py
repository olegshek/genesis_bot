from apps.bot import messages, bot, keyboards
from apps.bot.telegram_views import send_main_menu
from apps.bot.utils import try_delete_message
from apps.lead import callback_filters
from apps.lead.states import LeadForm, CustomerForm
from apps.bot import dispatcher as dp
from apps.lead.tortoise_models import Customer, Lead


async def create_lead(user_id, state, locale, message_id=None, text=None):
    async with state.proxy() as data:
        apartment_id = data['apartment_id']

    lead = await Lead.create(customer_id=user_id, apartment_id=apartment_id)
    await lead.send_lead_to_bitrix()

    if state != CustomerForm.full_name.state and message_id:
        await try_delete_message(user_id, message_id)
        await bot.send_message(user_id, text)

    message = await messages.get_message('request_accepted', locale)
    await bot.send_message(user_id, message, reply_markup=keyboards.remove_keyboard)

    message = await messages.get_message('request_number', locale) + f' {lead.number}'
    await bot.send_message(user_id, message, reply_markup=keyboards.remove_keyboard)

    customer = await Customer.get(id=user_id)
    await send_main_menu(customer, locale, state)


@dp.callback_query_handler(callback_filters.lead_request, state=LeadForm.lead_request.state)
async def lead_request(query, state, locale):
    user_id = query.from_user.id
    customer = await Customer.get(id=user_id)

    async with state.proxy() as data:
        data['state'] = 'lead_request'
        data['apartment_id'] = int(query.data.split(':')[1])

    if not customer.full_name:
        message = await messages.get_message('full_name', locale)
        await try_delete_message(user_id, query.message.message_id)
        await bot.send_message(user_id, query.message.text)
        await bot.send_message(user_id, message, reply_markup=await keyboards.back_keyboard(locale))
        await CustomerForm.full_name.set()
        return

    await create_lead(user_id, state, locale, query.message.message_id, query.message.text)
