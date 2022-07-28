import os
import time
import requests
from pyrogram import filters
from pyrogram.types import Message
from Hermione.services.pyrogram import pbot
from Hermione.conf import get_str_key
from Hermione.function.pluginhelpers import (
    edit_or_reply,
    progress,
    edit_or_send_as_file,
    get_text,
    admins_only,
)

V_T_KEY = get_str_key("V_T_KEY") # String
vak = V_T_KEY

@pbot.on_message(filters.command(['vt', 'scan']) & ~filters.edited & ~filters.bot)
@admins_only
async def scan_my_file(client, message):
    ms_ = await edit_or_reply(message, "`Please Wait! Scanning This File`")
    if not message.reply_to_message:
      return await ms_.edit("`Please Reply To File To Scan For Viruses`")
    if not message.reply_to_message.document:
      return await ms_.edit("`Please Reply To File To Scan For Viruses`")
    if not vak:
      return await ms_.edit("`You Need To Set VIRUSTOTAL_API_KEY For Functing Of This Plugin.`")
    if int(message.reply_to_message.document.file_size) > 25000000:
      return await ms_.edit("`File Too Large , Limit is 25 Mb`")
    c_time = time.time()
    downloaded_file_name = await message.reply_to_message.download(progress=progress, progress_args=(ms_, c_time, f"`Downloading This File!`"))
    url = "https://www.virustotal.com/vtapi/v2/file/scan"
    params = {"apikey": vak}
    files = {"file": (downloaded_file_name, open(downloaded_file_name, "rb"))}
    response = requests.post(url, files=files, params=params)
    try:
       r_json = response.json()
       scanned_url = r_json["permalink"]
    except:
      return await ms_.edit(f"`[{response.status_code}] - Unable To Scan File.`")
    await ms_.edit(f"<b><u>Hermione #Scanned {message.reply_to_message.document.file_name}</b></u>. <b>You Can Visit :</b> {scanned_url} <b>In 5-10 Min To See File Report</b> Or Type `/webshot {scanned_url}` to get screenshot of this file report \nJoin @HermioneSupport_Official to know more")
   
HELPSTRINGS = """
*Virus Scan* 
 - /scanit: Scan a file for virus (MAX SIZE = 25MB)
"""
__mod_name__ = "ᴠɪʀᴜꜱ ꜱᴄᴀɴɴᴇʀ🔎"
__help__ = HELPSTRINGS
__advtools__ = HELPSTRINGS
