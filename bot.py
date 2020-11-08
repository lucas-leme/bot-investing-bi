import logging
import os
import requests
import json

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from investing import get_investiments_last_period_performace, optimize_portfolio, backtesting

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
        text = get_investiments_last_period_performace(window)

        update.message.reply_photo(photo = open('returns.png', 'rb'))
        update.message.reply_text(text)  
        

        os.remove('returns.png')
    except Exception as e:
        update.message.reply_text(e) 

def optimize(update, context):
    risk_threshold = float(update.message.text[9:])
    weights, performace = optimize_portfolio(risk_threshold = risk_threshold)

    update.message.reply_photo(photo = open('clustermap.png', 'rb'))
    update.message.reply_text(weights)
    update.message.reply_text(performace)

    os.remove('clustermap.png')

def backtesting_stats(update, context):
    risk_threshold = float(update.message.text[12:])

    report = backtesting(risk_threshold)

    update.message.reply_photo(photo = open('rents.png', 'rb'))
    update.message.reply_text(report)
    update.message.reply_photo(photo = open('rents_dist.png', 'rb'))

    os.remove('rents.png')
    os.remove('rents_dist.png')
    

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
    dp.add_handler(CommandHandler('backtesting', backtesting_stats))

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