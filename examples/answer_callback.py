from botapitamtam import BotHandler
import time

token = 'access_token_primebot' # токен, полученный при создании бота в @PrimeBot

bot = BotHandler(token)

def main():
    marker = None
    n = 0 
    chat_id = bot.get_chat_id() # Получаем chat_id последнего активного диалога с ботом
    bot.send_message("Напишите любое сообщение", chat_id)
    while True:
        last_update = bot.get_updates(
            marker)  # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if last_update == None:  # проверка на пустое событие, если пусто - возврат к началу цикла
            continue
        marker = bot.get_marker(last_update)
        chat_id = bot.get_chat_id(last_update)  # получаем chat_id диалога с ботом
        type = bot.get_update_type(last_update)
        callback_id = bot.get_callback_id(last_update)
        if bot.get_text(last_update) != None:
            buttons = bot.button_callback('Test', 'ok') # готовим кнопку
            bot.send_buttons(time.ctime(), buttons, chat_id)
        if type == 'message_callback':
            if callback_id != None:
                n += 1
                key = bot.button_callback('Test[{}]'.format(n), 'ok') # готовим кнопку
                attach = bot.attach_buttons(key) # при необходимости можно добавить еще attach путем сложения 
                text = time.ctime()
                bot.send_answer_callback(callback_id, 'test well...', text=text,
                                         attachments=attach) # выводим кратковременное уведомление и скорректированное событие по его callback_id
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
