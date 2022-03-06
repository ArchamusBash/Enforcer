#!/usr/bin/env python3

import os
from pyrogram import Client, filters

nomes = []

bot = Client("Enforcer",
            api_id = os.environ.get("APID")
            api_hash = os.environ.get("HASH"),
            bot_token = os.environ.get("TOKEN")
)

admin = os.environ.get("ADMIN")

@bot.on_message(filters.command("start") & filters.private)
def start(client, message):
    message.reply("Adicione-me em um grupo")

@bot.on_message(filters.command("start") & filters.group)
def starte(client, message):
    message.reply("Modo de uso: de adm para o bot e deixe que ele faça o resto.")

@bot.on_message(filters.group & filters.new_chat_members)
def ban_rus(client, message):
    ide = message.new_chat_members
    usr = [u.mention for u in message.new_chat_members]
    txt_ban = "{} enviado pro Gulag.".format(ide).replace("[","").replace("]","").replace("'","")
    ide = str(ide).split(",")
    ide = list(ide)
    lol = str(ide[0]).replace("[pyrogram.types.User(id=","")
    rm  = "href=tg://user?id=" + lol
    print(lol)
    rus = ["й","ц","у","к","е","н","г","ш","щ","з","х","ф","ы","в","а","п","р","о","л","д","ж","э","я","ч","с","м","и","т","ь","б","ю"]
    name = [f.mention for f in message.new_chat_members]    
    name = str(name)
    name = name.replace("'","").replace("[","").replace("]","").replace("<a href=tg://user?id=5111841981>","").replace("</a>","")
    name = list(name)
    print(name)
    for l in rus:
        if l in name:
            print(l)
            bot.ban_chat_member(message.chat.id, lol)
            bot.send_message(message.chat.id, "Usuario {} foi enviado pro Gulag.".format(lol))
            break
        
    with open("logs.txt", "a") as f:
        out = str(ide)
        f.write(str(out))
        print(out)
        f.write("\n")
        f.write("-------------------------------")
        f.write("\n")
    f.close()


@bot.on_message(filters.command("logs"))
def logs(client, message):
    user = message.from_user.id
    if int(admin) == int(user):
        try:
            doc = open("logs.txt", "r")
        except:
            bot.send_message(admin, "O arquivo de logs não existe...")
        else:
            bot.send_message(admin, "Aqui estão os logs:")
            bot.send_document(admin, "logs.txt")



if __name__ == "__main__":
    bot.run()
