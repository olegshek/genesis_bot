from apps.bot import dispatcher as dp, bot, messages, keyboards
from apps.bot.utils import try_delete_message
from apps.lead import callback_filters
from apps.lead.states import LeadForm, CustomerForm
from apps.lead.tortoise_models import Apartment, Customer


@dp.callback_query_handler(callback_filters.residence_choice, state=LeadForm.residence_choice)
def residence_choice(query, state, locale):
    user_id = query.from_user.id
    residence_id = int(query.data.split(':')[1])

    async with state.proxy() as data:
        data['residence_id'] = residence_id

    message = await messages.get_message('room_quantity', locale)
    keyboard = await keyboards.room_quantity_choice(residence_id, locale)
    await bot.edit_message_text(message, user_id, query.message.message_id, reply_markup=keyboard)


@dp.callback_query_handler(callback_filters.room_quantity_choice, state=LeadForm.room_quantity_choice)
def room_quantity_choice(query, state, locale):
    user_id = query.from_user.id
    room_quantity_id = int(query.data.split(':')[1])

    async with state.proxy() as data:
        data['room_quantity_id'] = room_quantity_id
        residence_id = data['residence_id']

    message = await messages.get_message('apartment_choice', locale)
    keyboard = keyboards.apartment_choice(residence_id, room_quantity_id, locale)
    await bot.edit_message_text(message, user_id, query.message.message_id, reply_markup=keyboard)

    await LeadForm.apartment_choice.set()


@dp.callback_query_handler(callback_filters.apartment_choice, state=LeadForm.apartment_choice)
def apartment_choice(query, state, locale):
    user_id = query.from_user.id
    apartment_id = int(query.data.split(':')[1])

    async with state.proxy() as data:
        data['apartment_id'] = apartment_id

    apartment = await Apartment.get(pk=apartment_id)
    files = await apartment.files.all()
    photos = await apartment.photos.all()

    if files:
        if await files.count() > 1:
            try_delete_message(user_id, query.message.message_id)
            bot.send_media_group(user_id, list(map(lambda file: file.get_url, files)))

    if photos:
        if await photos.count() > 1:
            try_delete_message(user_id, query.message.message_id)
            bot.send_media_group(user_id, list(map(lambda photo: photo.get_url, photos)))

    await bot.send_message(user_id, apartment.description, reply_markup=keyboards.lead_request(apartment_id, locale))
    await LeadForm.lead_request.set()


