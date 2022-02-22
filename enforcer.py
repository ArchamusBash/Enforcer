#!/usr/bin/env python3

import os
import time

from pyrogram import Client, emoji, filters
from pyrogram.types import Message
from dotenv import load_dotenv

load_dotenv()

app = Client(
        "Enforcer",
        api_id    = int(os.getenv("APID")),
        api_hash  = os.getenv("HASH"),
        bot_token = os.getenv("TOKEN")
        )

flood = {}
time_muted = 720
admins = {}
target_group = -1001771832249

def GetAdmins(app: Client, message: Message) -> list:
    return [
            admin.user.id
            for admin in app.get_chat_members(message.chat.id, filter="administrators")
            ]

@app.on_message(filters.chat(target_group) & filters.new_chat_members)
def welcome(client, message):
    new_member = [u.mention for u in message.new_chat_members]
    text = "Seja bem vindo {}!\nTe enviei as regras no privado.".format(new_member, message.from_user.id).replace("[","").replace("]","").replace("'","")
    message.reply(text, disable_web_page_preview=True)

@app.on_message(filters.group)
def floodw(app, message: Message):
    chat_id = -1001771832249
    user_id = message.from_user.id
    print(chat_id)
    try:
        if user_id not in admins[chat_id]:
            try:
                flood[chat_id][user_id] += 1
            except KeyError:
                flood[chat_id][user_id] -= 1
        else:
            if flood[chat_id][user_id] > 4:
                app.restrict_chat_member(chat_id, user_id, int(time.time()) + time_muted)
                message.reply_text(f"Por favor evite spam!\nUsuario {user_id} mutado.")
            else:
                time.sleep(1.5)
                try:
                    flood[chat_id][user_id] -= 1
                    if flood[chat_id][user_id] == 0:
                        del flood[chat_id][user_id]
                except KeyError as err:
                    print(err)
    except KeyError:
        admins[chat_id] = GetAdmins(app, message)

@app.on_message(filters.command("start") & filters.group)
def start(client, message):
    usr = message.from_user.first_name
    app.send_message(message.chat.id, f"Eai, {usr}!")

if __name__ == "__main__":
    app.run()


