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
async def _(event):
    "To get id of the group or user."
    if input_str := event.pattern_match.group(2):
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{e}`", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"**⎉╎ايـدي المستخـدم**  `{input_str}` **هـو** `{p.id}`"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"**⎉╎ايـدي المستخـدم**  `{p.title}` **هـو** `{p.id}`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "**⎉╎أدخل إما اسم مستخدم أو الرد على المستخدم**")
    elif event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                f"**⎉╎ايـدي الدردشـه : **`{event.chat_id}`\n\n**⎉╎ايـدي المستخـدم : **`{r_msg.sender_id}`\n\n**⎉╎ايـدي الميديـا : **`{bot_api_file_id}`",
            )

        else:
            await edit_or_reply(
                event,
                f"**⎉╎ايـدي الدردشـه : **`{event.chat_id}`\n\n**⎉╎ايـدي المستخـدم : **`{r_msg.sender_id}`",
            )

    else:
        await edit_or_reply(event, f"**⎉╎ايـدي الدردشـه : **`{event.chat_id}`")


@zedub.zed_cmd(
    pattern="رابطه(?:\s|$)([\s\S]*)",
    command=("رابطه", plugin_category),
    info={
        "header": "لـ جـلب اسـم الشخـص بشكـل ماركـدون ⦇.رابطه بالـرد او + معـرف/ايـدي الشخص⦈ ",
        "الاسـتخـدام": "{tr}رابطه <username/userid/reply>",
    },
)
async def permalink(event):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(event)
    if not user:
        return
    if custom:
        return await edit_or_reply(event, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(event, f"[{tag}](tg://user?id={user.id})")


@zedub.zed_cmd(pattern="اسمي$")
async def permalink(event):
    user = await event.client.get_me()
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(event, f"[{tag}](tg://user?id={user.id})")


@zedub.zed_cmd(
    pattern="اسمه(?:\s|$)([\s\S]*)",
    command=("اسمه", plugin_category),
    info={
        "header": "لـ جـلب اسـم الشخـص بشكـل ماركـدون ⦇.اسمه بالـرد او + معـرف/ايـدي الشخص⦈ ",
        "الاسـتخـدام": "{tr}اسمه <username/userid/reply>",
    },
)
async def permalink(event):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(event)
    if not user:
        return
    if custom:
        return await edit_or_reply(event, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(event, f"[{tag}](tg://user?id={user.id})")

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