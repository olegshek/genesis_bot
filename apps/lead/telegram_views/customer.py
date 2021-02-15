from apps.bot import dispatcher as dp
from apps.bot.tortoise_models import KeyboardButtonsOrdering
from apps.lead import callback_filters
from apps.lead.states import CustomerForm
from apps.lead.tortoise_models import Customer


@dp.message_handler(callback_filters.language_choice, state=CustomerForm.language_choice)
async def language_choice_processing(message, locale, state):
    user_id = message.from_user.id
    text = message.text
    lang_buttons = await KeyboardButtonsOrdering.filter(keyboard__name='language_choice')

    language = 'en'

    for keyboard_button in lang_buttons:
        button = await keyboard_button.button

        if text == button.text:
            language = button.code

    await Customer.filter(id=user_id).update(language=language)
