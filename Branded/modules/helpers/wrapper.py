from pyrogram.types import *
from traceback import format_exc

from ...console import SUDOERS
from ..clients.clients import app, bot

def super_user_only(mystic):
    async def wrapper(client, message):
        try:
            if message.from_user.is_self:
                return await mystic(client, message)
        except:
            if message.outgoing:
                return await mystic(client, message)
            
    return wrapper



def sudo_users_only(mystic):
    async def wrapper(client, message):
        try:
            if (message.from_user.is_self or
               message.from_user.id in SUDOERS
            ):
                return await mystic(client, message)
        except:
            if (message.outgoing or
               message.from_user.id in SUDOERS
            ):
                return await mystic(client, message)
            
    return wrapper
    

def cb_wrapper(func):
    async def wrapper(bot, cb):
        sudousers = SUDOERS
        if (cb.from_user.id != app.me.id and
            cb.from_user.id not in sudousers
        ):
            return await cb.answer(
                "❎ You Are Not A Sudo User❗",
                cache_time=0,
                show_alert=True,
            )
        else:
            try:
                return await func(bot, cb)
            except Exception:
                print(format_exc())
                return await cb.answer(
                    f"❎ Something Went Wrong, Please Check Logs❗..."
                )
        
    return wrapper


def inline_wrapper(func):
    from ... import __version__
    async def wrapper(bot, query):
        sudousers = SUDOERS
        if (query.from_user.id != app.me.id and
            query.from_user.id not in sudousers
        ):
            try:
                button = [
                    [
                        InlineKeyboardButton(
                            "💥 Deploy  ✨",
                            url=f"https://github.com"
                        )
                    ]
                ]
                await bot.answer_inline_query(
                    query.id,
                    cache_time=1,
                    results=[
                        (
                            InlineQueryResultPhoto(
                                photo_url=f"https://graph.org/file/78dce13fe7648784e9260-846be6d7c1bed528c2.jpg",
                                title="🥀 Branded Userbot ✨",
                                thumb_url=f"https://graph.org/file/78dce13fe7648784e9260-846be6d7c1bed528c2.jpg",
                                description=f"🌷 Deploy Your Own -Userbot 🌿...",
                                caption=f"<b>🥀 Welcome » To »  🌷\n✅ Userbot {__version__} ✨...</b>",
                                reply_markup=InlineKeyboardMarkup(button),
                            )
                        )
                    ],
                )
            except Exception as e:
                print(str(e))
                await bot.answer_inline_query(
                    query.id,
                    cache_time=1,
                    results=[
                        (
                            InlineQueryResultArticle(
                                title="",
                                input_message_content=InputTextMessageContent(
                                    f"||**🥀 Please, Deploy Your Own Branded Userbot❗...\n\nRepo:** <i>https://github.com/WCGKING/KINGUSERBOT/</i>||"
                                ),
                            )
                        )
                    ],
                )
            except Exception as e:
                print(str(e))
                pass
        else:
           return await func(bot, query)

    return wrapper

