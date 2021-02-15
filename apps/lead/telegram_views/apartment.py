from aiogram.types import ContentType

from apps.bot import dispatcher as dp
from apps.bot.telegram_views import send_main_menu
from apps.bot.tortoise_models import Button
from apps.lead import callback_filters
from apps.lead.states import CustomerForm
from apps.lead.tortoise_models import Customer

