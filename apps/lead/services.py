import asyncio
import json
import logging
import sys

import aiohttp
from django.conf import settings

logger = logging.getLogger('telegram')


async def send_to_bitrix(instance):
    from apps.lead.tortoise_models import Lead

    customer = await instance.customer

    data = {
        "fields": {
            "TITLE": str(instance.number),
            "NAME": customer.full_name,
            "STATUS_ID": "NEW",
            "OPENED": "Y",
            "ASSIGNED_BY_ID": 1,
            "PHONE": [{"VALUE": str(customer.phone_number), "VALUE_TYPE": "MOBILE"}],
            "COMMENTS": "Просьба связаться с клиентом"
        }
    }

    if isinstance(instance, Lead):
        apartment = await instance.apartment
        residence = await apartment.residence
        room_quantity = await apartment.room_quantity

        data['fields']["COMMENTS"]: f"Интересует {room_quantity.quantity}-комантная квартира в ЖК {residence.name_ru}"

    async with aiohttp.ClientSession(json_serialize=json.dumps) as session:
        for i in range(5):
            try:
                async with session.post(settings.BITRIX_URL, json=data) as resp:

                    logger.info(
                        f'url={resp.url}, request_data={data}, status={resp.status}, content={await resp.text()}'
                    )

                    if resp.status not in [200, 201]:
                        await asyncio.sleep(1.5)
                        continue
                    return

            except Exception as ex:
                logger.error(
                    'Internal Server Error',
                    exc_info=sys.exc_info()
                )
