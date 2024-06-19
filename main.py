from dotenv import load_dotenv
import os
import telebot

load_dotenv()

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=["start"])
def handle_start(message):
  bot.reply_to(message, """\
Halo, saya joyboy.
ada perlu apa lu chat gua??\
kalo bingung coba lu ketik /help di situ banyak informasi penting\
""")
  
@bot.message_handler(commands=["help"])
def handle_help(message):
  bot.reply_to(message, """\
TAPI BOONG WKWKWKWKW
""")
  
bot.polling(none_stop=True, interval=0)