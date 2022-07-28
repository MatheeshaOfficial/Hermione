import os
import io
import requests
import shutil 
import random
import re
import glob
import time
import sys
import base64

from bs4 import *
from io import BytesIO
from requests import get
from pyrogram import filters	
from PIL import Image, ImageDraw, ImageFont
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Hermione.services.pyrogram import pbot
from Hermione.function.pluginhelpers import get_text
from Hermione import OWNER_ID, BOT_USERNAME, SUPPORT_CHAT
from Hermione.helper_extra.blogo_helper import download_images, mainne
from Hermione.modules.fsub import ForceSub
"""

# ==================== Logo ====================

@pbot.on_message(filters.command("logo") & ~filters.edited & ~filters.bot)
async def logo(client, message):            
 quew = get_text(message)
 if not quew:
     await client.send_message(message.chat.id, "Please Gimmie A Text For The Logo.")
     return
 mritzme = await client.send_message(message.chat.id, "**Logo In A Process. Please Wait.⏳**")
 try:
    text = get_text(message)
    LOGO_API = f"https://api.singledevelopers.net/logo?name={text}"
    randc = (LOGO_API)
    img = Image.open(io.BytesIO(requests.get(randc).content))
    murl = requests.get(f"https://api.singledevelopers.net/logo?name={text}").history[1].url
    logogend = f"**Logo Generated Successfully**\n**Full resolution Image =>** {murl}"
    fname = "HermioneSlBotLOGO.png"
    img.save(fname, "png")
    await mritzme.edit(logogend, disable_web_page_preview=True)
    await client.send_photo(message.chat.id, photo=murl, caption = f"**Made By @HermioneSlBot ⚡️**")
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await client.send_message(message.chat.id, f'Error, Report @{SUPPORT_CHAT}, {e}')
   

# ==================== HQ Logo ====================
   
@pbot.on_message(filters.command(["hqlogo", "logohq"]) & ~filters.edited & ~filters.bot)
async def hqlogo(client, message):     
 quew = get_text(message)
 if not quew:
     await client.send_message(message.chat.id, "Please Gimmie A Text For The Logo.")
     return
 mritzme = await client.send_message(message.chat.id, "**Logo In A Process. Please Wait.⏳**")
 try:
    text = get_text(message)
    LOGO_API = f"https://api.singledevelopers.net/logohq?name={text}"
    randc = (LOGO_API)
    img = Image.open(io.BytesIO(requests.get(randc).content))
    murl = requests.get(f"https://api.singledevelopers.net/logohq?name={text}").history[1].url
    logogend = f"**Logo Generated Successfully**\n**Full resolution Image =>** {murl}"
    fname = "HermioneSlBotLogo.png"
    img.save(fname, "png")
    await mritzme.edit(logogend, disable_web_page_preview=True)
    await client.send_photo(message.chat.id, photo=murl, caption = f"**Made By @HermioneSlBot⚡️**")
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await client.send_message(message.chat.id, f'Error, Report @{SUPPORT_CHAT}, {e}')

"""
    
# ==================== Brandcrowd Logo ====================    
   
@pbot.on_message(filters.command("brandcrowd") & ~filters.edited & ~filters.bot)
@ForceSub
async def brandcrowd(client, message):
    pablo = await client.send_message(message.chat.id,"**Logo In A Process. Please Wait.⏳**")
    Godzilla = get_text(message)
    if not Godzilla:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    lmao = Godzilla.split(":", 1)
    try:
        typeo = lmao[1]
    except BaseException:
        typeo = "name"
        await pablo.edit(
             "Give name and type for logo Idiot. like `/brandcrowd Hermione:Robot`")
    name = lmao[0]
    mainne(name, typeo)
    caption = "<b>Made By @HermioneSlBot⚡️<b>"
    pate = "logo@HermioneSlBot.jpg"
    await client.send_photo(message.chat.id, pate)
    try:
        os.remove(pate)
    except:
        pass
    await pablo.delete()
    

HELPSTRINGS = """
 Logo Maker
 ╔ /logo [TEXT]: Create a logo
 ╠ /hqlogo [TEXT]: Create a HQ logo
 ╠ /glogo [TEXT] : New Beautiful trending logo
 ╠ /sqlogo [TEXT] : Create Square Logo (For Dp s)
 ╚ /brandcrowd [TEXT : TYPE]: Create logos from brandcrowd.com
 """
__help__ = HELPSTRINGS
__funtools__ = HELPSTRINGS
__mod_name__ = "ʟᴏɢᴏ🎭"
