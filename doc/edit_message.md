## edit_content(message_id, attachments, text=None, link=None, notify=True)  
https://dev.tamtam.chat/#operation/editMessage  
Метод  изменения (обновления) любого контента по его идентификатору  
:param **message_id:** Идентификатор редактируемого контента  
:param **attachments:** Новый массив объектов (файл, фото, видео, аудио, кнопки)  
:param **text:** Обновленное текстовое сообщение  
:param **link:** Обновленное пересылаемые (цитируемые) сообщение  
:param **notify:** Уведомление о событии, если значение false, участники чата не будут уведомлены  
:return **update:** Возвращает результат PUT запроса  

## Пример
```python
# этот пример показывает как можно сформировать и изменить совокупный контент

from botapitamtam import BotHandler
import time

token = 'access_token_primebot' # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)

def main():
    marker = None
    while True:
        update = bot.get_updates(
            marker)  # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if update == None:  # проверка на пустое событие, если пусто - возврат к началу цикла
            continue
        marker = bot.get_marker(update)
        updates = update['updates']
        for last_update in list(
                updates):  # формируем цикл на случай если updates вернул список из нескольких событий
            chat_id = bot.get_chat_id(last_update)
            
            cont_img = 'test.png'     # тестовый файл изображения в рабочем каталоге
            cont_video = 'movie.mp4'  # тестовый файл видео в рабочем каталоге
           
            button = bot.button_link('Открыть mail.ru', 'http://mail.ru') # готовим первую кнопку
            button2 = bot.button_link('Открыть ok.ru', 'http://ok.ru') # готовим вторую кнопку
            button.extend(button2) # формируем кнопки в строку
            buttons = [button]

            image = bot.attach_image(cont_img)    # подготовка изображения к совокупной отправке
            video = bot.attach_video(cont_video)  # подготовка видео к совокупной отправке
            key = bot.attach_buttons(buttons)     # подготовка кнопки к совокупной отправке

            attach = image + video + key

            upd = bot.send_content(attach, chat_id, text='текст начальный') # совокупная отправка контента
            mid = bot.get_message_id(upd) # получаем идентификатор отправленного контента

            upd = bot.send_message('Через 5 сек. всё изменится...', chat_id) 
            mid1 = bot.get_message_id(upd)
            time.sleep(2)
            bot.delete_message(mid1)
                # готовим контент к изменению
            cont_img = 'test2.png' # файл должен быть в рабочем каталоге
            cont_video = 'voko.mkv' # файл должен быть в рабочем каталоге
            
            button = bot.button_callback('Новая кнопка 1', 'short')
            button2 = bot.button_callback('Новая кнопка 2', 'long')
            buttons = [button, button2] # формируем кнопки в колонку

            image = bot.attach_image(cont_img)
            video = bot.attach_video(cont_video)
            key = bot.attach_buttons(buttons)

            attach = image + video + key

            bot.edit_content(mid, attach, text='ТЕКСТ ИЗМЕНЁННЫЙ') # изменяем загруженный контент
            
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
```
