## get_chat_id(update=None)
Получает ID чата (диалога) в которм происходит взаимодействие с ботом.  
**update** получаем методом [get_updates](get_updates.md). Если **update**=None, то возвращается chat_id последнего активного диалога.
## Пример:
```python
from botapitamtam import BotHandler
import time

token = 'access_token_primebot' # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)

def main():
    marker = None
    chat_id = bot.get_chat_id()
    bot.send_message("Напишите любое сообщение", chat_id)
    while True: # цикл ожидания взаимодействия с ботом
        update = bot.get_updates(marker) # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if update == None:  # проверка на пустое событие, если пусто - возврат к началу цикла
            continue
        marker = bot.get_marker(update) # получение маркера очередного сообщения
        chat_id = bot.get_chat_id(update) # получаем chat_id диалога с ботом
        bot.send_message("привет, я бот", chat_id)  # отправляем текстовое сообщение в чат (диалог)
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
``` 
