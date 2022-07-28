import requests
import os
from pyrogram import filters
from Hermione.services.pyrogram import pbot as hermione
from Hermione.function.pluginhelpers import (
  edit_or_reply,
  get_text,
  convert_to_image,
)
                                            

headers = {
    'authority': 'api8.ocr.space',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'apikey': '5a64d478-9c89-43d8-88e3-c65de9999580',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.39',
    'origin': 'https://ocr.space',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://ocr.space/',
    'accept-language': 'en-US,en;q=0.9',
}

async def read_ocr_(img_path):
    path_ = {"file": (img_path, open(img_path, "rb"))}
    response = requests.post('https://api8.ocr.space/parse/image', headers=headers, files=path_)
    return response.json()["ParsedResults"][0]['ParsedText']


@hermione.on_message(filters.command(["imgtotext", "itt"]))
async def idontknowhowtospell(client, message):
    msg_ = await edit_or_reply(message, "<code>Reading Please..</code>", parse_mode="html")
    if not message.reply_to_message:
        return await msg_.edit("<code>Please Reply To A Image.</code>", parse_mode="html")
    cool = await convert_to_image(message, client)
    if not cool:
        await msg_.edit("<code>Reply to a valid media first.</code>", parse_mode="html")
        return
    if not os.path.exists(cool):
        await msg_.edit("<code>Invalid Media!</code>", parse_mode="html")
        return
    text_ = await read_ocr_(cool)
    if not text_:
        return await msg_.edit("`No Text Found in Image.`")
    await msg_.edit(f"<u><b>HERMIONE IMAGE TO TEXT RESULT</u></b> \n\n<code>{text_}</code>", parse_mode="html")
