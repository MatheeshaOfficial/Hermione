import sys
from Hermione.utils.logger import log
from pyrogram import Client
from Hermione.conf import get_int_key, get_str_key

STRING_SESSION = get_str_key("P_SESSION")
API_ID = get_int_key("API_ID", required=True)
API_HASH = get_str_key("API_HASH", required=True)

pubot = Client(STRING_SESSION, api_id=API_ID, api_hash=API_HASH)
try:
    ubot.start()
    log.info("☘️ Hermione Userbot Starting 🍁")
except Exception as e:
    pass
