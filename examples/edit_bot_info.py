# Этот пример показывает как можно отредактировать информацию о боте

from botapitamtam import BotHandler

token = 'access_token_primebot'  # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)

# commands = [{"name": '/команда_1', "description": "Описание команды 1"},
#            {"name": '/команда_2', "description": "Описание команды 2"},
#            {"name": '/команда_3', "description": "Описание команды 3"}]

commands = [bot.command('команда_1', 'Описание команды 1'),
            bot.command('команда_2', 'Описание команды 2'),
            bot.command('команда_3', 'Описание команды 3')]

photo = 'e.jpg'
photo_url = ''  # ссылка на изображение
bot.edit_bot_info(name='Супер бот',  # если для имени не нужно изменение, достаточно написать: name=None
                  username='superbot01',
                  description='Описание бота',
                  commands=commands,
                  photo=photo
                  )

