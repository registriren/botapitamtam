from botapitamtam import BotHandler
import time

token = 'access_token_primebot'  # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)


def main():
    bot.send_message('Напишите что-нибудь', bot.get_chat_id())
    while True:  # цикл ожидания взаимодействия с ботом, в данном примере необходимо ввести любой текст
        last_update = bot.get_updates()  # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if last_update:  # проверка на пустое событие, если пусто - возврат к началу цикла
            chat_id = bot.get_chat_id(last_update)  # получаем chat_id диалога с ботом
            update = bot.send_message("это сообщение будет удалено через 5 сек...",
                                      chat_id)  # отправляем текстовое сообщение в чат (диалог)
            mid = bot.get_message_id(update)  # получаем messаge_id сообщения (контента)
            time.sleep(3)  # ждем 3 сек
            bot.delete_message(mid)
        continue


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
