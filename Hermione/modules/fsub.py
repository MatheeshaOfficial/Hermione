from functools import wraps
from Hermione.services.pyrogram import pbot as bot
import pyrogram
from pyrogram import filters, idle
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from typing import Optional
# from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

FTEXT = """⛔️ **Access Denied** ⛔️
🙋‍♂️ Hey There, You Must Join [My Channel](t.me/Hermione_Updates)🥀 To Use This Tool. So, Please Join it & Try Again🌹. Thank You 🔥
"""
CAPTION_BTN = InlineKeyboardMarkup(
            [[InlineKeyboardButton("☘️ Join Channel", url="https://t.me/Hermione_Updates")]])

def ForceSub(func):
    @wraps(func)
    async def bot_message(_, message):
        try:
            await message._client.get_chat_member(-1001191609062, message.from_user.id)
        except UserNotParticipant:
            return await message.reply_text(
                        text=FTEXT,
                        reply_markup=CAPTION_BTN,
                        disable_web_page_preview=True) 
        return await func(_, message)    
    return bot_message
