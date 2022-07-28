import importlib
import time
import re
import random
from sys import argv
from typing import Optional
from pyrogram import filters, idle

from Hermione import (
    ALLOW_EXCL,
    CERT_PATH,
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    PORT,
    SUPPORT_CHAT,
    TOKEN,
    URL,
    WEBHOOK,
    SUPPORT_CHAT,
    dispatcher,
    StartTime,
    telethn,
    updater,
    pbot,
)
# from Hermione.services.pyrogram import pbot
from Hermione.events import register
# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from Hermione.modules import ALL_MODULES
from Hermione.modules.helper_funcs.chat_status import is_user_admin
from Hermione.modules.helper_funcs.misc import paginate_modules
from Hermione.modules.sudoers import bot_sys_stats
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = f"""
*Hello 👋*    
\n*I'm Hermione Jean Granger ❤*
\nɪ'ᴍ ᴘᴏᴡᴇʀꜰᴜʟʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇʀ ʙᴏᴛ ᴡɪᴛʜ ᴄᴏᴏʟ ᴍᴏᴅᴜʟᴇꜱ
\nHit /help to find my list of available commands
"""

buttons = [
    [
        InlineKeyboardButton(
            text="➕️ ᴀᴅᴅ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕️", url="t.me/HermioneSlBot?startgroup=true"),
    ],
    [
        InlineKeyboardButton(text="ᴀʙᴏᴜᴛ ⚠", callback_data="hermione_"),
        InlineKeyboardButton(
            text="ꜱᴜᴘᴘᴏʀᴛ 🎭", url=f"https://t.me/HermioneSupport_Official"
        ),
    ],
    [
        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇꜱ 📲", url=f"https://t.me/Hermione_updates"),
        InlineKeyboardButton(
            text="ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛᴇꜱ💻", callback_data="stats_callback"
        ),
    ],
    [
        InlineKeyboardButton(text="⁉ ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅꜱ ⁉", callback_data="helpmenu_"),
    ],
]


STICKERS = (
    "CAACAgUAAxkBAAIivWDr2T0buc1xq8Sschbe2OqgMiruAALQAwACZupgVztQDgABVViikx4E",
    "CAACAgUAAxkBAAIivmDr2U2tWmIwlN0FfBgsC5dpzP1tAALVAwACf8NgV9WDkUEV1bV7HgQ",
    "CAACAgUAAxkBAAIiv2Dr2VfYnGTRK1m7HrblirkAASWEkQACngMAAr2uYFdfOOy7PanETh4E",
    "CAACAgUAAxkBAAIiwGDr2W-R0BHMivAsBbsm4lTn77zmAAJJBAAClbxhV02b12_bQE8_HgQ",
    "CAACAgUAAxkBAAIiwWDr2XZE7HRx-CvtXf0tJK5-FbufAALjAgACEJRgVwlEAaqcX_qqHgQ",
    "CAACAgUAAxkBAAIiwmDr2X3tCHzCp53-5gbBQNbdYVPsAAIwBAACimZgV1j0HuTR_ej6HgQ",
    "CAACAgUAAxkBAAIiw2Dr2YVHF4gvDkn3SP9D9WdIKyawAALGAwACe6hhV84cO0her4U8HgQ",
    "CAACAgUAAxkBAAIixGDr2Yvpg91EAAFsh44spe2TlDXxlAACEgMAAnJuWFcK-J0yqY2qzh4E",
    "CAACAgUAAxkBAAIixmDr2ZrhwXjNKeaSj3Pcn-wj2D-xAALjAgACEJRgVwlEAaqcX_qqHgQ",
    "CAACAgUAAxkBAAIixWDr2ZFWitNjNGRFdQEKdANGkZcJAALaAgACUSJhV40-51_ZbzozHgQ",
    "CAACAgUAAxkBAAKVTWE3jAT6Hj825pBb7dgHZLEaWm4ZAAJKAwAC0dXBVe81BwWerfGJHgQ",
    "CAACAgUAAxkBAAKVTmE3jAz4_9F2ojbWYWH3JoXevsrGAALLBAAC1Jm4Vd-R5GRhcrSPHgQ",
    "CAACAgUAAxkBAAKVT2E3jBM77VU2NbIHUbayxPF21AIXAAJFAwAC__m5VZYZ4gaWxFBsHgQ"
)
HELP_STRINGS =  f"""
*Main Commands :* [🤖]()
 /start: Starts me! You've probably already used this.
 /mstart: Click this, You can find the music payer commands
 /vstart: Click this, You can find the video player commands
 /help: Click this, I'll let you know about myself!
 /donate: You can support my creater using this command.
 /settings: 
   ◔ in PM: will send you your settings for all supported modules.
   ◔ in a Group: will redirect you to pm, with all that chat's settings.
""".format(
    dispatcher.bot.first_name,
    "" if not ALLOW_EXCL else "\nAll commands can either be used with / or !.\n",
)


BASICHELP_STRINGS = """
*Base Commands*
Base commands are the basic tools of Hermione which help you to manage your group easily and effectively
Click buttons to get help  [ ](https://telegra.ph/file/7cea3ae0c4b8637870dd0.jpg)
"""

FUNTOOLS_STRINGS = """
*Fun tools and Extras*
\nExtra tools which are available in bot and tools made for fun are here
Click the buttons for help
"""

ADVTOOLS_STRINGS = """
*Advanced Commands*
\nAdvanced commands will help you to secure your groups from attackers and do many stuff in group from a single bot
Click buttons for help
"""

DONATE_STRING = """Hey, glad to hear you want to donate!
 You can support the project Of [𝕄𝕒𝕥𝕙𝕖𝕖𝕤𝕙𝕒](t.me/rodolphus_lestrang) \
 Supporting isnt always financial! [Team Hermione](https://t.me/HermioneSupport_Official) \
 Those who cannot provide monetary support are welcome to help us develop the bot at ."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
BASICCMDS = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}
FUNTOOLS = {}
ADVTOOLS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("Hermione.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module
    
    if hasattr(imported_module, "__basic_cmds__") and imported_module.__basic_cmds__:
        BASICCMDS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__funtools__") and imported_module.__funtools__:
        FUNTOOLS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__advtools__") and imported_module.__advtools__:
        ADVTOOLS[imported_module.__mod_name__.lower()] = imported_module
   
    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )
    
def send_basiccmds(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, BASICCMDS, "basiccmds"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@run_async
def test(update: Update, context: CallbackContext):
    # pprint(eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


@run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK", callback_data="help_back")]]
                    ),
                )
            elif args[0].lower() == "basiccmds":
                send_basiccmd(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("gbasiccmds_"):
                mod = args[0].lower().split("_", 1)[1]
                if not BASICCMDS.get(mod, False):
                    return
                send_basiccmd(
                    update.effective_chat.id,
                    BASICCMDS[mod].__basic_cmds__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK", callback_data="basiccmds_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            update.effective_message.reply_sticker(
                random.choice(STICKERS),
                timeout=60,
            )
            update.effective_message.reply_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
            )
    else:
        update.effective_message.reply_sticker(
                random.choice(STICKERS),
                timeout=60,
            )
        update.effective_message.reply_text(
            "I'm awake already!\n<b>Haven't slept since:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "Here is the available help for the *{}* module:\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answeSr_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass

@run_async
def basiccmds_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"basic_module\((.+?)\)", query.data)
    prev_match = re.match(r"basic_prev\((.+?)\)", query.data)
    next_match = re.match(r"basic_next\((.+?)\)", query.data)
    back_match = re.match(r"basic_back", query.data)
    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "*⚊❮❮❮❮ ｢  Help  for  {}  module 」❯❯❯❯⚊*\n".format(
                    BASICCMDS[module].__mod_name__
                )
                + BASICCMDS[module].__basic_cmds__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="🔙Back", callback_data="basic_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=BASICHELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, BASICCMDS, "basic")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=BASICHELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, BASICCMDS, "basic")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=BASICHELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, BASICCMDS, "basic")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete(      
    except BadRequest:
        pass
    
@run_async
def funtools_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"fun_module\((.+?)\)", query.data)
    prev_match = re.match(r"fun_prev\((.+?)\)", query.data)
    next_match = re.match(r"fun_next\((.+?)\)", query.data)
    back_match = re.match(r"fun_back", query.data)
    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "*⚊❮❮❮❮ ｢  Help  for  {}  module 」❯❯❯❯⚊*\n".format(
                    FUNTOOLS[module].__mod_name__
                )
                + FUNTOOLS[module].__funtools__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="🔙Back", callback_data="fun_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=FUNTOOLS_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, FUNTOOLS, "fun")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=FUNTOOLS_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, FUNTOOLS, "fun")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=FUNTOOLS_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, FUNTOOLS, "fun")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete(      
    except BadRequest:
        pass
    
@run_async
def advtools_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"adv_module\((.+?)\)", query.data)
    prev_match = re.match(r"adv_prev\((.+?)\)", query.data)
    next_match = re.match(r"adv_next\((.+?)\)", query.data)
    back_match = re.match(r"adv_back", query.data)
    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "*⚊❮❮❮❮ ｢  Help  for  {}  module 」❯❯❯❯⚊*\n".format(
                    ADVTOOLS[module].__mod_name__
                )
                +ADVTOOLS[module].__advtools__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Back", callback_data="adv_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=ADVTOOLS_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, ADVTOOLS, "adv")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=ADVTOOLS_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1,ADVTOOLS, "adv")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=ADVTOOLS_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, ADVTOOLS, "adv")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete(      
    except BadRequest:
        pass
@run_async
def hermione_about_callback(update, context):
    query = update.callback_query
    if query.data == "hermione_":
        query.message.edit_text(
            text=""" *ʜᴇʀᴍɪᴏɴᴇ* - A bot to manage your groups with additional features!
            \nHere's the basic help regarding use of Hermione.
            
            \nAlmost all modules usage defined [ ](https://telegra.ph/file/2b3f3211174d22694466e.mp4)in the help menu, checkout by sending `/help`
            \nReport error/bugs click the Button""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    
                    [InlineKeyboardButton(text="⁉ ʙᴀꜱɪᴄ ʜᴇʟᴘ", callback_data="hermione_basichelp")],
                    [
                        InlineKeyboardButton(
                            text="🎧ᴍᴜꜱɪᴄ ʜᴇʟᴘᴇʀ", url="t.me/Hermione_Music"
                        ),
                        InlineKeyboardButton(
                            text="🎞ᴠɪᴅᴇᴏ ʜᴇʟᴘᴇʀ ", url="t.me/HermioneVHelper"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="✅ ᴜᴘᴅᴀᴛᴇꜱ", url="t.me/Hermione_Updates"
                        ),
                        InlineKeyboardButton(
                            text="👨‍💻 ᴅᴇᴠᴏʟᴏᴘᴇʀ ", url="t.me/rodolphus_lestrang"
                        ),
                    ],
                    [InlineKeyboardButton(text="🏡 ʜᴏᴍᴇ", callback_data="hermione_back")],
                ]
            ),
        )
    elif query.data == "hermione_back":
        query.message.edit_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )

    elif query.data == "hermione_basichelp":
        query.message.edit_text(
            text=f"*Here's basic Help regarding* *How to use Me?*"
            f"\n\n• Firstly Add {dispatcher.bot.first_name} to your group by pressing [here](http://t.me/{dispatcher.bot.username}?startgroup=true)\n"
            f"\n• After adding promote me manually with full rights for faster experience.\n"
            f"\n• Than send `/admincache@HermioneSLBot` in that chat to refresh admin list in My database.\n"
            f"\n\n*All done now use below given button's to know about use!*\n"
            f"",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="ᴀᴅᴍɪɴ 👮‍♀️", callback_data="hermione_admin"),
                    InlineKeyboardButton(text="ɴᴏᴛᴇꜱ 📖", callback_data="hermione_notes"),
                    InlineKeyboardButton(text="ᴀɴᴛɪꜱᴘᴀᴍ 📖", callback_data="hermione_spam"),
                 ],
                 [
                    InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ ⁉", callback_data="hermione_support"),
                    InlineKeyboardButton(text="ᴄʀᴇᴅɪᴛꜱ ❤", callback_data="hermione_credit"),
                 ],
                 [
                    InlineKeyboardButton(text="ᴅᴇᴠꜱ 👨‍💻", callback_data="hermione_devs"),
                    InlineKeyboardButton(text="ꜱᴏᴜʀᴄᴇ ᴄᴏʀᴅ 📜", callback_data="source_"),
                 ],
                 [
                    InlineKeyboardButton(text="🏡ʜᴏᴍᴇ", callback_data="hermione_back"),
                 
                 ]
                ]
            ),
        )
    elif query.data == "hermione_admin":
        query.message.edit_text(
            text=f"*Let's make your group bit effective now*"
            f"\nCongragulations, Hermione now ready to manage your group."
            f"\n\n*Admin Tools*"
            f"\nBasic Admin tools help you to protect and powerup your group."
            f"\nYou can ban members, Kick members, Promote someone as admin through commands of bot."
            f"\n\n*Welcome*"
            f"\nLets set a welcome message to welcome new users coming to your group."
            f"send `/setwelcome [message]` to set a welcome message!",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="🔙Back", callback_data="hermione_basichelp")]]
            ),
        )

    elif query.data == "hermione_notes":
        query.message.edit_text(
            text=f"<b> Setting up notes</b>"
            f"\nYou can save message/media/audio or anything as notes"
            f"\nto get a note simply use # at the beginning of a word"
            f"\n\nYou can also set buttons for notes and filters (refer help menu)",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="🔙Back", callback_data="hermione_basichelp")]]
            ),
        )
    elif query.data == "hermione_support":
        query.message.edit_text(
            text="* Hermione support chats*"
            "\nJoin Support Group/Channel",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="ʟᴏɢꜱ 📜", url="t.me/HermioneLogs"),
                    InlineKeyboardButton(text="ꜱᴅʙᴏᴛꜱ 🤖", url="https://t.me/SDBOTz"),
                 ],
                 [
                    InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ ❓", url="https://t.me/HermioneSupport_Official"),
                    InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇꜱ ✅", url="https://t.me/Hermione_updates"),
                 ],
                 [
                    InlineKeyboardButton(text="◀ Back", callback_data="hermione_basichelp"),
                 
                 ]
                ]
            ),
        )
    elif query.data == "hermione_credit":
        query.message.edit_text(
            text=f"<b> CREDIT FOR OTHER BOT I USING THERE CODES </b>\n"
            f"\nHere Some Bots Helping in Making The Innexia Bot",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Hermione", url="t.me/hermioneslbot"),
                 
                 ],
                 [
                    InlineKeyboardButton(text="ᴅᴀɪꜱʏ", url="t.me/DaisyXbot"),
                    InlineKeyboardButton(text="ʜᴇxʏ", url="t.me/HiTechRockets"),
                 ],
                 [
                    InlineKeyboardButton(text="ᴀɴᴋɪᴠᴇᴄᴛᴏʀ", url="https://t.me/ankivectorUpdates"),
                    InlineKeyboardButton(text="ɴᴀᴛᴢᴜᴋɪ", url="https://t.me/Natsuki_Updates"),
                 ],
                 [
                    InlineKeyboardButton(text="◀ ʙᴀᴄᴋ", callback_data="hermione_basichelp"),
                 
                 ]
                ]
            ),
        )
    elif query.data == "hermione_devs":
        query.message.edit_text(
            text=f"""
           *Contributors of Hermione 5.0*

           *✪ Owners 👨‍💻*
           • [Matheesha Illeperuma](t.me/rodolphus_lestrang) » [GitHub](https://github.com/MatheeshaOfficial)  (Owner)
           
           *✪ Devs 🔥*
           • Damantha Jasinghe » [GitHub](https://github.com/Damantha126) (Dev)
           • Supunma » [GitHub](http://github.com/szsupunma)  (Dev) 
           
           *✪ Special Credits ❤️*
           • Inuka Asith (specially ❤)
           • Prabasha
           • ImJanindu
           • Devil
           • Miss-Valentina 
           • Mr-Dark-Prince
           • Anime Kaizoku
           • thehamkercat
           • TroJanzHEX
           • TeamDaisyx
           
           *@HermioneSLBot*
           """,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
              [
                  [
                      InlineKeyboardButton(text="◀ ʙᴀᴄᴋ", callback_data="hermione_basichelp"),
                  ]
                ]
            ),
        ) 
        

@pbot.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()
    await pbot.answer_callback_query(CallbackQuery.id, text, show_alert=True)
    
    
@run_async
def Source_about_callback(update, context):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_text(
            text=""" Hi..🙋 I'm *Hermione*
                 \nHere is the [Source Code](https://github.com/PercyOfficial/Hermione) .""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Go Back", callback_data="source_back")
                 ]
                ]
            ),
        )
    elif query.data == "source_back":
        query.message.edit_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )
@run_async
def hermione_menu_callback(update, context):
    query = update.callback_query
    if query.data == "helpmenu_":
        query.message.edit_text(
            text=""" *Welcome Hermione's Help Menu*
            \n `ꜱᴇʟᴇᴄᴛ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ ꜰᴏʀ ꜰᴜʟʟ  ʜᴇʟᴘ ᴏʀ ꜱᴇʟᴇᴄᴛ ᴄᴀᴛᴀɢᴏʀʏ ꜰᴏʀ ᴍᴏʀ ʜᴇʟᴘ ᴅᴏᴄᴜᴍᴀᴛɪᴏɴ ᴏɴ ꜱᴇʟᴇᴄᴛᴇᴅ ꜰɪᴇʟᴅꜱ` """,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="➕All Commands➕", callback_data="help_back"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="⛑ Basic Commands ", callback_data="basic_back"
                        ),
                        InlineKeyboardButton(
                            text="🔍 Inline Commands", callback_data="helpmenu_inline"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="😹 Fun Tools & Extras", callback_data="fun_back"
                        ),
                        InlineKeyboardButton(
                            text="♨ Advance Commands", callback_data="adv_back"
                        ),
                    ],
                        [InlineKeyboardButton(text="🏡 Home ", callback_data="helpmenu_back")],
                ]
            ),
        )
    elif query.data == "helpmenu_back":
        query.message.edit_text(
            PM_START_TEXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
        )
        
    elif query.data == "helpmenu_inline":
        query.message.edit_text(
            text="""*INLINE BOT SERVICE OF @HermioneSLBot *
            \n `I'm more efficient when added as group admin. By the way these commands can be used by anyone in a group via inline.`
            \n\n *Syntax*
            \n❍@HermioneSLBot [command] [query]
            \n\n❍ *Commands Available*
            \n❍alive - Check Bot's Stats.
            \n❍yt [query] - Youtube Search.
            \n❍tr [LANGUAGE_CODE] [QUERY]** - Translate Text.
            \n❍modapk [name] - Give you direct link of mod apk.
            \n❍ud [QUERY] - Urban Dictionary Query
            \n❍google [QUERY] - Google Search.
            \n❍webss [URL] - Take Screenshot Of A Website.
            \n❍bitly [URL] - Shorten A Link.
            \n❍wall [Query] - Find Wallpapers.
            \n❍pic [Query] - Find pictures.
            \n❍saavn [SONG_NAME] - Get Songs From Saavn.
            \n❍deezer [SONG_NAME] - Get Songs From Deezer.
            \n❍torrent [QUERY] - Torrent Search.
            \n❍reddit [QUERY] - Get memes from reddit.
            \n❍imdb [QUERY] - Search movies on imdb.
            \n❍spaminfo [ID] - Get spam info of the user.
            \n❍lyrics [QUERY] - Get lyrics of the song.
            \n❍paste [TEXT] - Paste text on pastebin.
            \n❍define [WORD] - Get definition from Dictionary.
            \n❍synonyms [WORD] - Get synonyms from Dictionary.
            \n❍antonyms [WORD] - Get antonyms from Dictionary.
            \n❍country [QUERY] - Get Information about given country.
            \n❍cs - Gathers Cricket info (Globally).
            \n❍covid [COUNTRY] - Get covid updates of given country.
            \n❍fakegen - Gathers fake information.
            \n❍weather [QUERY] - Get weather information.
            \n❍datetime [QUERY] - Get Date & time information of given country/region.
            \n❍app [QUERY] - Search for apps in playstore.
            \n❍gh [QUERY] - Search github.
            \n❍so [QUERY] - Search stack overflow.
            \n❍wiki [QUERY] - Search wikipedia.
            \n❍ping - Check ping rate.
            \n❍pokedex [TEXT]: Pokemon Search """,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="helpmenu_")]]
            ),
        )
@run_async
def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Help",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "Contact me in PM to get the list of possible commands.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Help",
                            url="t.me/{}?start=help".format(context.bot.username),
                        )
                    ]
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="🔙Back", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)

@run_async
def get_basiccmds(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in BASICCMDS):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Help",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "Contact me in PM to get the list of possible commands.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="⚙️Help",
                            url="t.me/{}?start=help".format(context.bot.username),
                        )
                    ]
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                BASICCMDS[module].__mod_name__
            )
            + BASICCMDS[module].__basic_cmds__
        )
        send_basiccmds(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="🔙Back", callback_data="basiccmds_back")]]
            ),
        )

    else:
        send_basiccmds(chat.id, HELP_STRINGS)
                       

def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


@run_async
def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🔙Back",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


@run_async
def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Settings",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)


@run_async
def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 254318997 and DONATION_LINK:
            update.effective_message.reply_text(
                "You can also donate to the person currently running me "
                "[here]({})".format(DONATION_LINK),
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "I've PM'ed you about donating to my creator!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "Contact me in PM first to get donation information."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendMessage(f"@{SUPPORT_CHAT}", "Oh🥳 \n Hermione new version released ♨ \nplease pm for more 🤟 ")
        except Unauthorized:
            LOGGER.warning(
                "Bot isnt able to send message to support_chat, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    test_handler = CommandHandler("test", test)
    start_handler = CommandHandler("start", start)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*")

    funtools_callback_handler = CallbackQueryHandler(funtools_button, pattern=r"fun_.*")
    advtools_callback_handler = CallbackQueryHandler(advtools_button, pattern=r"adv_.*")
    basiccmds_callback_handler = CallbackQueryHandler(basiccmds_button, pattern=r"basic_.*")
    basiccmds_handler = CommandHandler("basiccmds",get_basiccmds)
    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    menu_callback_handler = CallbackQueryHandler(hermione_menu_callback, pattern =r"helpmenu_")
    about_callback_handler = CallbackQueryHandler(hermione_about_callback, pattern=r"hermione_")
    source_callback_handler = CallbackQueryHandler(Source_about_callback, pattern=r"source_")

    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    # dispatcher.add_handler(test_handler)Call
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(source_callback_handler)
    dispatcher.add_handler(advtools_callback_handler)
    dispatcher.add_handler(funtools_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)
    dispatcher.add_handler(basiccmds_callback_handler)
    dispatcher.add_handler(basiccmds_handler)
    dispatcher.add_handler(menu_callback_handler)
                       
    dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4, clean=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    pbot.start()
    telethn.start(bot_token=TOKEN)
    main()
