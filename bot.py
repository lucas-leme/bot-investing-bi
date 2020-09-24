# import telebot
# import os
# import logging
# import os
# import random
# import sys

# import telegram
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# TOKEN = '1182419980:AAHaPWcy9eBRK3Ne8LSy8UaiMCaSPqbm8-U'#os.environ['TELEGRAM_TOKEN']

# bot = telebot.TeleBot(TOKEN)

# def run(updater):
#     PORT = int(os.environ.get("PORT", "8443"))
#     HEROKU_APP_NAME = os.environ.get("bot-telegram-turing")
#     # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
#     updater.start_webhook(listen="0.0.0.0",
#                           port=PORT,
#                           url_path=TOKEN)
#     updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
#     updater.idle()

# @bot.message_handler(commands=['start', 'help'])
# @bot.message_handler(commands=['help'])
# def send_welcome(message):
#     bot.reply_to(message, "Comandos: /quant; /nlp; /cv; /rl; /ds")


# # Descrição das Areas de foco

# #quant
# @bot.message_handler(commands=['quant'])
# def send_quant_describe(message):
#     bot.reply_to(message, 'Essa área de foco tem como principal objetivo estudar as aplicações de programação no mercado financeiro, através de determinadas plataformas. Buscamos, juntos, aprender tanto sobre mercado financeiro quanto sobre aplicações e métodos quantitativos utilizados nesse mercado.')

# #nlp
# @bot.message_handler(commands=['nlp'])
# def send_nlp_describe(message):
#     bot.reply_to(message, 'Processamento de Linguagem Natural é uma área da inteligência artificial cujo objetivo é a interpretação e manipulação de linguagens humanas. NLP tem muitas tarefas, algumas se relacionam ao processamento mais imediato dos componentes linguísticos, como a análise sintática, morfossintática (POS Tagging), lematização etc.')

# #cv
# @bot.message_handler(commands=['cv'])
# def send_cv_describe(message):
#     bot.reply_to(message, 'Em Computer Vision (ou Visão Computacional) trabalhamos principalmente com o processamento de imagens.')

# #rl
# @bot.message_handler(commands=['rl'])
# def send_rl_describe(message):
#     bot.reply_to(message, 'O Aprendizado por Reforço é uma das áreas mais únicas do Aprendizado de Máquina, fundamentada em ensinar a um agente como agir em um ambiente a partir de suas experiências.')

# #ds
# @bot.message_handler(commands=['ds'])
# def send_ds_describe(message):
#     bot.reply_to(message, 'Data Science (ou Ciência de Dados) é sobre obter insights ou conhecimento através do estudo e análise de dados')


# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.reply_to(message, "Salve, Salve Grupo Turing!")

# @bot.message_handler(regexp="Pistola")
# def handle_message(message):
#     bot.reply_to(message, "Vc quis dizer Azank??")
    
# @bot.message_handler(content_types=['document'])
# def handle_docs_audio(message):
#     bot.reply_to(message, "Oloko mandou a braba")
# bot.polling()

# if __name__ == '__main__':
#     updater = Updater(TOKEN, use_context=True)

#     updater.dispatcher.add_handler(CommandHandler("start", start_handler))
#     updater.dispatcher.add_handler(CommandHandler("random", random_handler))

#     run(updater)
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.environ['TELEGRAM_TOKEN']

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://bot-telegram-turing.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()