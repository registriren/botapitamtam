import requests
import json

class BotHandler:
    """
    обработчик комманд
    """
    
    def __init__(self, token):
        self.token = token
        self.url = 'https://botapi.tamtam.chat/'

    def get_updates(self, marker=None):
        """
        Основная функция опроса состояния (событий) бота методом long polling
        This method is used to get updates from bot via get request. It is based on long polling.
        https://dev.tamtam.chat/#operation/getUpdates
        API = subscriptions/Get updates/
        """
        method = 'updates'
        params = {
            "timeout": 45,
            "limit": 100,
            "marker": marker,
            "types": None,
            "access_token": self.token
        }
        try:
            response = requests.get(self.url + method, params)
            update = response.json()
            if len(update['updates']) == 0:
                update = None
        except ConnectionError:
            update = None
        return update

    def get_marker(self, update):
        """
        Метод получения маркера события
        API = subscriptions/Get updates/[marker]
        :param update = результат работы метода get_update
        :return: возвращает значение поля 'marker', при неудаче = None
        """
        marker = None
        if update != None:
            marker = update['marker']
        return marker


    def get_members(self, chat_id):
        method = 'chats/{}'.format(chat_id) + '/members'
        params = {
            "access_token": self.token
        }
        response = requests.get(self.url + method, params)
        #members = (self.url + method, params)
        members = response.json()
        #if len(members['members']) == 0:
        #    members = None
        return members


    def get_update_type(self, update):
        """
        Метод получения типа события произошедшего с ботом
        API = subscriptions/Get updates/[updates][0][update_type]
        :param update = результат работы метода get_update
        :return: возвращает значение поля 'update_type', при неудаче = None
        """
        type = None
        if update != None:
            upd = update['updates'][0]
            type = upd.get('update_type')
        return type

    def get_text(self, update):
        """
        Получение текста отправленного или пересланного боту
        API = subscriptions/Get updates/[updates][0][message][link][message][text] (type = 'forward')
           или = subscriptions/Get updates/[updates][0][message][body][text]
        :param update = результат работы метода get_update
        :return: возвращает, если это возможно, значение поля 'text' созданного или пересланного сообщения
                 из 'body' или 'link'-'forward' соответственно, при неудаче 'text' = None
        """
        text = None
        if update != None:
            upd = update['updates'][0]
            type = self.get_update_type(update)
            if type == 'message_created':
                upd = upd.get('message')
                text = upd.get('body').get('text')
                if 'link' in upd.keys():
                   if upd.get('link').get('type') == 'forward':
                       text = upd.get('link').get('message').get('text')

        return text

    def get_url(self, update):
        """
        Получение ссылки отправленного или пересланного боту файла
        API = subscriptions/Get updates/[updates][0][message][link][message][attachment][url]
           или = subscriptions/Get updates/[updates][0][message][body][attachment][url]
        :param update = результат работы метода get_update
        :return: возвращает, если это возможно, значение поля 'url' созданного или пересланного файла
                 из 'body' или 'link' соответственно, при неудаче 'url' = None
        """
        url = None
        if update != None:
            upd = update['updates'][0]
            type = self.get_update_type(update)
            if type == 'message_created':
                upd1 = upd.get('message').get('body')
                if 'attachments' in upd1.keys():
                    upd1 = upd1['attachments'][0]
                    if 'payload' in upd1.keys():
                        upd1 = upd1.get('payload')
                        if 'url' in upd1.keys():
                            url = upd1.get('url')
                else:
                    upd1 = upd.get('message')
                    if 'link' in upd1.keys():
                        upd1 = upd1.get('link')
                        if 'message' in upd1.keys():
                            upd1 = upd1.get('message')
                            if 'attachments' in upd1.keys():
                                upd1 = upd1['attachments'][0]
                                if 'payload' in upd1.keys():
                                    upd1 = upd1.get('payload')
                                    if 'url' in upd1.keys():
                                        url = upd1.get('url')
        return url

    def get_chat_id(self, update):
        """
        Получения идентификатора чата, в котором произошло событие
        API = subscriptions/Get updates/[updates][0][chat_id]
           или = subscriptions/Get updates/[updates][0][message][recipient][chat_id]
        :param update = результат работы метода get_update
        :return: возвращает, если это возможно, значение поля 'chat_id' не зависимо от события, произошедшего с ботом
                 если событие - "удаление сообщения", то chat_id = None
        """
        chat_id = None
        if update != None:
            upd = update['updates'][0]
            if 'message_id' in upd.keys():
                chat_id = None
            elif 'chat_id' in upd.keys():
                 chat_id = upd.get('chat_id')
            else:
                upd = upd.get('message')
                chat_id = upd.get('recipient').get('chat_id')
        return chat_id
    
    def get_link_chat_id(self, update):
        """
        Получения идентификатора чата пересланного сообщения
        API = subscriptions/Get updates/[updates][0][message][link][chat_id]
        :param update = результат работы метода get_update
        :return: возвращает, если это возможно, значение поля 'chat_id' пересланного боту сообщения (от кого)
        """
        chat_id = None
        if update != None:
            upd = update['updates'][0]
            if 'message' in upd.keys():
                upd = upd['message']
                if 'link' in upd.keys():
                    upd = upd['link']
                    if 'chat_id' in upd.keys():
                        chat_id = upd['chat_id']
        return chat_id
    
    def get_user_id(self, update):
        """
        Получения идентификатора пользователя, инициировавшего событие
        API = subscriptions/Get updates/[updates][0][user][user_id]
           или = subscriptions/Get updates/[updates][0][message][sender][user_id]
        :param update = результат работы метода get_update
        :return: возвращает, если это возможно, значение поля 'user_id' не зависимо от события, произошедшего с ботом
                 если событие - "удаление сообщения", то user_id = None
        """
        user_id = None
        if update != None:
            upd = update['updates'][0]
            if 'message_id' in upd.keys():
                user_id = None
            elif 'chat_id' in upd.keys():
                user_id = upd['user']['user_id']
            elif 'callback' in upd.keys():
                user_id = upd['callback']['user']['user_id']
            else:
                upd = upd['message']
                if 'sender' in upd.keys():
                    user_id = upd['sender']['user_id']
                else:
                    user_id = upd['recipient']['user_id']
        return user_id
    
    def get_link_user_id(self, update):
        """
        Получения идентификатора пользователя пересланного сообщения
        API = subscriptions/Get updates/[updates][0][message][link][sender][user_id]
        :param update = результат работы метода get_update
        :return: возвращает, если это возможно, значение поля 'user_id' пересланного боту сообщения (от кого)
        """
        user_id = None
        if update != None:
            upd = update['updates'][0]
            if 'message' in upd.keys():
                upd = upd['message']
                if 'link' in upd.keys():
                    upd = upd['link']
                    if 'sender' in upd.keys():
                        user_id = upd['sender']['user_id']
        return user_id

    def get_name(self, update):
        """
        Получение имени пользователя, инициировавшего событие
        API = subscriptions/Get updates/[updates][0][user][user_id]
           или = subscriptions/Get updates/[updates][0][message][sender][user_id]
        :param update = результат работы метода get_update
        :return: возвращает, если это возможно, значение поля 'name' не зависимо от события, произошедшего с ботом
                 если событие - "удаление сообщения", то name = None
        """
        name = None
        if update != None:
            upd = update['updates'][0]
            if 'message_id' in upd.keys():
                name = None
            elif 'chat_id' in upd.keys():
                name = upd['user']['name']
            elif 'callback' in upd.keys():
                name = upd['callback']['user']['name']
            else:
                upd = upd['message']
                if 'sender' in upd.keys():
                    name = upd['sender']['name']
                else:
                    name = None
        return name

    def get_link_name(self, update):
        """
        Получение имени пользователя пересланного сообщения
        API = subscriptions/Get updates/[updates][0][message][link][sender][name]
        :param update = результат работы метода get_update
        :return: возвращает, если это возможно, значение поля 'name' пересланного боту сообщения (от кого)
        """
        name = None
        if update != None:
            upd = update['updates'][0]
            if 'message' in upd.keys():
                upd = upd['message']
                if 'link' in upd.keys():
                    upd = upd['link']
                    if 'sender' in upd.keys():
                        name = upd['sender']['name']
        return name
    
    def get_payload(self, update):
        """
        API = subscriptions/Get updates/[updates][0][callback][payload]
        :param update: результат работы метода get_update
        :return: возвращает результат нажатия кнопки или None
        """
        payload = None
        if update != None:
            upd = update['updates'][0]
            type = self.get_update_type(update)
            if type == 'message_callback':
                upd = upd.get('callback')
                if 'payload' in upd.keys():
                    payload = upd.get('payload')
        return payload

    def send_message(self, text, chat_id):
        """
        Send message to specific chat_id by post request
        Отправляет сообщение в соответствующий чат
        API = messages/Send message/{text}
        :param text: text of message / текст сообщения
        :param chat_id: integer, chat id of user / чат куда поступит сообщение
        :return
        """
        method = 'messages?access_token='
        url = ''.join([self.url, method, self.token, '&chat_id={}'.format(chat_id)])
        params = {"text": text}
        response = requests.post(url, data=json.dumps(params))
        if response.status_code != 200:
            print("Error sending message: {}".format(response.status_code))

    def send_buttons(self, text, buttons, chat_id):
        """
        Send buttons to specific chat_id by post request
        Отправляет кнопки (количество и функционал определяются параметром buttons) в соответствующий чат
        :param text: Текст выводимый над блоком кнопок
        :param chat_id: integer, chat id of user / чат где будут созданы кнопки
        :param buttons = [{"type": 'callback',
                           "text": 'key1_text',
                           "payload": 'payload1'},
                          {"type": 'link',
                           "text": 'API TamTam',
                           "url": 'https://dev.tamtam.chat',
                           "intent": 'positive'}]
                           :param type: реакция на нажатие кнопки
                           :param text: подпись кнопки
                           :param payload: результат нажатия кнопки
                           :param intent: цвет кнопки
        """
        method = 'messages?access_token='
        url = ''.join([self.url, method, self.token, '&chat_id={}'.format(chat_id)])
        params = {
                 "text": text,
                 "attachments": [
                    {
                        "type": "inline_keyboard",
                        "payload": {
                            "buttons": [
                                        buttons
                                       ]
                                    }
                    }
                                ]
                 }
        response = requests.post(url, data=json.dumps(params))
        if response.status_code != 200:
            print("Error sending message: {}".format(response.status_code))




