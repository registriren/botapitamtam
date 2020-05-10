#!/usr/bin/python
# -*- coding: utf-8 -*-


# для подписки на webhook через @primebot и команду /set_webhook
# задать адрес и порт (см. конец кода) сервера где размещен бот
# в формате: http://123.123.123.123:33333
# это простой, но не безопасный способ, представлен для понимания работы

from botapitamtam import BotHandler
import json
import logging
from flask import Flask, request, jsonify  # для webhook

config = 'config.json' # файл, содержащий токен доступа к боту в формате json, размещается в каталоге с ботом
with open(config, 'r', encoding='utf-8') as c:
    conf = json.load(c)
    token = conf['access_token']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = BotHandler(token)

app = Flask(__name__)  # для webhook


@app.route('/', methods=['POST'])  # для webhook
def main():
    while True:
        upd = bot.get_updates()  # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if upd:  # основной код, для примера представлен эхо-бот
            chat_id = bot.get_chat_id(upd)
            text = bot.get_text(upd)
            bot.send_message(text, chat_id)
            logger.info('Сообщение получено и отправлено')
        return jsonify(upd)  # для webhook


if __name__ == '__main__':  # для webhook
    try:
        app.run(port=29347, host="0.0.0.0") # порт нужно выбирать нестандартный для уменьшения количиства атак
    except KeyboardInterrupt:
        exit()
