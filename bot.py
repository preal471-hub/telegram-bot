import telebot
from telebot.types import ChatJoinRequest
import json
import time

TOKEN = "8266089449:AAEJ35ONfsuI2glgRQW_WVwfmGguDp0MEfU"
CHANNEL_ID = -1002280087377   # we will add later

bot = telebot.TeleBot(TOKEN)

# Save users
def save_user(user_id):
    try:
        with open("users.json","r") as f:
            users = json.load(f)
    except:
        users = []

    if user_id not in users:
        users.append(user_id)
        with open("users.json","w") as f:
            json.dump(users,f)

# START command
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    bot.send_message(message.chat.id,
    "👋 Welcome Trader!\nClick below to join OUR Channel 💎")

# Auto approve join request
@bot.chat_join_request_handler()
def approve_join_request(join_request: ChatJoinRequest):
    user_id = join_request.from_user.id

    # Save user automatically when they request to join channel
    save_user(user_id)

    # Approve join request
    bot.approve_chat_join_request(
        join_request.chat.id,
        user_id
    )

    # Send welcome DM after approval
    try:
        bot.send_message(user_id,
        "🎉 You are approved in OUR Channel!\n\nStay ready for premium trades 🚀")
    except:
        pass

# Broadcast command
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    msg = message.text.replace("/broadcast ","")

    with open("users.json","r") as f:
        users = json.load(f)

    for user in users:
        try:
            bot.send_message(user, msg)
            time.sleep(0.05)
        except:
            pass

    bot.reply_to(message,"Broadcast sent!")

bot.infinity_polling()