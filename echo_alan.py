# Funções do Alan

import telebot

# Insira o token
Token = ""

bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salve, Salve Grupo Turing!")

@bot.message_handler(regexp="Pistola")
def handle_message(message):
    bot.reply_to(message, "Vc quis dizer Azank??")
    
@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    bot.reply_to(message, "Oloko mandou a braba")

bot.polling()