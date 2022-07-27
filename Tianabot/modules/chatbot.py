import requests
from googletrans import Translator
from pyrogram import filters
from pyrogram.types import Message

from Tianabot import BOT_ID, eor
from Tianabot import pbot as app
from Tianabot.mongo import db
from Tianabot.utils.filter_groups import chatbot_group

__mod_name__ = "Cʜᴀᴛ-Bᴏᴛ"
__help__ = """
/chatbot on/off: To Enable Or Disable ChatBot In Your Chat.

There's one module of this available for userbot also
check userbot module help."""

chatbotdb = db.chatbot

def check_chatbot():
    return chatbotdb.find_one({"chatbot": "chatbot"}) or {
        "bot": [],
        "userbot": [],
    }

def add_chatbot(chat_id: int, is_userbot: bool = False):
    list_id = check_chatbot()
    if is_userbot:
        list_id["userbot"].append(chat_id)
    else:
        list_id["bot"].append(chat_id)
    chatbotdb.update_one({"chatbot": "chatbot"}, {"$set": list_id}, upsert=True)

def rm_chatbot(chat_id: int, is_userbot: bool = False):
    list_id = check_chatbot()
    if is_userbot:
        list_id["userbot"].remove(chat_id)
    else:
        list_id["bot"].remove(chat_id)
    chatbotdb.update_one({"chatbot": "chatbot"}, {"$set": list_id}, upsert=True)


async def chat_bot_toggle(message: Message, is_userbot: bool):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    db = check_chatbot()
    db = db["userbot"] if is_userbot else db["bot"]
    if status == "on":
        if chat_id not in db:
            add_chatbot(chat_id, is_userbot=is_userbot)
            text = "Merissa Chatbot Enabled!"
            return await eor(message, text=text)
        await eor(message, text="Merissa ChatBot Is Already Enabled.")
    elif status == "off":
        if chat_id in db:
            rm_chatbot(chat_id, is_userbot=is_userbot)
            return await eor(message, text="Merissa Chatbot Disabled!")
        await eor(message, text="Merissa ChatBot Is Already Disabled.")
    else:
        await eor(message, text="**Usage:**\n/chatbot On/Off")


# Enabled | Disable Chatbot


@app.on_message(filters.command("chatbot") & ~filters.edited)
async def chatbot_status(_, message: Message):
    if len(message.command) != 2:
        return await eor(message, text="**Usage:**\n/chatbot on/off")
    await chat_bot_toggle(message, is_userbot=False)


tr = Translator()


@app.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded
    & ~filters.edited,
    group=chatbot_group,
)
async def chatbot_talk(_, message: Message):
    chat = message.chat.id
    db = check_chatbot()
    if message.chat.id not in db["bot"]:
        return
    if not message.reply_to_message:
        return
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id != BOT_ID:
        return
    if message.text[0] == "/":
        return
    if chat:
        await app.send_chat_action(message.chat.id, "typing")
        lang = tr.translate(message.text).src
        trtoen = (
            message.text if lang == "en" else tr.translate(message.text, dest="en").text
        ).replace(" ", "%20")
        text = trtoen.replace(" ", "%20") if len(message.text) < 2 else trtoen
        merissaurl = requests.get(
            f"https://merissachatbot.tk/api/apikey={token}/{botname}/{owner}/message={text}"
        )
        textmsg = merissaurl.json()["message"]
        msg = tr.translate(textmsg, src="en", dest=lang)
        await message.reply_text(msg.text)
