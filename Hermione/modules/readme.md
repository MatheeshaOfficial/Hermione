# Hermione Example plugin format
## Advanced: Pyrogram
```python3
from Hermione.function.pluginhelpers import admins_only
from Hermione.services.pyrogram import pbot

@pbot.on_message(filters.command("hi") & ~filters.edited & ~filters.bot)
@admins_only
async def hmm(client, message):
    j = "Hello there"
    await message.reply(j)
    
__mod_name__ = "Hi"
__help__ = """
<b>Hi</b>
- /hi: Say Hello There Im Hermione
"""
```

## Advanced: Telethon
```python3

from Hermione import telethn as tbot
from Hermione.services.events import register

@register(pattern="^/hi$")
async def hmm(event):
    j = "Hello there"
    await event.reply(j)
    
__mod_name__ = "Hi"
__help__ = """
<b>Hi</b>
- /hi: Say Hello There Im Hermione 
"""
```
