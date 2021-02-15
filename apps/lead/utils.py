from apps.lead.tortoise_models import Lead


async def delete_unconfirmed_leads(user_id):
    await Lead.filter(customer_id=user_id, completed_at__isnull=True).delete()


