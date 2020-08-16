from botapitamtam import BotHandler

token = 'access_token_primebot'  # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)


def post_posting(sid, post_txt, post_attach):
    key = []
    if post_txt:
        comment = post_txt
    else:
        comment = 'Чат для обсуждения'
    title_chat = comment[:120]
    descript_chat = 'Обсуждаем пост:\n' + comment[:380]
    start_text_chat = comment[:508] + '...'
    button = bot.button_chat('\U0001F4AC Обсудить', title_chat, chat_description=descript_chat,
                             start_payload=start_text_chat)
    key.append([button])
    attach = bot.attach_buttons(key)
    attachments = post_attach
    if not attachments:
        attachments = []
    if not attach:
        attach = []
    attachments = attachments + attach
    title = post_txt
    key_clr = bot.button_callback('\U0000274E Сбросить', 'clr', intent='negative')
    key = [[key_clr]]
    bot.send_construct_message(sid, 'Пост подготовлен', text=title, attachments=attachments,
                               buttons=key, allow_user_input=False)


def main():
    post_txt = ''
    post_attach = []
    while True:
        upd = bot.get_updates()  # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if upd:
            type_upd = bot.get_update_type(upd)
            if type_upd == 'message_constructed':
                post_txt = ''
                post_attach = []
            if type_upd == 'message_chat_created':
                chat_id = bot.get_chat_id(upd)
                start_text = bot.get_start_payload(upd)
                bot.send_message(start_text, chat_id)
            if type_upd == 'message_construction_request':
                payload = bot.get_payload(upd)
                sid = bot.get_session_id(upd)
                text = bot.get_text(upd)
                attachments = bot.get_attachments(upd)
                if text or attachments:
                    if text:
                        post_txt = text
                    if attachments:
                        post_attach = attachments
                    post_posting(sid, post_txt, post_attach)
                else:
                    bot.send_construct_message(sid,
                                               'Введите текст вашего поста и прикрепите необходимый контент (фото, видео). Другой тип контента поддерживается с ограничениями.')
                if payload == 'clr':
                    bot.send_construct_message(sid,
                                               'Введите текст вашего поста и прикрепите необходимый контент (фото, видео). Другой тип контента поддерживается с ограничениями.')
                    post_txt = ''
                    post_attach = []


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
