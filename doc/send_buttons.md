## send_buttons(text, buttons, chat_id)  
Отправляет текстовое сообщение с кнопками (количество, рядность и функционал определяются параметром buttons) в соответствующий чат  
**:param text:** Текст выводимый над блоком кнопок  
**:param chat_id:** Чат где будут созданы кнопки  

        :param buttons = [
                          [{"type": 'callback',
                           "text": 'line1_key1_text',
                           "payload": 'payload1',
                           "intent": 'positive'},
                          {"type": 'link',
                           "text": 'line1_key2_API TamTam',
                           "url": 'https://dev.tamtam.chat'}],
                           [{"type": 'callback',
                           "text": 'line2_key1_text',
                           "payload": 'payload1',
                           "intent": 'negative'},
                          {"type": 'link',
                           "text": 'line2_key2_API TamTam',
                           "url": 'https://dev.tamtam.chat'}]
                         ]
                           :param type: реакция на нажатие кнопки
                           :param text: подпись кнопки
                           :param payload: результат нажатия кнопки
                           :param url: ссылка на ресурс
                           :param intent: цвет кнопки
        :return update: результат POST запроса на отправку кнопок
        
## Пример  
Это пример действующего бота для управления ботами, работающими на том же сервере. Бот позволяет получать лог, останавливать, запускать, обновлять (git pull) и  перезапускать боты на сервере при помощи соответствующих скриптов bash, размещенных в каталогах управляемых ботов.   
```python

from botapitamtam import BotHandler
import json
from subprocess import call
import os

token = 'access_token_primebot' # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)

user_id = 000000000000 # ваш user_id для авторизации
catalog = '/opt/' # рабочий каталог с ботами в нем находятся катологи с ботами
commands = {'list': None,                     
            'log': 'log.txt',
            'upd_restart': 'upd_restart.sh', # командные файлы действий с ботами (должны находится в каталоге каждого бота)
            'restart': 'restart.sh',
            'stop': 'stop.sh',
            'start': 'start.sh',
            'update': 'update.sh'
            }
botlist = ['filelink', 'gotranslate', 'userinfo', 'botapitamtam'] # список имен ботов (должны совпадать с именами каталогов                                                                                             ботов)


def menu(callback_id, chat_id, notifi=None):                # меню действий с ботами, если callback_id не None - меню
    key1 = bot.button_callback('Список ботов', 'list')      #  изменится, иначе сформируется заново
    key2 = bot.button_callback('Получить лог', 'log')
    key3 = bot.button_callback('Обновление и перезапуск', 'upd_restart')
    key4 = bot.button_callback('Перезапуск бота', 'restart')
    key5 = bot.button_callback('Остановка бота', 'stop')
    key6 = bot.button_callback('Запуск бота', 'start')
    key7 = bot.button_callback('Обновление бота', 'update')
    key = [key1, key2, key3, key4, key5, key6, key7] # так созданные кнопки формируются в столбец
    if callback_id != None:
        button = bot.attach_buttons(key) 
        message = {"text": 'Выберете действие',
                   "attachments": button}
        upd = bot.send_answer_callback(callback_id, notification=notifi, message=message) # отправляем кнопки с возможностью                                                                                              их изменения
    else:
        upd = bot.send_buttons('Выберете действие', key, chat_id) # простая отправка кнопок
    mid = bot.get_message_id(upd)
    return mid

def list_bot(callback_id, chat_id): # автоматическое формирование кнопок с именами ботов (выводится аналогично menu() )
    key = []
    back = bot.button_callback('Назад', 'home', intent='positive')
    for bots in botlist:
        button = bot.button_callback('@{}'.format(bots), bots)
        key.append(button)
    key.append(back)
    if callback_id != None:
        button = bot.attach_buttons(key)
        message = {"text": 'Выберете бота',
                   "attachments": button}
        upd = bot.send_answer_callback(callback_id, notification=None, message=message)
    else:
        upd = bot.send_buttons('Выберете бота', key, chat_id)
    mid = bot.get_message_id(upd)
    return mid


def main():
    marker = None
    mid_m = None # message_id текущего меню
    mid_d = None # message_id удаляемого (изменяемого) меню
    cmd = None
    while True:
        update = bot.get_updates(marker, limit=1)
        if update == None:
            continue
        marker = bot.get_marker(update)
        type_upd = bot.get_update_type(update)
        chat_id = bot.get_chat_id(update)
        payload = bot.get_payload(update)
        cbid = bot.get_callback_id(update) # 
        if user_id == bot.get_user_id(update): # авторизация пользователя бота по user_id
            if mid_m != None:
                mid_d = mid_m
            if type_upd == 'bot_started':
                mid_m = menu(callback_id=cbid, chat_id=chat_id)
            if type_upd == 'message_created':
                bot.delete_message(mid_d)
                payload = 'home'
            if payload == 'home':
                mid_m = menu(callback_id=cbid, chat_id=chat_id)
            if payload in botlist:
                os.chdir(catalog + payload)
                if cmd == 'log.txt':
                    cmd = catalog + payload + '/log.txt'
                    logger.info(cmd)
                    try:
                        if os.path.getsize(cmd) != 0:
                            bot.delete_message(mid_d)
                            bot.send_file(cmd, chat_id, text='Лог бота @{}'.format(payload))
                            mid_m = menu(callback_id=None, chat_id=chat_id)
                            cmd = None
                        else:
                            mid_m = menu(callback_id=cbid, chat_id=chat_id, notifi='Лог пустой')
                    except:
                        mid_m = menu(callback_id=cbid, chat_id=chat_id, notifi='Лог пустой')
                elif cmd != None:
                    try:
                        with open(cmd, 'rb') as file:
                            script = file.read()
                        rc = call(script, shell=True)
                        notifi = cmd + ' для бота @{}'.format(payload) + ' выполнил'
                        cmd = None
                        if rc == 0:
                            mid_m = menu(callback_id=cbid, chat_id=chat_id, notifi=notifi)
                        else:
                            mid_m = menu(callback_id=cbid, chat_id=chat_id, notifi='Жду команду')
                    except Exception as e:
                        mid_m = menu(callback_id=cbid, chat_id=chat_id, notifi=str(e))
                else:
                    mid_m = menu(callback_id=cbid, chat_id=chat_id, notifi='Жду команду')
            elif payload in commands:
                mid_m = list_bot(callback_id=cbid, chat_id=chat_id)
                cmd = commands[payload] # получаем команду, которая будет исполнена в следующем цикле 


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
```
