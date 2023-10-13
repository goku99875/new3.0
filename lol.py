import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Define your API token (bot token) obtained from the BotFather on Telegram.
API_TOKEN = '6696946141:AAHaG-AlGEpA-y2l1pQL8UJSujDZjtujlI4'

# Define the chat_id of the source channel you want to forward posts from.
SOURCE_CHANNEL_ID = -1001989302520  # Replace with the actual source channel ID.

# Define the chat_id of the destination channel where you want to forward the posts.
DESTINATION_CHANNEL_ID = -1001838544499  # Replace with the actual destination channel ID.

# Initialize the Telegram Bot API updater.
updater = Updater(token=API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Enable logging for debugging (optional).
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define a command to start the bot.
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Bot started!')

# Define a function to forward messages from the source channel to the destination channel.
def forward_message(update: Update, context: CallbackContext):
    message = update.message
    try:
        # Forward the message from the source channel to the destination channel.
        message.forward(DESTINATION_CHANNEL_ID)
    except Exception as e:
        # Handle errors, e.g., if the bot doesn't have permission to forward messages.
        update.message.reply_text(f'Error forwarding message: {str(e)}')

# Handle incoming messages from the source channel.
forward_handler = MessageHandler(Filters.chat(chat_id=SOURCE_CHANNEL_ID), forward_message)
dispatcher.add_handler(forward_handler)

# Start the bot.
updater.start_polling()

# Keep the bot running until you manually stop it (Ctrl+C).
updater.idle()
