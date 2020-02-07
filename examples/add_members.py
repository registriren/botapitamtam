from botapitamtam import BotHandler

token = 'access_token_primebot'  # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)


def main():
    while True:  # цикл ожидания взаимодействия с ботом, в данном примере необходимо ввести любой текст
        last_update = bot.get_updates()  # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if last_update:  # проверка на пустое событие, если пусто - возврат к началу цикла
            text = bot.get_text(last_update)  # получаем текст сообщения.
            chat_id = bot.get_chat_id(last_update)  # получаем chat_id в чате (или канале)
            link_user_id = bot.get_link_user_id(
                last_update)  # получаем link_user_id сообщения пользователя из чата (или канала), если он там был.
            if text == '/add':  # пример команды для добавления пользователя в чаи
                bot.add_members(chat_id,
                                user_ids=link_user_id)  # так же в user_ids= можно передать user_id, если он нам известен.
                bot.send_message('Пользователь был добавлен в чат.', chat_id)
        continue


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
