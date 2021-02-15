from django.conf import settings

from apps.lead.tortoise_models import Lead


async def delete_unconfirmed_leads(user_id):
    await Lead.filter(customer_id=user_id, confirmed_at__isnull=True).delete()


