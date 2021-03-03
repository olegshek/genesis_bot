from aiogram import types
from aiogram.utils.exceptions import MessageNotModified, TelegramAPIError

from apps.bot import dispatcher as dp, bot, messages, keyboards, callback_filters
from apps.bot.callback_filters import keyboard_back, inline_back
from apps.bot.messages import get_message
from apps.bot.states import BotForm
from apps.bot.utils import try_delete_message
from apps.information.states import InformationForm
from apps.information.tortoise_models import InformationPhoto, InformationFile, InformationText, InformationVideo
from apps.lead.states import CustomerForm, LeadForm
from apps.lead.tortoise_models import Customer, Apartment, Residence


async def back(user_id, state, locale, message_id=None):
    state_name = await state.get_state()
    customer = await Customer.get(id=user_id)

    async with state.proxy() as data:
        user_data = data.get('state', None)

    if state_name in [LeadForm.residence_choice.state, InformationForm.information_state.state] or \
            (state_name == CustomerForm.full_name.state and user_data == 'feedback'):
        if message_id:
            await try_delete_message(user_id, message_id)

        await send_main_menu(customer, locale, state)

    try:
        if state_name == LeadForm.apartment_choice.state:
            await send_residence_choice(user_id, message_id, locale)

        if state_name == LeadForm.lead_request.state:
            async with state.proxy() as data:
                residence_id = data['residence_id']

            message_text = await messages.get_message('apartment_choice', locale)
            keyboard = await keyboards.apartment_choice(residence_id, locale)
            await bot.edit_message_text(message_text, user_id, message_id, reply_markup=keyboard)
            await LeadForm.apartment_choice.set()

        if state_name == CustomerForm.full_name.state and user_data == 'lead_request':
            async with state.proxy() as data:
                apartment_id = data['apartment_id']

            apartment = await Apartment.get(id=apartment_id)
            keyboard = await keyboards.lead_request(apartment_id, locale)
            await bot.send_message(user_id, getattr(apartment, f'description_{locale}'), reply_markup=keyboard)
            await LeadForm.lead_request.set()

    except MessageNotModified:
        pass

    except TelegramAPIError:
        await send_main_menu(customer, locale, state)


async def send_main_menu(customer, locale, state=None):
    if state:
        await state.finish()

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


async def send_residence_choice(user_id, message_id, locale):
    message = await get_message('residence_choice', locale)

    await try_delete_message(user_id, message_id)
    await bot.send_message(user_id, message)

    residences = await Residence.all().order_by(f'name_{locale}')
    residences_len = len(residences)

    for residence in residences:
        is_last = True if residences.index(residence) == residences_len - 1 else False
        keyboard = await keyboards.residence_choice(residence, locale, is_last)
        photo = await residence.photo
        residence_name = getattr(residence, f'name_{locale}')
        residence_description = getattr(photo, f'description_{locale}')
        text = f'<b>{residence_name}</b>\n\n' \
               f'{residence_description}'

        with open(photo.get_path(), 'rb') as photo_data:
            await bot.send_photo(
                user_id,
                photo_data,
                caption=text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )

    await LeadForm.residence_choice.set()


@dp.message_handler(keyboard_back, state='*')
async def button_back(message, state, locale):
    user_id = message.from_user.id

    await bot.send_message(user_id, '🔙', reply_markup=keyboards.remove_keyboard)
    await back(message.from_user.id, state, locale)


@dp.callback_query_handler(inline_back, state='*')
async def back_inline(query, state, locale):
    await back(query.from_user.id, state, locale, query.message.message_id)


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, locale):
    user_id = message.from_user.id
    customer = await Customer.filter(id=user_id).first()
    if not customer:
        customer = await Customer.create(id=user_id, username=message.from_user.username)

    await bot.send_message(user_id, await messages.get_message('greeting', locale),
                           reply_markup=keyboards.remove_keyboard)

    if not customer.language:
        await CustomerForm.language_choice.set()
        return await bot.send_message(user_id, await messages.get_message('language_choice', locale),
                                      reply_markup=await keyboards.language_choice(locale, False))

    await send_main_menu(customer, locale)


@dp.callback_query_handler(callback_filters.main_menu, state=BotForm.main_menu.state)
async def main_menu(query, locale, state):
    from apps.lead.telegram_views.customer import create_feedback

    user_id = query.from_user.id
    customer = await Customer.get(id=user_id)

    if query.data == 'object_choice':
        await send_residence_choice(user_id, query.message.message_id, locale)

    if query.data == 'link_with_me':
        if not customer.full_name:
            async with state.proxy() as data:
                data['state'] = 'feedback'

            message = await messages.get_message('full_name', locale)
            await try_delete_message(user_id, query.message.message_id)

            await bot.send_message(user_id, query.message.text)
            await bot.send_message(user_id, message, reply_markup=await keyboards.back_keyboard(locale))

            await CustomerForm.full_name.set()
        else:
            await create_feedback(user_id, state, locale, query.message.message_id)

    if query.data == 'change_language':
        await CustomerForm.language_choice.set()
        return await bot.send_message(user_id, await messages.get_message('language_choice', locale),
                                      reply_markup=await keyboards.language_choice(locale, False))

    if query.data == 'about_company':
        photos = await InformationPhoto.all()
        videos = await InformationVideo.all()
        files = await InformationFile.all()
        texts = await InformationText.all()

        for photo in photos:
            photo = await photo.photo
            with open(photo.get_path(), 'rb') as photo_data:
                await bot.send_photo(user_id, photo_data, caption=getattr(photo, f'description_{locale}'))

        for video in videos:
            video = await video.video
            with open(video.get_path(), 'rb') as video_data:
                await bot.send_video(user_id, video_data, caption=getattr(video, f'description_{locale}'))

        for file in files:
            file = await file.file
            with open(file.get_path(), 'rb') as file_data:
                await bot.send_document(user_id, file_data)

        keyboard = await keyboards.back_keyboard(locale)
        for text in texts:
            await bot.send_message(user_id, getattr(text, f'text_{locale}'), reply_markup=keyboard, parse_mode='HTML')

        await InformationForm.information_state.set()
