import requests
import json

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.url = 'https://botapi.tamtam.chat/'

    def get_updates(self):
        """
        This method is used to get updates from bot via get request. It is based on long polling.
        https://dev.tamtam.chat/#operation/getUpdates
        """
        method = 'updates'
        params = {
            "timeout": 90,
            "limit": 100,
            "marker": None,
            "types": None,
            "access_token": self.token
        }
        response = requests.get(self.url + method, params)
        update = response.json()
        if len(update['updates']) == 0:
            update = None
        return update

    def get_update_type(self, update):
        """
        :param update: результат работы метода get_update
        :return: возвращает значение поля 'update_type', при неудаче = None
        """
        type = None
        if update != None:
            upd = update['updates'][0]
            type = upd.get('update_type')
        return type

    def get_text(self, update):
        """
        :param update: результат работы метода get_update
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

    def get_chat_id(self, update):
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

    def get_payload(self, update):
        """
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
        :param text: text of message
        :param chat_id: integer, chat id of user
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
        :param text: text of message
        :param chat_id: integer, chat id of user
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




