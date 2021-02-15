from apps.bot.tortoise_models import KeyboardButtonsOrdering


async def callback_filter(query, keyboard_name):
    buttons = map(
        str,
        await KeyboardButtonsOrdering.filter(keyboard__name=keyboard_name).values_list('button__name', flat=True)
    )
    return query.data in buttons
