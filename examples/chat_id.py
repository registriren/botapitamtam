from botapitamtam import BotHandler
import time

token = 'access_token_primebot'  # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)


def main():
    chat_id = bot.get_chat_id()
    bot.send_message("Напишите любое сообщение", chat_id)
    while True:  # цикл ожидания взаимодействия с ботом
        update = bot.get_updates()  # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if update:  # проверка на пустое событие, если пусто - возврат к началу цикла
            chat_id = bot.get_chat_id(update)  # получаем chat_id диалога с ботом
            bot.send_message("привет, я бот", chat_id)  # отправляем текстовое сообщение в чат (диалог)
        continue


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
