from apps.bot import messages, bot, keyboards
from apps.lead import callback_filters
from apps.lead.states import LeadForm, CustomerForm
from apps.lead.tortoise_models import Customer


@dp.callback_query_handler(callback_filters.lead_request, state=LeadForm.lead_request)
def lead_request(query, state, locale):
    user_id = query.from_user.id
    customer = await Customer.get(id=user_id)

    async with state.proxy() as data:
        data['state'] = 'lead_request'

    if not customer.full_name:
        message = await messages.get_message('full_name', locale)
        await bot.edit_message_reply_markup(user_id, query.message.message_id, reply_markup=keyboards.remove_keyboard)
        await bot.send_message(user_id, message, reply_markup=keyboards.back_keyboard(locale))

        await CustomerForm.full_name.set()