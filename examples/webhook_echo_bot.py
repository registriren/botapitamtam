#!/usr/bin/python
# -*- coding: utf-8 -*-


# для подписки на webhook через @primebot и команду /set_webhook
# задать адрес и порт (см. конец кода) сервера где размещен бот
# например: http://123.123.123.123:33333 или http://myserver.com:17235
# допустимые порты 80, 8080, 443, 8443, 16384-32383
# это простой, но не безопасный способ, представлен для понимания работы

from botapitamtam import BotHandler
import json
import logging
from flask import Flask, request, jsonify  # для webhook

config = 'config.json' # файл, содержащий токен доступа к боту в формате json, размещается в каталоге с ботом
# токен получаем через @primebot, формат файла config.json :
# {
# "access_token": "vIhiiW6OX2qYfbwoKyatxqiXDdjeqRgxgj56v-8Ixxx"
# }
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
        upd = request.get_json()  # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # этот способ не формирует событие (mark_seen) о прочтении ботом сообщения, нужно формировать его самостоятельно 
        if upd:  # основной код, для примера представлен эхо-бот
            chat_id = bot.get_chat_id(upd)
            text = bot.get_text(upd)
            bot.send_message(text, chat_id)
            logger.info('Сообщение получено и отправлено')
        return jsonify(upd)  # для webhook


if __name__ == '__main__':  # для webhook
    try:
        app.run(port=23432, host="0.0.0.0") # порт нужно выбирать нестандартный для уменьшения количества атак
    except KeyboardInterrupt:
        exit()
