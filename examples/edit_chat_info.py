# Этот пример показывает как можно отредактировать информацию чата.

from botapitamtam import BotHandler

token = 'access_token_primebot'  # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)


def main():
    while True:
        update = bot.get_updates()  # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if update:  # проверка на пустое событие, если пусто - возврат к началу цикла
            updates = update['updates']
            for last_update in list(
                    updates):  # формируем цикл на случай если updates вернул список из нескольких событий
                chat_id = bot.get_chat_id(last_update)
                icon = 'icon.jpg'  # путь до файла.
                icon_url = ''  # ссылка на изображение.
                bot.edit_chat_info(chat_id, icon=icon, title='Заголовок!', icon_url=None)
        continue


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
