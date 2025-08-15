# -*- coding: utf-8 -*-
from Tepthon import zedub
from telethon import Button, events

plugin_category = "الادوات"

# عدادات الإعجابات لكل رسالة
like_counts = {}
liked_users = {}

def make_text(count):
    return f"اضغط على الزر لتسجّل إعجابك ❤️🚶\nالإعجابات: {count}"

@zedub.zed_cmd(
    pattern="لايك$",
    command=("like", plugin_category),
    info={
        "header": "زر إعجاب بسيط",
        "description": "يعرض زر إعجاب يمكن الضغط عليه لزيادة العدّاد.",
        "usage": ".لايك",
    },
)
async def _(event):
    # إنشاء رسالة مبدئية مع زر
    msg = await event.edit(
        make_text(0),
        buttons=[[Button.inline("like❤️🚶", data=b"like_btn")]]
    )
    like_counts[msg.id] = 0
    liked_users[msg.id] = set()

# التعامل مع الضغط على زر الإعجاب
@zedub.tgbot.on(events.CallbackQuery(data=b"like_btn"))
async def _(event):
    msg = await event.get_message()
    user_id = event.sender_id

    # تهيئة إذا غير موجود
    if msg.id not in like_counts:
        like_counts[msg.id] = 0
        liked_users[msg.id] = set()

    # منع التكرار
    if user_id in liked_users[msg.id]:
        await event.answer("سبق وسجّلت إعجابك 😉", alert=False)
        return

    liked_users[msg.id].add(user_id)
    like_counts[msg.id] += 1

    # تعديل النص بنفس الرسالة
    await msg.edit(
        make_text(like_counts[msg.id]),
        buttons=[[Button.inline("like❤️🚶", data=b"like_btn")]]
    )
    await event.answer("تم تسجيل إعجابك! ❤️", alert=False)
