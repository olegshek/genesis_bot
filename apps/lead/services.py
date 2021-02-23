import asyncio

import aiohttp
from django.conf import settings


async def send_to_bitrix(instance):
    customer = await instance.customer

    data = {
        "TITLE": str(instance.number),
        "NAME": customer.full_name,
        "STATUS_ID": "NEW",
        "OPENED": "Y",
        "ASSIGNED_BY_ID": 1,
        "CURRENCY_ID": "USD",
        "OPPORTUNITY": 0,
        "PHONE": [{"VALUE": str(customer.phone_number), "VALUE_TYPE": "MOBILE"}]
    }

    async with aiohttp.ClientSession(timeout=3) as session:
        for i in range(5):
            try:
                async with session.post(settings.BITRIX_URL, data=data) as resp:
                    if resp.status not in [200, 201]:
                        await asyncio.sleep(1.5)
                        continue
            except Exception:
                await asyncio.sleep(1.5)
                continue
