import logging
import os
import requests
import json

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from investing import get_investiments_last_period_performace, optimize_portfolio

TOKEN = os.environ['TELEGRAM_TOKEN']
PORT = int(os.environ.get("PORT", "8443"))
HEROKU_APP_NAME = os.environ.get("bot-investing-bi")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# /help
def send_help(update, context):
    update.message.reply_text("Comandos: /return período; /optimize")

# /start
def send_welcome(update, context):
    update.message.reply_text("Salve, Salve Grupo Turing!")

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def last_returns(update, context):
    try:
        window = int(update.message.text[8:])
        text, image_path = get_investiments_last_period_performace(window)
        update.message.reply_text(text)  
        update.message.reply_photo(image_path)

        os.remove(image_path)
    except:
        update.message.reply_text('Erro no comando: /returns PERÍODOS') 

def optimize(update, context):
    weights, performace = optimize_portfolio()

    update.message.reply_text(weights)
    update.message.reply_text(performace)

def main():
    logger.info("Bot started")

    updater = Updater(
        TOKEN, use_context=True)

    dp = updater.dispatcher

    logger.info("working till here")

    dp.add_handler(CommandHandler("start", send_welcome))
    dp.add_handler(CommandHandler("help", send_help))

    dp.add_handler(CommandHandler('returns', last_returns))
    dp.add_handler(CommandHandler('optimize', optimize))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://bot-investing-bi.herokuapp.com/" + TOKEN)

    logger.info("Listening for messages...")

    updater.start_polling()
    updater.idle()

    

if __name__ == '__main__':
    main()