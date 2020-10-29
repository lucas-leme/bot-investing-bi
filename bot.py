import logging
import os
import requests
import json

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from investing import get_investiments_last_period_performace

TOKEN = os.environ['TELEGRAM_TOKEN']
PORT = int(os.environ.get("PORT", "8443"))
HEROKU_APP_NAME = os.environ.get("bot-investing-bi")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# /help
def send_help(update, context):
    update.message.reply_text("Comandos: /quant; /nlp; /cv; /rl; /ds; /gpt2; /qa")

# Descrição das Areas de foco

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
        update.message.reply_text(text)  
    except:
        update.message.reply_text('Erro no comando: /returns PERÍODOS') 


def gpt2_reply(update, context):
    GPT2_API_URL = "https://api-inference.huggingface.co/models/pierreguillou/gpt2-small-portuguese"
    payload_input_text =  json.dumps(update.message.text)

    response = requests.post(GPT2_API_URL, payload_input_text)

    text = str(response.json()[0])[20:-2]

    update.message.reply_text(text)

def turing_qa(update, context):
    API_URL = "https://api-inference.huggingface.co/models/mrm8488/bert-base-portuguese-cased-finetuned-squad-v1-pt"

    payload = json.dumps({
        "context": get_manual_do_membro(),
        "question": update.message.text
    })

    response = requests.post(API_URL, payload)

    update.message.reply_text(response.json()['answer'])

def main():
    logger.info("Bot started")

    updater = Updater(
        TOKEN, use_context=True)

    dp = updater.dispatcher

    logger.info("working till here")

    dp.add_handler(CommandHandler("start", send_welcome))
    dp.add_handler(CommandHandler("help", send_help))

    dp.add_handler(CommandHandler("gpt2", gpt2_reply))
    dp.add_handler(CommandHandler("qa", turing_qa))

    dp.add_handler(CommandHandler('returns', last_returns))

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