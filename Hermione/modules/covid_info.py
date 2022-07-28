import requests
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async

from Hermione import dispatcher
from Hermione.modules.disable import DisableAbleCommandHandler


@run_async
def covid(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text.split(" ", 1)
    if len(text) == 1:
        r = requests.get("https://corona.lmao.ninja/v2/all").json()
        reply_text = f"**Global Totals** 🦠\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
    else:
        variabla = text[1]
        r = requests.get(f"https://corona.lmao.ninja/v2/countries/{variabla}").json()
        reply_text = f"**Cases for {r['country']} 🦠**\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)


COVID_HANDLER = DisableAbleCommandHandler(["covid", "corona"], covid)
dispatcher.add_handler(COVID_HANDLER)

__mod_name__ = "ᴄᴏᴠɪᴅ🦠"

HELPSTRINGS = """
• `/covid`** <songname artist(optional)>: download the song in it's best quality available.(API BASED)
Commands     
• /covid - To Get Global Stats of Covid.
• /covid [COUNTRY] - To Get Stats of A Single Country.
• /corona - Same as `/covid`
"""
__help__ = HELPSTRINGS
__funtools__ = HELPSTRINGS
