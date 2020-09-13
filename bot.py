import telebot
import os
import logging
import os
import random
import sys

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(TOKEN)

def run(updater):
    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("bot-telegram-turing")
    # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
    updater.idle()

@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Comandos: /quant; /nlp; /cv; /rl; /ds")


# Descrição das Areas de foco

#quant
@bot.message_handler(commands=['quant'])
def send_quant_describe(message):
    #text_quant = open("./text_files/quant_describe.txt", "r")
    bot.reply_to(message, 'Essa área de foco tem como principal objetivo estudar as aplicações de programação no mercado financeiro, através de determinadas plataformas. Buscamos, juntos, aprender tanto sobre mercado financeiro quanto sobre aplicações e métodos quantitativos utilizados nesse mercado.')

#nlp
@bot.message_handler(commands=['nlp'])
def send_nlp_describe(message):
    #text_nlp = open("./text_files/nlp_describe.txt", "r")
    bot.reply_to(message, 'Processamento de Linguagem Natural é uma área da inteligência artificial cujo objetivo é a interpretação e manipulação de linguagens humanas. NLP tem muitas tarefas, algumas se relacionam ao processamento mais imediato dos componentes linguísticos, como a análise sintática, morfossintática (POS Tagging), lematização etc.')

#cv
@bot.message_handler(commands=['cv'])
def send_cv_describe(message):
    #text_cv = open("./text_files/cv_describe.txt", "r")
    bot.reply_to(message, 'Em Computer Vision (ou Visão Computacional) trabalhamos principalmente com o processamento de imagens.')

#rl
@bot.message_handler(commands=['rl'])
def send_rl_describe(message):
    #text_rl = open("./text_files/rl_describe.txt", "r")
    bot.reply_to(message, 'O Aprendizado por Reforço é uma das áreas mais únicas do Aprendizado de Máquina, fundamentada em ensinar a um agente como agir em um ambiente a partir de suas experiências.')

#ds
@bot.message_handler(commands=['ds'])
def send_ds_describe(message):
    #text_ds = open("./text_files/ds_describe.txt", "r")
    bot.reply_to(message, 'Data Science (ou Ciência de Dados) é sobre obter insights ou conhecimento através do estudo e análise de dados')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salve, Salve Grupo Turing!")

@bot.message_handler(regexp="Pistola")
def handle_message(message):
    bot.reply_to(message, "Vc quis dizer Azank??")
    
@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    bot.reply_to(message, "Oloko mandou a braba")
bot.polling()

if __name__ == '__main__':
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("random", random_handler))

    run(updater)
