from telethon.utils import pack_bot_file_id

from Tepthon import zedub
from Tepthon.core.logger import logging
from ..helpers.utils import _format, get_user_from_event
from ..core.managers import edit_delete, edit_or_reply

plugin_category = "الادوات"

LOGS = logging.getLogger(__name__)


@zedub.zed_cmd(
    pattern="(الايدي|id)(?:\s|$)([\s\S]*)",
    command=("id", plugin_category),
    info={
        "header": "To get id of the group or user.",
        "description": "if given input then shows id of that given chat/channel/user else if you reply to user then shows id of the replied user \
    along with current chat id and if not replied to user or given input then just show id of the chat where you used the command",
        "usage": "{tr}id <reply/username>",
    },
)
# like_userbot.py
# سكربت Telethon (Userbot) يضيف زر "لايك 🚶❤️" عند كتابة الأمر .لايك
# ملاحظة: لا توجد إمكانية لجعل الزر "شفّاف" فعلياً في تيليجرام

import os
import asyncio
from telethon import TelegramClient, events, Button

# ======== عيّن هنا أو استخدم متغيرات بيئية ==========
API_ID = int(os.getenv("API_ID", "123456"))          # عدّل هنا أو صدّر ENV
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")    # عدّل هنا أو صدّر ENV
# ===================================================

client = TelegramClient("like_userbot_session", API_ID, API_HASH)

# عدّادات في الذاكرة (message.id -> count) و (message.id -> set(user_id))
like_counts = {}
liked_users = {}

def make_text(base_text: str, count: int) -> str:
    """بناء النص الذي سيعرض فوق/تحته الزر"""
    base = base_text.strip() or "اضغط الزر لتسجيل إعجابك"
    return f"{base}\n\nالإعجابات: {count} ❤️"

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.لايك(?:\s+(.+))?$'))
async def on_like_command(event):
    """
    عند كتابة:
    .لايك
    أو
    .لايك نص هنا
    سيتم تعديل نفس الرسالة لإضافة زر لايك
    """
    # الحصول على النص المرافق للأمر (إن وُجد)
    m = event.pattern_match.group(1) or ""
    base_text = m.strip()

    # نحرّر الرسالة الأصلية (التي كتبتها) بحيث تصبح النص الجديد + زر
    try:
        # نحرّك إلى نص أولي مع عدّاد صفر
        edited = await event.edit(make_text(base_text, 0),
                                  buttons=[[Button.inline("لايك 🚶❤️", b"like")]])
    except Exception as e:
        await event.reply("خطأ أثناء إضافة الزر: " + str(e))
        return

    # تهيئة العدّادات للرسالة المعدّلة
    like_counts[edited.id] = 0
    liked_users[edited.id] = set()

@client.on(events.CallbackQuery(data=b"like"))
async def on_like_press(event):
    """
    التعامل مع الضغط على زر الإعجاب.
    يمنع تكرار الإعجاب من نفس المستخدم على نفس الرسالة.
    حدّث النص لعرض العدّاد.
    """
    # من ضغط؟ ومن أي رسالة؟
    user_id = event.sender_id
    msg = await event.get_message()
    msg_id = msg.id

    # تهيئة إذا لم تكن موجودة (مثلاً لو الرسالة أُرسلت بطريقة أخرى)
    if msg_id not in like_counts:
        like_counts[msg_id] = 0
        liked_users[msg_id] = set()

    # منع التكرار
    if user_id in liked_users[msg_id]:
        # نُعلم المستخدم أنه سبق صوّت (غير مزعج)
        await event.answer("سبق سجلت إعجابك 😉", alert=False)
        return

    # تسجيل الإعجاب
    liked_users[msg_id].add(user_id)
    like_counts[msg_id] += 1
    new_count = like_counts[msg_id]

    # إعادة تحرير الرسالة لعرض العدد الجديد (نحافظ على نفس الزر)
    try:
        # نحاول استخراج النص الأصلي قبل السطر "الإعجابات" إن أمكن
        # إن لم نتمكن، نستخدم نص افتراضي بسيط
        raw_text = msg.text or ""
        # نفصل النص عند سطر "الإعجابات:" إن وُجد
        parts = raw_text.split("\n\nالإعجابات:")
        base_text = parts[0] if parts else raw_text

        await msg.edit(make_text(base_text, new_count),
                       buttons=[[Button.inline("لايك 🚶❤️", b"like")]])
    except Exception:
        # إذا لم نتمكن من التعديل (مثلاً قديمة أو صلاحيات)، نعرض تنبيه للمستخدم
        await event.answer(f"الإعجابات الآن: {new_count} ❤️", alert=True)
        return

    # ردّ سريع للمستخدم الذي ضغط
    await event.answer("تم تسجيل إعجابك! ❤️", alert=False)

def main():
    print("تشغيل userbot... اتّصل الآن بحسابك.")
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    main()
