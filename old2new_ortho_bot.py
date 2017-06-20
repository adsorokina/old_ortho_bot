"""Телеграм-бот, переводящий из старой орфографии в новую
и возвращающий пользователю ответ в виде транслитерированного
текста. Нужно использовать вот этот код:
https://github.com/shelari/prereform_to_contemporary или
этот веб-сервис:http://web-corpora.net/wsgi/tolstoi_translit.wsgi/"""

import flask 
import telebot
import conf
from phrases import info, decline
import random
from utils import process_old2new

#WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
#WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
#bot.remove_webhook()
#bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands=['help', 'start'])  #'func=lambda m: True)
def send_welcome(message):
    bot.send_message(message.chat.id, info)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    contemp_text = process_old2new(message.text)
    bot.send_message(message.chat.id, contemp_text)

@bot.message_handler(content_types=['document', 'photo'])
def handle_file(message):
    bot.send_message(message.chat.id, random.choice(decline))
    
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

