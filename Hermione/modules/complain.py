import html
from telegram import Update, Bot, ParseMode
from telegram.ext import run_async
from Hermione.modules.disable import DisableAbleCommandHandler
from Hermione import dispatcher
from requests import get
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton



@run_async
def complain(bot: Bot, update: Update):
  name = update.effective_message.from_user.first_name
  message = update.effective_message
  userid=message.from_user.id
  text = message.text[len('/complain '):]
   

  com_text = f"ꀍꏂꋪꎭꀤꂦꈤꏂ's *New* feedback from [{name}](tg://user?id={userid})\n\nfeed: {text}"
  

  bot.send_message(-1001548071532, com_text, parse_mode=ParseMode.MARKDOWN)
 
  text = html.escape(text)
  reply_text=f"Thankyou for giving ums your feedback."
  message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="You can see your feedback here",url="https://telegram.dog/allukabotfeeds")]]))
                                               
  

  





com_handle = DisableAbleCommandHandler
LIST_HANDLER = DisableAbleCommandHandler("complain", complain)

dispatcher.add_handler(LIST_HANDLER)
