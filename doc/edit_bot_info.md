## edit_bot_info(name, username, description, commands, photo, photo_url=None)
https://dev.tamtam.chat/#operation/editMyInfo  
Метод редактирует текущую информацию о боте.  
:param **name:** имя бота  
:param **username:** уникальное имя (@my_bot) бота без знака "@"  
:param **description:** описание бота  
:param **commands:** = [{"name": '/команда', "description": "Описание команды"}]  
:param **photo:** файл с изображением  
:param **photo_url:** ссылка на изображение  
:return **edit_bot_info:** возвращает результат PATCH запроса  

## Пример
```python
# Этот пример показывает как можно отредактировать информацию бота

from botapitamtam import BotHandler

token = 'access_token_primebot' # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)

def main():
    marker = None
    while True:
        update = bot.get_updates(marker)
        # pprint(update)
        if update is None:
            continue
        updates = update['updates']
        for last_update in list(updates):
            commands = [{"name": '/команда_1', "description": "Описание команды 1"},
                        {"name": '/команда_2', "description": "Описание команды 2"},
                        {"name": '/команда_3', "description": "Описание команды 3"},
                        {"name": '/команда_4', "description": "Описание команды 4"}]
            photo = 'e.jpg'
            photo_url = ''  # ссылка на изображение
            bot.edit_bot_info(name='Супер бот',  # если для имени не нужно изменение, достаточно написать: name=None
                              username='superbot01',
                              description='Описание бота',
                              commands=commands,
                              photo=photo,
                              photo_url=None)
            
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
```