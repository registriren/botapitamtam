## edit_chat_info(chat_id, icon, title, icon_url=None)
https://dev.tamtam.chat/#operation/editChat  
Метод редактирования информации чата (заголовок и значок)   
:param **chat_id:** Идентификатор изменяемого чата  
:param **icon:** Иконка чата в виде файла  
:param **title:** Заголовок чата  
:param **icon_url:** Ссылка на изображение (по умолчанию парамет пустой и может не указываться)    
:return **chat_info:** Возвращает информацию о параметрах измененного чата  

Если параметр **icon_url** не пустой, то параметр **icon** не рассматривается.  

## Пример
```python
# Этот пример показывает как можно отредактировать информацию чата.

from botapitamtam import BotHandler

token = 'access_token_primebot' # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)

def main():
    marker = None
    while True:
        update = bot.get_updates(marker)  # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if update == None:  # проверка на пустое событие, если пусто - возврат к началу цикла
            continue
        marker = bot.get_marker(update)
        updates = update['updates']
        for last_update in list(updates):  # формируем цикл на случай если updates вернул список из нескольких событий
            chat_id = bot.get_chat_id(last_update)
            icon = 'icon.jpg' # путь до файла.
            icon_url = '' # ссылка на изображение.
            bot.edit_chat_info(chat_id, icon=icon, title='Заголовок!', icon_url=None)
            
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
```
