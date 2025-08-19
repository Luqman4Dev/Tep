import random
import re
import time
import psutil
from datetime import datetime
from platform import python_version

import requests
from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from . import StartTime, zedub, tepversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import zedalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

plugin_category = "العروض"
STATS = gvarstatus("Z_STATS") or "فحص"


@zedub.zed_cmd(pattern=f"{STATS}$")
async def amireallyalive(event):
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    start = datetime.now()
    zedevent = await edit_or_reply(event, "**يتِم فحـص تنصيبـك لـ 𝖳𝖾𝗉𝗍h᥆ᥒ 𔘓  . .**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    if gvarstatus("z_date") is not None:
        zzd = gvarstatus("z_date")
        zzt = gvarstatus("z_time")
        zedda = f"{zzd}┊{zzt}"
    else:
        zedda = f"{bt.year}/{bt.month}/{bt.day}"
    Z_EMOJI = gvarstatus("ALIVE_EMOJI") or "✾╿"
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "**- بوت تيبثـون 𝖳𝖤𝖯𝖳𝖧𝖮𝖭 يعمـل بنجـاح 🌿 ..**"

    # تحضير النص ويا المعلومات
    caption_text = f"""
{ALIVE_TEXT}

{Z_EMOJI} مدة التشغيل : `{uptime}`
{Z_EMOJI} وقت التشغيل : `{zedda}`
{Z_EMOJI} تأخير الاستجابة : `{ms}ms`
{Z_EMOJI} نسخة بايثون : `{python_version()}`
{Z_EMOJI} نسخة تيليثون : `{version.__version__}`
{Z_EMOJI} نسخة تيبثون : `{tepversion}`
"""

    # ارسال صورة ويا التفاصيل
    photo_url = "https://raw.githubusercontent.com/dev-source1/Tep/main/IMG_20250818_192518_860.jpg"
    await event.client.send_file(
        event.chat_id,
        photo_url,
        caption=caption_text,
        reply_to=reply_to_id
    )

    await zedevent.delete()
