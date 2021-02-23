from apps.bot import dispatcher as dp, bot, messages, keyboards
from apps.bot.utils import try_delete_message
from apps.lead import callback_filters
from apps.lead.states import LeadForm
from apps.lead.tortoise_models import Apartment, File, LeadApartmentFile, Photo, LeadApartmentPhoto, Video, \
    LeadApartmentVideo


@dp.callback_query_handler(callback_filters.residence_choice, state=LeadForm.residence_choice.state)
async def residence_choice(query, state, locale):
    user_id = query.from_user.id
    residence_id = int(query.data.split(':')[1])

    async with state.proxy() as data:
        data['residence_id'] = residence_id

    message = await messages.get_message('room_quantity', locale)
    keyboard = keyboards.apartment_choice(residence_id, locale)

    await try_delete_message(user_id, query.message.message_id)
    await bot.send_message(user_id, message, reply_markup=await keyboard)

    await LeadForm.apartment_choice.set()


@dp.callback_query_handler(callback_filters.apartment_choice, state=LeadForm.apartment_choice.state)
async def apartment_choice(query, state, locale):
    user_id = query.from_user.id
    apartment_id = int(query.data.split(':')[1])

    async with state.proxy() as data:
        data['apartment_id'] = apartment_id

    apartment = await Apartment.get(pk=apartment_id)
    files = await File.filter(
        id__in=await LeadApartmentFile.filter(apartment_id=apartment_id).values_list('file_id', flat=True)
    ).distinct()
    photos = await Photo.filter(
        id__in=await LeadApartmentPhoto.filter(apartment_id=apartment_id).values_list('photo_id', flat=True)
    ).distinct()
    videos = await Video.filter(
        id__in=await LeadApartmentVideo.filter(apartment_id=apartment_id).values_list('video_id', flat=True)
    ).distinct()

    if photos:
        for photo in photos:
            with open(photo.get_path(), 'rb') as photo_data:
                await bot.send_photo(user_id, photo_data, caption=getattr(photo, f'description_{locale}'))

    if videos:
        for video in videos:
            with open(video.get_path(), 'rb') as video_data:
                await bot.send_video(user_id, video_data, caption=getattr(video, f'description_{locale}'))

    if files:
        for file in files:
            with open(file.get_path(), 'rb') as file_data:
                await bot.send_document(user_id, file_data, caption=getattr(file, f'description_{locale}'))

    keyboard = await keyboards.lead_request(apartment_id, locale)
    await bot.send_message(user_id, getattr(apartment, f'description_{locale}'), reply_markup=keyboard)
    await LeadForm.lead_request.set()
