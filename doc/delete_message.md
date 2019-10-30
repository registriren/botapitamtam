## delete_message(message_id)
https://dev.tamtam.chat/#operation/deleteMessage  
Удаляет сообщение (контент) по его message_id. В диалоге с ботом возможно удаление только сообщений созданных ботом, в чатах удаление сообщений возможно при наличии у бота прав администратора.  
**message_id** получаем методом [get_message_id(update)](get_message_id.md).  
**update** получаем методом [get_updates](get_updates.md).  
## Пример
```python
from botapitamtam import BotHandler
import time

token = 'access_token_primebot' # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)

def main():
    marker = None
    while True: # цикл ожидания взаимодействия с ботом, в данном примере необходимо ввести любой текст
        last_update = bot.get_updates(marker) # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if last_update == None:  # проверка на пустое событие, если пусто - возврат к началу цикла
            continue
        marker = bot.get_marker(last_update) # получение маркера очередного сообщения
        chat_id = bot.get_chat_id(last_update) # получаем chat_id диалога с ботом
        update = bot.send_message("это сообщение будет удалено через 5 сек...", chat_id)  # отправляем текстовое сообщение в чат (диалог)
        mid = bot.get_message_id(update)  # получаем messаge_id сообщения (контента)
        time.sleep(3)  # ждем 5 сек
        bot.delete_message(mid)
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
``` 
