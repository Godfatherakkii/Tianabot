import dateparser 
import os
import asyncio
import pytz

from pyrogram import filters
from pymongo import MongoClient
from datetime import datetime, timedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions

from Tianabot import pbot
from Tianabot import BOT_ID, MONGO_DB_URI


client = MongoClient(MONGO_DB_URI)
dbd = client["missjuliarobot"]
approved_users = dbd.approve
db = dbd

tagdb = db.tagdb1
alarms = db.alarm
shedule = db.shedule
nightmod = db.nightmode4

def get_info(id):
    return nightmod.find_one({"id": id})


@pbot.on_message(filters.command(["tagalert"]) & filters.private)
async def locks_dfunc(_, message):
   lol = await message.reply("Processing..")
   if len(message.command) != 2:
      return await lol.edit("Expected on or off 👀")
   parameter = message.text.strip().split(None, 1)[1].lower()
  
   if parameter == "on" or parameter=="ON":
     if not message.from_user:
       return
     if not message.from_user.username:
       return await lol.edit("Only users with usernames are eligible for tag alert service")
     uname=str(message.from_user.username)
     uname = uname.lower()
     isittrue = tagdb.find_one({f"teg": uname})
     if not isittrue:
          tagdb.insert_one({f"teg": uname})
          return await lol.edit(f"Tag alerts enabled.\nWhen someone tags you as @{uname} you will be notified")
     else:
          return await lol.edit("Tag alerts already enabled for you")
   if parameter == "off" or parameter=="OFF":
     if not message.from_user:
       return
     if not message.from_user.username:
       return await lol.edit("Only users with usernames are eligible for tag alert service")
     uname = message.from_user.username
     uname = uname.lower()
     isittrue = tagdb.find_one({f"teg": uname})
     if isittrue:
          tagdb.delete_one({f"teg": uname})
          return await lol.edit("Tag alerts removed")
     else:
          return await lol.edit("Tag alerts already disabled for you") 
   else:
     await lol.edit("Expected on or off 👀")
     





     
@pbot.on_message(filters.incoming & ~filters.edited)
async def mentioned_alert(client, message):
    try:
        if not message:
            message.continue_propagation()
            return
        if not message.from_user:
            message.continue_propagation()
            return 
        input_str = message.text
        input_str = input_str.lower()
        if "@" in input_str:
            
            input_str = input_str.replace("@", "  |")
            inuka = input_str.split("|")[1]
            text = inuka.split()[0]
        else:
            chats = alarms.find({})
            for c in chats:
              #print(c)
              chat = c["chat"]
              user = c["user"]
              time = c["time"]
              zone = c["zone"]
              reason = c["reason"]
              present = dateparser.parse(f'now', settings={'TIMEZONE': f'{zone}', 'DATE_ORDER': 'YMD'}) 
              ttime = dateparser.parse(f'{time}', settings={'TIMEZONE': f'{zone}'}) 
              #print(ttime)
              #print(present)
              #print (zone)
              #print(present>=ttime)
              if present > ttime:
               try:
                 alarms.delete_one({"chat": chat, "user": user, "time": time, "zone": zone, "reason": reason})
                 await client.send_message(chat, f"**🚨 REMINDER 🚨**\n\n__This is a reminder set by__ {user}\n__Reason__: {reason} \n\n`Reminded at: {ttime}`")
                 
                 message.continue_propagation()
               except:
                 alarms.delete_one({"chat": chat, "user": user, "time": time, "zone": zone, "reason": reason})
                 return message.continue_propagation()
               break
               return message.continue_propagation()
              continue
            chats = shedule.find({})
            for c in chats:
              #print(c)
              chat = c["chat"]
              user = c["user"]
              time = c["time"]
              zone = c["zone"]
              reason = c["reason"]
              present = dateparser.parse(f'now', settings={'TIMEZONE': f'{zone}', 'DATE_ORDER': 'YMD'}) 
              ttime = dateparser.parse(f'{time}', settings={'TIMEZONE': f'{zone}'}) 
              #print(ttime)alarms
              #print(present)
              #print (zone)
              #print(present>=ttime)
              if present > ttime:
               try:
                 shedule.delete_one({"chat": chat, "user": user, "time": time, "zone": zone, "reason": reason})                  
                 await client.send_message(chat, f"{reason}")
                 message.continue_propagation()
               except:
                 shedule.delete_one({"chat": chat, "user": user, "time": time, "zone": zone, "reason": reason})
                 return message.continue_propagation()
               break
               return message.continue_propagation()
              continue              
            chats = nightmod.find({})
            
            for c in chats:
              # print(c)
              id = c["id"]
              valid = c["valid"]
              zone = c["zone"]
              c["ctime"]
              otime = c["otime"]
              present = dateparser.parse(
                   "now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"}
              )
              try:
                 if present > otime and valid:
                     newtime = otime + timedelta(days=1)
                     to_check = get_info(id=id)
                     if not to_check:
                         return message.continue_propagation()
                     if not newtime:
                         return message.continue_propagation()                       
                     #print(newtime)
                     #print(to_check)
                     nightmod.update_one(
                         {
                             "_id": to_check["_id"],
                             "id": to_check["id"],
                             "valid": to_check["valid"],
                             "zone": to_check["zone"],
                             "ctime": to_check["ctime"],
                             "otime": to_check["otime"],
                         },
                         {"$set": {"otime": newtime}},
                     )                  
                     await client.set_chat_permissions(
                          id,
                          ChatPermissions(
                              can_send_messages=True,
                              can_send_media_messages=True,
                              can_send_stickers=True,
                              can_send_animations=True
                           )
                     )

                     await client.send_message(
                          id,
                          "**🌗 Night Mode Ended: `Chat Opening` \n\nEveryOne Should Be Able To Send Messages.**",
                     )
                     message.continue_propagation()
                     break
                     return message.continue_propagation()
              except:
                  print("Chat open error in nightbot")
                  return message.continue_propagation()
              continue       
            chats = nightmod.find({})
            for c in chats:
              # print(c)
              id = c["id"]
              valid = c["valid"]
              zone = c["zone"]
              ctime = c["ctime"]
              c["otime"]
              optime = c["otime"]
              present = dateparser.parse(
                  "now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"}
              )
              try:
                 if present > ctime and valid:
                     newtime = ctime + timedelta(days=1)
                     to_check = get_info(id=id)
                     if not to_check:
                         return message.continue_propagation()
                     if not newtime:
                         return message.continue_propagation()
                     #print(newtime)
                     #print(to_check)
                     nightmod.update_one(
                         {
                             "_id": to_check["_id"],
                             "id": to_check["id"],
                             "valid": to_check["valid"],
                             "zone": to_check["zone"],
                             "ctime": to_check["ctime"],
                             "otime": to_check["otime"],
                         },
                         {"$set": {"ctime": newtime}},
                     )
                     await client.set_chat_permissions(id, ChatPermissions())                  
                     await client.send_message(
                         id,
                         "**🌗Night Mode Starting: `Chat close initiated`\n\nOnly Admins Should Be Able To Send Messages**",
                     )
                     message.continue_propagation()
                     break
                     return message.continue_propagation()
              except:
                  print("Chat close err")
                  return message.continue_propagation()
              continue            
            return message.continue_propagation()
        #print(text)
        if tagdb.find_one({f"teg": text}):
            pass
        else:
            return message.continue_propagation()
        #print("Im inn")
        try:
            chat_name = message.chat.title
            chat_id = message.chat.id
            tagged_msg_link = message.link
        except:
            return message.continue_propagation()
        user_ = message.from_user.mention or f"@{message.from_user.username}"
        
        final_tagged_msg = f"**🔔 You Have Been** [Tagged]({tagged_msg_link}) **in** {chat_name} **By** {user_}"
        button_s = InlineKeyboardMarkup([[InlineKeyboardButton("🔔 View Message 🔔", url=tagged_msg_link)]])
        #print(final_tagged_msg)
        try:
            await client.send_message(chat_id=f"{text}", text=final_tagged_msg,reply_markup=button_s,disable_web_page_preview=True)
            
        except:
            return message.continue_propagation()
        message.continue_propagation()
    except:
        return message.continue_propagation()
