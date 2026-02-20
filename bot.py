import telebot
from telebot.types import ChatJoinRequest
import json
import time
import os
from flask import Flask
import threading

# 👇 Render will read token from Environment Variables
TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = -1002280087377

bot = telebot.TeleBot(TOKEN)

# Dummy Flask server (for Render Free Web Service)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

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

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    bot.send_message(message.chat.id,
    "👋 Welcome Trader!\nClick below to join OUR Channel 💎")

@bot.chat_join_request_handler()
def approve_join_request(join_request: ChatJoinRequest):
    user_id = join_request.from_user.id
    save_user(user_id)

    bot.approve_chat_join_request(
        join_request.chat.id,
        user_id
    )

    try:
        bot.send_message(user_id,
        "🎉 You are approved in OUR Channel!\n\nStay ready for premium trades 🚀")
    except:
        pass

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

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.infinity_polling()

