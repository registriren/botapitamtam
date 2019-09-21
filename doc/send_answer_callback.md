## send_answer_callback(callback_id, notification, message=None)  
https://dev.tamtam.chat/#operation/answerOnCallback  
        Метод отправки любого контента, сформированного в соответсвии с документацией, в указанный чат  
        :param callback_id: параметр, соответствующий нажатой кнопке  
        :param notification: кратковременное, всплывающее уведомление  
        :param message: объекты в соответствии с API  
        :return update: результат POST запроса  
## Пример:
```python
from botapitamtam import BotHandler

token = 'access_token_primebot' # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)

def main():
    marker = None
    while True: # цикл ожидания взаимодействия с ботом, в данном примере необходимо ввести любой текст
        update = bot.get_updates(marker) # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if update == None:  # проверка на пустое событие, если пусто - возврат к началу цикла
            continue
        marker = bot.get_marker(last_update) # маркер следующего события в боте
        chat_id = bot.get_chat_id(last_update)  # получаем chat_id диалога с ботом
        type_upd = bot.get_update_type(last_update) # получаем update_type события в боте
        callback_id = bot.get_callback_id(last_update) # получаем callback_id если кнопка была нажата, или None
        if bot.get_text(last_update) != None:
            buttons = [[{"type": 'callback',
                         "text": 'Test',
                         "payload": 'ok'
                         }]
                       ]
            bot.send_buttons("Test notification", buttons, chat_id)
        if type_upd == 'message_callback':
            if callback_id != None:
                bot.send_answer_callback(callback_id, 'test well...') # выводим кратковременное уведомление
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
``` 
