# пример получения информации из пересланного боту сообщения
from botapitamtam import BotHandler
import json

token = 'access_token_primebot'  # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)


def main():
    marker = None
    while True:
        last_update = bot.get_updates(marker)
        if last_update == None:  # проверка на пустое событие, если пусто - возврат к началу цикла
            continue
        marker = bot.get_marker(last_update)
        chat_id = bot.get_chat_id(last_update)
        user_id = bot.get_user_id(last_update)
        name = bot.get_name(last_update)
        link_userid = bot.get_link_user_id(last_update)
        link_name = bot.get_link_name(last_update)
        link_chatid = bot.get_link_chat_id(last_update)

        if link_userid != None:
            bot.send_message(
                'forward name: {}\nforward user_id: {}\nforward chat_id: {}\n'.format(link_name, link_userid,
                                                                                      link_chatid), chat_id)
        elif link_chatid != None:
            bot.send_message(
                'forward name: {}\nforward user_id: {}\nforward chat_id: {}\n'.format(link_name, link_userid,
                                                                                      link_chatid), chat_id)
        else:
            bot.send_message('name: {}\nuser_id: {}\nchat_id: {}\n'.format(name, user_id, chat_id), chat_id)
        update = json.dumps(last_update, ensure_ascii=False, indent=4)
        bot.send_message('полная структура ответа GetUpdates:\n{}'.format(str(update)), chat_id)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
