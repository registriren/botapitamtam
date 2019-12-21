# Этот пример показывает как можно отредактировать информацию о боте

from botapitamtam import BotHandler

token = 'access_token_primebot'  # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)

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

