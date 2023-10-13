import telebot
from telebot import custom_filters
import time

TOKEN = "6657389725:AAGEp83C3rDXTZZ0d7dIczOFB-3rvwt0t-0"
MSG = "Join Binverse for more giveaways"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def not_admin(message):
    bot.send_message(message.chat.id, "Your Bot is Running Fine")
    while(True):
        bot.send_message(-1001617751848, MSG, time.sleep(60))
        bot.send_message(-1001780812092, MSG, time.sleep(60))

# Do not forget to register
bot.add_custom_filter(custom_filters.ChatFilter())
bot.polling(none_stop=True)
