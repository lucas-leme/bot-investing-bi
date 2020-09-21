# Funções do Alan
import telebot
# Insira o token
import os
Token = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Comandos: /quant; /nlp; /cv; /rl; /ds")


# Descrição das Areas de foco

#quant
@bot.message_handler(commands=['quant'])
def send_quant_describe(message):
    text_quant = 'melhor área'
    bot.reply_to(message, text_quant)

#nlp
@bot.message_handler(commands=['nlp'])
def send_nlp_describe(message):
    text_nlp = 'open("./text_files/nlp_describe.txt", "r")'
    bot.reply_to(message, text_nlp)

#cv
@bot.message_handler(commands=['cv'])
def send_cv_describe(message):
    text_cv = 'open("./text_files/cv_describe.txt", "r")'
    bot.reply_to(message, text_cv)

#rl
@bot.message_handler(commands=['rl'])
def send_rl_describe(message):
    text_rl = 'open("./text_files/rl_describe.txt", "r")'
    bot.reply_to(message, text_rl)

#ds
@bot.message_handler(commands=['ds'])
def send_ds_describe(message):
    text_ds = 'open("./text_files/ds_describe.txt", "r")'
    bot.reply_to(message, text_ds)


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