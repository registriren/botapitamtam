# Version 0.2.0.2

import json
import logging
import os
import time

import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class BotHandler:
    """
    обработчик комманд
    """

    def __init__(self, token):
        self.token = token
        self.url = 'https://botapi.tamtam.chat/'

    def get_updates(self, marker=None, limit=100, timeout=30):
        """
        Основная функция опроса состояния (событий) бота методом long polling
        This method is used to get updates from bot via get request. It is based on long polling.
        https://dev.tamtam.chat/#operation/getUpdates
        API = subscriptions/Get updates/
        """
        method = 'updates'
        params = {
            "marker": marker,
            "limit": limit,
            "timeout": timeout,
            "types": None,
            "access_token": self.token
        }
        try:
            response = requests.get(self.url + method, params)
            update = response.json()
        except Exception as e:
            logger.error("Error get updates: %s.", e)
            update = {}
        if 'updates' in update.keys():
            if len(update['updates']) != 0:
                self.send_mark_seen(chat_id=self.get_chat_id(update))
            else:
                update = None
        else:
            update = None
        return update

    def get_subscriptions(self):
        """
        Если ваш бот получает данные через WebHook, метод возвращает список всех подписок.
        In case your bot gets data via WebHook, the method returns list of all subscriptions
        https://dev.tamtam.chat/#operation/getSubscriptions
        API = subscriptions
        :return: возвращает список подписок.
        """
        method = 'subscriptions'
        params = {
            "access_token": self.token,
        }
        try:
            response = requests.get(self.url + method, params=params)
            if response.status_code == 200:
                subscriptions = response.json()
            else:
                logger.error("Error get subscriptions: {}".format(response.status_code))
                subscriptions = None
        except Exception as e:
            logger.error("Error connect get subscriptions: %s.", e)
            subscriptions = None
        return subscriptions

    def subscribe(self, url, update_types, version):
        """
        Подписывается бот для получения обновлений через WebHook. После вызова этого метода бот будет получать
        уведомления о новых событиях в чатах по указанному URL.
        Subscribes bot to receive updates via WebHook. After calling this method, the bot will receive notifications
        about new events in chat rooms at the specified URL.
        https://dev.tamtam.chat/#operation/subscribe
        API = subscriptions
        :param url: URL HTTP(S) - точки входа вашего бота, должен начинаться с http(s)://
        :param update_types: список типов обновлений, которые хочет получить ваш бот [в разработке..]
        :param version: версия API
        :return: возвращает статус POST запроса
        """
        method = 'subscriptions'
        params = {
            "access_token": self.token,
        }
        data = {
            "url": url,
            "update_types": update_types,
            "version": version
        }
        try:
            response = requests.post(self.url + method, params=params, data=json.dumps(data))
            if response.status_code == 200:
                subscribe = response.json()
            else:
                logger.error("Error subscribes: {}".format(response.status_code))
                subscribe = None
        except Exception as e:
            logger.error("Error connect subscribes: %s.", e)
            subscribe = None
        return subscribe

    def unsubscribe(self, url):
        """
        Отменяет подписку бота на получение обновлений через WebHook. После вызова метода бот перестает получать
        уведомления о новых событиях. Уведомление через API длинного опроса становится доступным для бота
        Unsubscribes bot from receiving updates via WebHook. After calling the method, the bot stops receiving
        notifications about new events. Notification via the long-poll API becomes available for the bot
        https://dev.tamtam.chat/#operation/unsubscribe
        API = subscriptions
        :param url: URL для удаления из подписок WebHook
        :return: возвращает результат DELETE запроса
        """
        method = 'subscriptions'
        params = (
            ('access_token', self.token),
            ('url', url),
        )
        try:
            response = requests.delete(self.url + method, params=params)
            if response.status_code == 200:
                unsubscribe = response.json()
            else:
                logger.error("Error unsubscribe: {}".format(response.status_code))
                unsubscribe = None
        except Exception as e:
            logger.error("Error connect unsubscribe: %s.", e)
            unsubscribe = None
        return unsubscribe

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

    def get_bot_info(self):
        """
        Возвращает информацию о текущем боте. Текущий бот может быть идентифицирован по токену доступа. Метод
        возвращает идентификатор бота, имя и аватар (если есть).
        Returns info about current bot. Current bot can be identified by access token.
        Method returns bot identifier, name and avatar (if any).
        https://dev.tamtam.chat/#operation/getMyInfo
        API = me
        :return: bot_info: возвращает информацию о боте.
        """
        method = 'me'
        params = {
            "access_token": self.token,
        }
        try:
            response = requests.get(self.url + method, params=params)
            if response.status_code == 200:
                bot_info = response.json()
            else:
                logger.error("Error get bot info: {}".format(response.status_code))
                bot_info = None
        except Exception as e:
            logger.error("Error connect get bot info: %s.", e)
            bot_info = None
        return bot_info

    def bot_user_id(self):
        """
        Возвращает айди текущего бота.
        :return:
        """
        bot = self.get_bot_info()
        bot_user_id = bot['user_id']
        return bot_user_id

    def bot_name(self):
        """
        Возвращает имя текущего бота
        :return:
        """
        bot = self.get_bot_info()
        name = bot['name']
        return name

    def bot_username(self):
        """
        Возвращает username текущего бота.
        :return:
        """
        bot = self.get_bot_info()
        username = bot['username']
        return username

    def bot_avatar_url(self):
        """
        Возвращает ссылку на аватар текущего бота.
        :return:
        """
        bot = self.get_bot_info()
        if 'avatar_url' in bot:
            avatar_url = bot['avatar_url']
            return avatar_url

    def bot_full_avatar_url(self):
        """
        Возвращает ссылку на аватар большого размера текущего бота.
        :return:
        """
        bot = self.get_bot_info()
        if 'full_avatar_url' in bot:
            full_avatar_url = bot['full_avatar_url']
            return full_avatar_url

    def bot_commands(self):
        """
        Возвращает список команд текущего бота.
        :return:
        """
        bot = self.get_bot_info()
        if 'commands' in bot:
            commands = bot['commands']
            return commands

    def bot_description(self):
        """
        Возвращает описание текущего бота.
        :return:
        """
        bot = self.get_bot_info()
        if 'description' in bot:
            description = bot['description']
            return description

    def edit_bot_info(self, name, username, description, commands, photo=None, photo_url=None):
        """
        Редактирует текущую информацию о боте. Заполните только те поля, которые вы хотите обновить. Все остальные
        поля останутся нетронутыми.
        Edits current bot info. Fill only the fields you want to update. All remaining
        fields will stay untouched
        https://dev.tamtam.chat/#operation/editMyInfo
        API = me
        :param name: имя бота
        :param username: уникальное имя (@my_bot) бота без знака "@"
        :param description: описание бота
        :param commands: = [{"name": '/команда_1', "description": "Описание команды 1"},
                            {"name": '/команда_2', "description": "Описание команды 2"}]
        :param photo: файл с изображением бота
        :param photo_url: ссылка на изображение бота
        :return edit_bot_info: возвращает результат PATCH запроса.
        """
        method = 'me'
        params = {
            "access_token": self.token
        }
        if photo is not None:
            photo = self.token_upload_content('image', photo)
        else:
            photo = {}
        photo_res = {
            "url": photo_url
        }
        photo_res.update(photo)
        data = {
            "name": name,
            "username": username,
            "description": description,
            "commands": commands,
            "photo": photo_res
        }
        try:
            response = requests.patch(self.url + method, params=params, data=json.dumps(data))
            if response.status_code == 200:
                edit_bot_info = response.json()
            else:
                logger.error("Error edit bot info: {}".format(response.status_code))
                edit_bot_info = None
        except Exception as e:
            logger.error("Error connect edit bot info: %s.", e)
            edit_bot_info = None
        return edit_bot_info

    def get_chat(self, chat_id):
        """
        https://dev.tamtam.chat/#operation/getChat
        Метод получения информации о чате (какой информации?).
        Returns info about chat.
        API = chats/{chatId}
        :param chat_id: идентификатор чата о котором получаем информацию
        :return: возвращает информацию о чате в формате JSON или None при неудаче
        """
        method = 'chats/{}'.format(chat_id)
        params = {
            "access_token": self.token
        }
        try:
            response = requests.get(self.url + method, params)
            if response.status_code == 200:
                chat = response.json()
            else:
                logger.error("Error get chat info: {}".format(response.status_code))
                chat = None
        except Exception as e:
            logger.error("Error connect get chat info: %s.", e)
            chat = None
        return chat

    def get_chat_type(self, update):
        """
        https://dev.tamtam.chat/#operation/getUpdates
        API = subscriptions/Get updates/[updates][0][message][recipient][chat_type]
        Получает тип чата, канала, или диалога (Enum:"dialog" "chat" "channel")
        :param update: результат работы метода get_updates
        :return: возвращает значение поля chat_type.
        """
        chat_type = None
        if update != None:
            if 'updates' in update.keys():
                upd = update['updates'][0]
            else:
                upd = update
            update_type = self.get_update_type(update)
            if update_type == 'message_created':
                upd1 = upd.get('message').get('recipient')
                if 'chat_type' in upd1.keys():
                    chat_type = upd1['chat_type']
                else:
                    chat_type = None
        return chat_type

    def get_all_chats(self, count=50, marker=None):
        """
        Возвращает информацию о чатах, в которых участвовал бот: список результатов и маркер указывают на следующую страницу
        Returns information about chats that bot participated in: a result list and marker points to the next page
        https://dev.tamtam.chat/#operation/getChats
        API = chats
        :param count: количествово анализируемых чатов (максмум 100).
        :param marker: указывает на следующую страницу данных, null для первой страницы
        :return: chats: возвращает результат GET запроса.
        """
        method = 'chats'
        params = {
            "access_token": self.token,
            "count": count,
            "marker": marker
        }
        try:
            response = requests.get(self.url + method, params=params)
            if response.status_code == 200:
                chats = response.json()
            else:
                logger.error("Error get all chats: {}".format(response.status_code))
                chats = None
        except Exception as e:
            logger.error("Error connect get all chats: %s.", e)
            chats = None
        return chats

    def get_chat_admins(self, chat_id):
        """
        Возвращает пользователей, участвовавших в чате.
        Returns users participated in chat.
        https://dev.tamtam.chat/#operation/getAdmins
        API = chats/{chatId}/members
        :param chat_id: идентификатор чата
        :return chat_admins: возвращает список администраторов чата
        """
        method = 'chats/{}'.format(chat_id) + '/members/admins'
        params = {
            "access_token": self.token
        }
        try:
            response = requests.get(self.url + method, params=params)
            if response.status_code == 200:
                chat_admins = response.json()
            else:
                logger.error("Error chat admins: {}".format(response.status_code))
                chat_admins = None
        except Exception as e:
            logger.error("Error connect chat admins: %s.", e)
            chat_admins = None
        return chat_admins

    def get_chat_membership(self, chat_id):
        """
        Возвращает информацию о членстве в чате для текущего бота
        Returns chat membership info for current bot.
        https://dev.tamtam.chat/#operation/getMembership
        API = chats/{chatId}/members/me
        :param chat_id: идентификатор чата
        :return chat_membership: возвращает информацию о членстве бота в чате
        """
        method = 'chats/{}'.format(chat_id) + '/members/me'
        params = {
            "access_token": self.token
        }
        try:
            response = requests.get(self.url + method, params=params)
            if response.status_code == 200:
                chat_membership = response.json()
            else:
                logger.error("Error chat membership: {}".format(response.status_code))
                chat_membership = None
        except Exception as e:
            logger.error("Error connect chat membership: %s.", e)
            chat_membership = None
        return chat_membership

    def leave_chat(self, chat_id):
        """
        Удаление бота из участников чата.
        Removes bot from chat members.
        https://dev.tamtam.chat/#operation/leaveChat
        API = chats/{chatId}/members/me
        :param chat_id: идентификатор изменяемого чата
        :return: возвращает результат DELETE запроса
        """
        method = 'chats/{}'.format(chat_id) + '/members/me'
        params = {
            "access_token": self.token
        }
        try:
            response = requests.delete(self.url + method, params=params)
            if response.status_code == 200:
                leave_chat = response.json()
            else:
                logger.error("Error leave chat: {}".format(response.status_code))
                leave_chat = None
        except Exception as e:
            logger.error("Error connect leave chat: %s.", e)
            leave_chat = None
        return leave_chat

    def edit_chat_info(self, chat_id, icon=None, title=None, icon_url=None):
        """
        https://dev.tamtam.chat/#operation/editChat
        Редактирование информации чата: заголовок и значок, бот должен иметь соответствующие разрешения
        Edits chat info: title, icon
        API = chats/{chatId}
        :param chat_id: идентификатор изменяемого чата
        :param icon: файл значка
        :param icon_url: ссылка на изображение (имеет приоритет перед файлом значка)
        :param title: заголовок
        :return: возвращает информацию о параметрах измененного чата
        """
        method = 'chats/{}'.format(chat_id)
        params = {
            "access_token": self.token
        }
        if icon != None:
            icon = self.token_upload_content('image', icon)
        else:
            icon = {}
        icon_res = {"url": icon_url}
        icon_res.update(icon)
        data = {
            "icon": icon_res,
            "title": title
        }
        try:
            response = requests.patch(self.url + method, params=params, data=json.dumps(data))
            if response.status_code == 200:
                chat_info = response.json()
            else:
                logger.error("Error edit chat info: {}".format(response.status_code))
                chat_info = None
        except Exception as e:
            logger.error("Error connect edit chat info: %s.", e)
            chat_info = None
        return chat_info

    def get_members(self, chat_id, user_ids, marker=None, count=20):
        """
        Возвращает пользователей, участвовавших в чате. Returns users participated in chat.
        https://dev.tamtam.chat/#operation/getMembers
        API = chats/{chatId}/members
        :param chat_id: идентификатор чата
        :param user_ids: разделенный запятыми список идентификаторов пользователей для получения их членства, при
        передаче этого параметра счетчик и маркер игнорируются
        :param marker: маркер события
        :param count: количество (счетчик) пользователей о которых получаем информацию (максимум 100)
        :return: возвращает информацию о пользователях чата (канала)
        """
        method = 'chats/{}'.format(chat_id) + '/members'
        params = {
            "access_token": self.token,
            'user_ids': [
                user_ids
            ],
            'marker': marker,
            'count': count
        }
        try:
            response = requests.get(self.url + method, params=params)
            if response.status_code == 200:
                members = response.json()
            else:
                logger.error("Error get members: {}".format(response.status_code))
                members = None
        except Exception as e:
            logger.error("Error connect get members: %s.", e)
            members = None
        return members

    def add_members(self, chat_id, user_ids):
        """
        Добавляет пользователя в чат. Могут потребоваться дополнительные разрешения.
        Adds members to chat. Additional permissions may require.
        https://dev.tamtam.chat/#operation/addMembers
        API = chats/{chatId}/members
        :param chat_id: идентификатор чата
        :param user_ids: массив идентификаторов пользователей
        :return: add_members: возвращает результат POST запроса
        """
        method = 'chats/{}'.format(chat_id) + '/members'
        params = {
            "access_token": self.token
        }
        data = {
            "user_ids": [
                user_ids
            ]
        }
        try:
            response = requests.post(self.url + method, params=params, data=json.dumps(data))
            if response.status_code == 200:
                add_members = response.json()
            else:
                logger.error("Error add members: {}".format(response.status_code))
                add_members = None
        except Exception as e:
            logger.error("Error connect add members: %s.", e)
            add_members = None
        return add_members

    def remove_member(self, chat_id, user_id):
        """
        Удаляет участника из чата. Могут потребоваться дополнительные разрешения.
        Removes member from chat. Additional permissions may require.
        https://dev.tamtam.chat/#operation/removeMember
        API = chats/{chatId}/members
        :param chat_id: идентификатор чата
        :param user_id: идентификатор пользователя
        :return remove_member: возвращает результат DELETE запроса
        """
        method = 'chats/{}'.format(chat_id) + '/members'
        params = (
            ('access_token', self.token),
            ('user_id', user_id),
        )
        try:
            response = requests.delete(self.url + method, params=params)
            if response.status_code == 200:
                remove_member = response.json()
            else:
                logger.error("Error remove member: {}".format(response.status_code))
                remove_member = None
        except Exception as e:
            logger.error("Error connect remove member: %s.", e)
            remove_member = None
        return remove_member

    def ban_member(self, chat_id, user_id, block=True):
        """
        Блокирует и удаляет участника из чата. Могут потребоваться дополнительные разрешения.
        Blocks and removes member from chat. Additional permissions may require.
        https://dev.tamtam.chat/#operation/removeMember
        API = chats/{chatId}/members
        :param chat_id: идентификатор чата
        :param user_id: идентификатор пользователя
        :param block: при true блокирует пользователя в чате.
        Применимо только для публичных чатов, или же чатов, имеющих личную ссылку. Иначе игнорируется.
        :return ban_member: возвращает результат DELETE запроса
        """
        method = 'chats/{}'.format(chat_id) + '/members'
        params = (
            ('access_token', self.token),
            ('user_id', user_id),
            ('block', block),
        )
        try:
            response = requests.delete(self.url + method, params=params)
            if response.status_code == 200:
                ban_member = response.json()
            else:
                logger.error("Error ban member: {}".format(response.status_code))
                ban_member = None
        except Exception as e:
            logger.error("Error connect ban member: %s.", e)
            ban_member = None
        return ban_member

    def get_update_type(self, update):
        """
        Метод получения типа события произошедшего с ботом
        API = subscriptions/Get updates/[updates][0][update_type]
        :param update = результат работы метода get_update
        :return: возвращает значение поля 'update_type', при неудаче = None
        """
        upd_type = None
        if update != None:
            if 'updates' in update.keys():
                upd = update['updates'][0]
            else:
                upd = update
            upd_type = upd.get('update_type')
        return upd_type

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
            if 'updates' in update.keys():
                upd = update['updates'][0]
            else:
                upd = update
            type = self.get_update_type(update)
            if type == 'message_created' or type == 'message_edited':
                upd = upd.get('message')
                text = upd.get('body').get('text')
                if 'link' in upd.keys():
                    if upd.get('link').get('type') == 'forward':
                        try:
                            text = upd.get('link').get('message').get('text')
                        except Exception as e:
                            logger.error("Error: %s.", e)
                            text = None
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
            if 'updates' in update.keys():
                upd = update['updates'][0]
            else:
                upd = update
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

    def get_chat_id(self, update=None):
        """
        Получения идентификатора чата, в котором произошло событие
        API = subscriptions/Get updates/[updates][0][chat_id]
           или = subscriptions/Get updates/[updates][0][message][recipient][chat_id]
        :param update = результат работы метода get_update, если update=None, то chat_id получается из последнего активного диалога
        :return: возвращает, если это возможно, значение поля 'chat_id' не зависимо от события, произошедшего с ботом
                 если событие - "удаление сообщения", то chat_id = None
        """
        chat_id = None
        if update == None:
            method = 'chats'
            params = {
                "access_token": self.token
            }
            try:
                response = requests.get(self.url + method, params=params)
                if response.status_code == 200:
                    update = response.json()
                    if 'chats' in update.keys():
                        update = update['chats'][0]
                        chat_id = update.get('chat_id')
                else:
                    logger.error("Error get chat_id: {}".format(response.status_code))
            except Exception as e:
                logger.error("Error connect get chat id: %s.", e)
                chat_id = None
        else:
            if 'updates' in update.keys():
                upd = update['updates'][0]
            else:
                upd = update
            if 'message_id' in upd.keys():
                chat_id = None
            elif 'chat_id' in upd.keys():
                chat_id = upd.get('chat_id')
            elif 'message' in upd.keys():
                upd = upd.get('message')
                if 'recipient' in upd.keys():
                    chat_id = upd.get('recipient').get('chat_id')
        return chat_id

    def get_link_chat_id(self, update):
        """
        Получение идентификатора чата пересланного сообщения
        API = subscriptions/Get updates/[updates][0][message][link][chat_id]
        :param update = результат работы метода get_update
        :return: возвращает, если это возможно, значение поля 'chat_id' пересланного боту сообщения (от кого)
        """
        chat_id = None
        if update != None:
            if 'updates' in update.keys():
                upd = update['updates'][0]
            else:
                upd = update
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
            if 'updates' in update.keys():
                upd = update['updates'][0]
            else:
                upd = update
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
            if 'updates' in update.keys():
                upd = update['updates'][0]
            else:
                upd = update
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
            if 'updates' in update.keys():
                upd = update['updates'][0]
            else:
                upd = update
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
            if 'updates' in update.keys():
                upd = update['updates'][0]
            else:
                upd = update
            if 'message' in upd.keys():
                upd = upd['message']
                if 'link' in upd.keys():
                    upd = upd['link']
                    if 'sender' in upd.keys():
                        name = upd['sender']['name']
        return name

    def get_payload(self, update):
        """
        Метод получения значения нажатой кнопки, заданного в send_buttons
        API = subscriptions/Get updates/[updates][0][callback][payload]
        :param update: результат работы метода get_update
        :return: возвращает результат нажатия кнопки или None
        """
        payload = None
        if update != None:
            if 'updates' in update.keys():
                upd = update['updates'][0]
            else:
                upd = update
            type = self.get_update_type(update)
            if type == 'message_callback':
                upd = upd.get('callback')
                if 'payload' in upd.keys():
                    payload = upd.get('payload')
        return payload

    def get_callback_id(self, update):
        """
        Метод получения значения callback_id при нажатии кнопки
        API = subscriptions/Get updates/[updates][0][callback][callback_id]
        :param update: результат работы метода get_update
        :return: возвращает callback_id нажатой кнопки или None
        """
        callback_id = None
        type = self.get_update_type(update)
        if update != None:
            if 'updates' in update.keys():
                upd = update['updates'][0]
            else:
                upd = update
            if type == 'message_callback':
                upd = upd.get('callback')
                if 'callback_id' in upd.keys():
                    callback_id = upd.get('callback_id')
        return callback_id

    def get_message_id(self, update):
        """
        Получение message_id отправленного или пересланного боту
        API = subscriptions/Get updates/[updates][0][message][link][message][mid] (type = 'forward')
           или = subscriptions/Get updates/[updates][0][message][body][mid]
        :param update = результат работы метода get_update
        :return: возвращает, если это возможно, значение поля 'mid'
        """
        mid = None
        if update != None:
            if 'updates' in update.keys():
                upd = update['updates'][0]
                type = self.get_update_type(update)
                if type == 'message_created' or type == 'message_callback':
                    mid = upd.get('message').get('body').get('mid')
            else:
                upd = update
                if 'message' in upd.keys():
                    mid = upd.get('message').get('body').get('mid')
        return mid

    def edit_message(self, message_id, text, attachments=None, link=None, notify=True):
        """
        https://dev.tamtam.chat/#operation/editMessage
        Метод  изменения (обновления) любого контента по его идентификатору
        :param message_id: Идентификатор редактируемого контента
        :param attachments: Новый массив объектов (файл, фото, видео, аудио, кнопки)
        :param text: Обновленное текстовое сообщение
        :param link: Обновленное пересылаемые (цитируемые) сообщение
        :param notify: Уведомление о событии, если значение false, участники чата не будут уведомлены
        :return update: Возвращает результат PUT запроса
        """
        method = 'messages'
        params = (
            ('access_token', self.token),
            ('message_id', message_id),
        )
        data = {
            "text": text,
            "attachments": attachments,
            "link": link,
            "notify": notify
        }
        flag = 'attachment.not.ready'
        while flag == 'attachment.not.ready':
            response = requests.put(self.url + method, params=params, data=json.dumps(data))
            upd = response.json()
            if 'code' in upd.keys():
                flag = upd.get('code')
                logger.info('ждем 5 сек...')
                time.sleep(5)
            else:
                flag = None
        # response = requests.put(self.url + method, params=params, data=json.dumps(data))
        if response.status_code == 200:
            update = response.json()
        else:
            logger.error("Error edit message: {}".format(response.status_code))
            update = None
        return update

    def send_typing_on(self, chat_id):
        """
        Отправка уведомления от бота в чат - 'печатает...'
        https://dev.tamtam.chat/#operation/sendAction
        :param chat_id: чат куда необходимо отправить уведомление
        :return:
        """
        method_ntf = 'chats/{}'.format(chat_id) + '/actions?access_token='
        params = {"action": "typing_on"}
        requests.post(self.url + method_ntf + self.token, data=json.dumps(params))

    def send_mark_seen(self, chat_id):
        """
        Отправка в чат маркера о прочтении ботом сообщения
        https://dev.tamtam.chat/#operation/sendAction
        :param chat_id: чат куда необходимо отправить уведомление
        :return:
        """
        method_ntf = 'chats/{}'.format(chat_id) + '/actions?access_token='
        params = {"action": "mark_seen"}
        requests.post(self.url + method_ntf + self.token, data=json.dumps(params))

    def send_sending_video(self, chat_id):
        """
        Отправка уведомления от бота в чат - 'отправка видео...'
        https://dev.tamtam.chat/#operation/sendAction
        :param chat_id: чат куда необходимо отправить уведомление
        :return:
        """
        method_ntf = 'chats/{}'.format(chat_id) + '/actions?access_token='
        params = {"action": "sending_video"}
        requests.post(self.url + method_ntf + self.token, data=json.dumps(params))

    def send_sending_audio(self, chat_id):
        """
        Отправка уведомления от бота в чат - 'отправка аудио...'
        https://dev.tamtam.chat/#operation/sendAction
        :param chat_id: чат куда необходимо отправить уведомление
        :return:
        """
        method_ntf = 'chats/{}'.format(chat_id) + '/actions?access_token='
        params = {"action": "sending_audio"}
        requests.post(self.url + method_ntf + self.token, data=json.dumps(params))

    def send_sending_photo(self, chat_id):
        """
        Отправка уведомления от бота в чат - 'отправка фото ...'
        https://dev.tamtam.chat/#operation/sendAction
        :param chat_id: чат куда необходимо отправить уведомление
        :return:
        """
        method_ntf = 'chats/{}'.format(chat_id) + '/actions?access_token='
        params = {"action": "sending_photo"}
        requests.post(self.url + method_ntf + self.token, data=json.dumps(params))

    def send_sending_image(self, chat_id):
        """
        Отправка уведомления от бота в чат - 'отправка фото ...'
        https://dev.tamtam.chat/#operation/sendAction
        :param chat_id: чат куда необходимо отправить уведомление
        :return:
        """
        method_ntf = 'chats/{}'.format(chat_id) + '/actions?access_token='
        params = {"action": "sending_image"}
        requests.post(self.url + method_ntf + self.token, data=json.dumps(params))

    def send_sending_file(self, chat_id):
        """
        Отправка уведомления от бота в чат - 'отправка файла...' #не работает, но ошибку не вызывает
        https://dev.tamtam.chat/#operation/sendAction
        :param chat_id: чат куда необходимо отправить уведомление
        :return:
        """
        method_ntf = 'chats/{}'.format(chat_id) + '/actions?access_token='
        params = {"action": "sending_file"}
        requests.post(self.url + method_ntf + self.token, data=json.dumps(params))

    def delete_message(self, message_id):
        """
        Delete message to specific chat_id by post request
        Удаляет сообщение в соответствии с message_id
        API = messages/Delete message/{message_id}
        :param message_id: идентификатор сообщения
        """
        method = 'messages'
        params = {
            "message_id": message_id,
            "access_token": self.token
        }
        response = requests.delete(self.url + method, params=params)
        if response.status_code != 200:
            logger.error("Error delete message: {}".format(response.status_code))

    def attach_buttons(self, buttons):
        """
        Метод подготовки к отправке кнопок в качестве элемента attachments
        :param buttons: кнопки в формате списка, cформированные при помощи:
            button_callback, button_contact, button_link, button_location и т.д.
        :return attach: подготовленный контент
        """
        attach = None
        if isinstance(buttons, list):
            try:
                if buttons[0][0]:
                    attach = [{"type": "inline_keyboard",
                               "payload": {"buttons": buttons}
                               }
                              ]
            except:
                attach = [{"type": "inline_keyboard",
                           "payload": {"buttons": [buttons]}
                           }
                          ]
        else:
            attach = [{"type": "inline_keyboard",
                       "payload": {"buttons": [[buttons]]}
                       }
                      ]
        return attach

    def button_callback(self, text, payload, intent='default'):
        """
        Подготавливает кнопку с реакцией callback
        :param text: подпись кнопки
        :param payload: значение кнопки при нажатии
        :param intent: цвет кнопки
        :return: возвращает подготовленную кнопку для последующего формирования массива
        """
        button = {"type": 'callback',
                  "text": text,
                  "payload": payload,
                  "intent": intent}
        return button

    def button_link(self, text, url):
        """
        Подготавливает кнопку с реакцией link
        :param text: подпись кнопки
        :param url: ссылка для перехода при нажатии
        :return: возвращает подготовленную кнопку для последующего формирования массива
        """
        button = {"type": 'link',
                   "text": text,
                   "url": url}
        return button

    def button_contact(self, text):
        """
        Подготавливает кнопку с запросом контакта
        :param text: подпись кнопки
        :return: возвращает подготовленную кнопку для последующего формирования массива
        """
        button = {"type": 'request_contact',
                   "text": text}
        return button

    def button_location(self, text, quick=False):
        """
        Подготавливает кнопку с запросом местоположения
        :param text: подпись кнопки
        :param quick: если true, отправляет местоположение без запроса подтверждения пользователя
        :return: возвращает подготовленную кнопку для последующего формирования массива
        """
        button = {"type": 'request_geo_location',
                   "text": text,
                   "quick": quick}
        return button

    def send_buttons(self, text, buttons, chat_id):
        """
        Send buttons to specific chat_id by post request
        Отправляет кнопки (количество, рядность и функционал определяются параметром buttons) в соответствующий чат
        :param text: Текст выводимый над блоком кнопок
        :param chat_id: integer, chat id of user / чат где будут созданы кнопки
        :param buttons: массив кнопок, сформированный методами button_callback, button_contact, button_link и т.п.
        :return update: результат POST запроса на отправку кнопок
        """
        self.send_typing_on(chat_id)
        attach = self.attach_buttons(buttons)
        update = self.send_message(text, chat_id, attachments=attach)
        return update

    def upload_url(self, type):
        """
        https://dev.tamtam.chat/#operation/getUploadUrl
        Вспомогательная функция получения URL для загрузки контента в ТамТам
        :param type: тип контента ('audio', 'video', 'file', 'photo')
        :return: URL на который будет отправляться контент
        """
        method = 'uploads'
        params = (
            ('access_token', self.token),
            ('type', type),
        )
        response = requests.post(self.url + method, params=params)
        if response.status_code == 200:
            update = response.json()
            url = update.get('url')
        else:
            url = None
        return url

    def attach_file(self, content, content_name=None):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Метод подготовки файла (файлы загружаются только по одному) совместно с кнопками
        :param content: имя файла или полный путь доступный боту на машине где он запущен, например '/mnt/files/movie.mp4'
        :param content_name: имя с которым будет загружен файл
        :return: attach: подготовленный контент
        """
        token = self.token_upload_content('file', content, content_name)
        attach = [{"type": "file", "payload": token}]
        return attach

    def send_file(self, content, chat_id, text=None, content_name=None):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Метод отправки файла в указанный чат (файлы загружаются только по одному)
        :param content: имя файла или полный путь доступный боту на машине где он запущен, например 'movie.mp4'
        :param chat_id: чат куда будет загружен файл
        :param text: сопровождающий текст к отправляемому файлу
        :param content_name: имя с которым будет загружен файл
        :return: update: результат работы POST запроса отправки файла
        """
        self.send_sending_file(chat_id)
        attach = self.attach_file(content, content_name)
        update = self.send_message(text, chat_id, attachments=attach)
        return update

    def attach_image(self, content):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Метод подготовки изображений (нескольких изображений) в указанный чат
        :param content: имя файла или список имен файлов с изображениями
        :return: attach: подготовленный контент
        """
        attach = []
        if isinstance(content, str):
            token = self.token_upload_content('image', content)
            attach.append({"type": "image", "payload": token})
        else:
            for cont in content:
                token = self.token_upload_content('image', cont)
                attach.append({"type": "image", "payload": token})
        return attach

    def send_image(self, content, chat_id, text=None):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Метод отправки фoто (нескольких фото) в указанный чат
        :param content: имя файла или список имен файлов с изображениями
        :param chat_id: чат куда будут загружены изображения
        :param text: Сопровождающий текст к отправляемому контенту
        :return: update: результат работы POST запроса отправки файла
        """
        self.send_sending_photo(chat_id)
        attach = self.attach_image(content)
        update = self.send_message(text, chat_id, attachments=attach)
        return update

    def attach_image_url(self, url):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Метод подготовки изображений (нескольких изображений) к отправке по их url
        :param url: http адрес или список адресов с изображениями
        :return: attach: подготовленный контент
        """
        attach = []
        if isinstance(url, str):
            attach.append({"type": "image", "payload": {'url': url}})
        else:
            for cont in url:
                attach.append({"type": "image", "payload": {'url': cont}})
        return attach

    def send_image_url(self, url, chat_id, text=None):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Метод отправки фото (нескольких фото) в указанный чат по url
        :param url: http адрес или список адресов с изображениями
        :param chat_id: чат куда будут загружены изображения
        :param text: сопровождающий текст к отправляемому контенту
        :return: update: результат работы POST запроса отправки фото
        """
        self.send_sending_photo(chat_id)
        attach = self.attach_image_url(url)
        update = self.send_message(text, chat_id, attachments=attach)
        return update

    def attach_video(self, content):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Метод подготовки к отправке видео (нескольких видео)
        :param content: имя файла или полный путь доступный боту на машине где он запущен, например 'movie.mp4'
                        иди список файлов ['movie.mp4', 'movie2.mkv']
        :return: attach: подготовленный контент
        """
        attach = []
        if isinstance(content, str):
            token = self.token_upload_content('video', content)
            attach.append({"type": "video", "payload": token})
        else:
            for cont in content:
                token = self.token_upload_content('video', cont)
                attach.append({"type": "video", "payload": token})
        return attach

    def send_video(self, content, chat_id, text=None):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Метод отправки видео (нескольких видео) в указанный чат
        :param content: имя файла или полный путь доступный боту на машине где он запущен, например 'movie.mp4'
                        иди список файлов ['movie.mp4', 'movie2.mkv']
        :param chat_id: чат куда будут загружены видео
        :param text: Сопровождающий текст к отправляемому(мым) видео
        :return: update: результат работы POST запроса отправки видео
        """
        self.send_sending_video(chat_id)
        attach = self.attach_video(content)
        update = self.send_message(text, chat_id, attachments=attach)
        return update

    def attach_audio(self, content):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Метод подготовки аудио (только по одному) к отправке
        :param content: имя файла или полный путь доступный боту на машине где он запущен (например 'audio.mp3'),
                        файлы защищенные авторскими правами не загружаются
        :return: attach: подготовленный контент
        """
        token = self.token_upload_content('audio', content)
        attach = [{"type": "audio", "payload": token}]
        return attach

    def send_audio(self, content, chat_id, text=None):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Метод отправки аудио (только по одному) в указанный чат
        :param content: имя файла или полный путь доступный боту на машине где он запущен (например 'audio.mp3'),
                        файлы защищенные авторскими правами не загружаются
        :param chat_id: чат куда будет загружено аудио
        :param text: сопровождающий текст к отправляемому аудио
        :return: update: результат работы POST запроса отправки аудио
        """
        self.send_sending_audio(chat_id)
        attach = self.attach_audio(content)
        update = self.send_message(text, chat_id, attachments=attach)
        return update

    def send_forward_message(self, text, mid, chat_id):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Send forward message specific chat_id by post request
        Пересылает сообщение в указанный чат
        :param text: текст к пересылаемому сообщению или None
        :param mid: message_id пересылаемого сообщения
        :param chat_id: integer, chat id of user / чат куда отправится сообщение
        :return update: response | ответ на POST message в соответствии с API
        """
        self.send_typing_on(chat_id)
        link = self.link_forward(mid)
        update = self.send_message(text, chat_id, link=link)
        return update

    def link_reply(self, mid):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Формирует параметр link на цитируемуе сообщение для отправки через send_message
        :param mid: идентификатор сообщения (get_message_id) на которое готовим link
        :return link: сформированный параметр link
        """
        link = {"type": "reply",
                "mid": mid
                }
        return link

    def link_forward(self, mid):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Формирует параметр link на пересылаемое сообщение для отправки через send_message
        :param mid: идентификатор сообщения (get_message_id) на которое готовим link
        :return link: сформированный параметр link
        """
        link = {"type": "forward",
                "mid": mid
                }
        return link

    def send_reply_message(self, text, mid, chat_id):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Send reply message specific chat_id by post request
        Формирует ответ на сообщение в указанный чат
        :param text: текст ответа на сообщение (обязательный параметр)
        :param mid: message_id сообщения на которое формируется ответ
        :param chat_id: integer, chat id of user / чат куда отправится сообщение
        :return update: response | ответ на POST запрос в соответствии с API
        """
        self.send_typing_on(chat_id)
        link = self.link_reply(mid)
        update = self.send_message(text, chat_id, link=link)
        return update

    def token_upload_content(self, type, content, content_name=None):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Вспомогательная функция получения Tokena для загрузки контента в ТамТам
        :param type: тип контента ('audio', 'video', 'file', 'photo')
        :param content: имя файла или полный путь доступный боту на машине где он запущен (например 'movie.mp4')
        :param content_name: Имя с которым будет загружен файл
        :return: update: результат работы POST запроса отправки файла
        """
        url = self.upload_url(type)
        response = 400
        if content_name is None:
            content_name = os.path.basename(content)
        try:
            content = open(content, 'rb')
        except Exception:
            logger.error("Error upload file (no such file)")
        response = requests.post(url, files={
            'files': (content_name, content, 'multipart/form-data')})
        if response.status_code == 200:
            token = response.json()
        else:
            logger.error("Error sending message")
            token = None
        return token

    def send_message(self, text, chat_id, user_id=None, attachments=None, link=None, notify=True, dislinkprev=False):
        """
        https://dev.tamtam.chat/#operation/sendMessage
        Метод отправки любого контента, сформированного в соответсвии с документацией, в указанный чат
        :param attachments: Массив объектов (файл, фото, видео, аудио, кнопки и т.д.)
        :param chat_id: Чат куда отправляется контент
        :param user_id: Идентификатор пользователя, которому отправляем сообщение
        :param text: Текстовое описание контента
        :param link: Пересылаемые (цитируемые) сообщения
        :param notify: Уведомление о событии, если значение false, участники чата не будут уведомлены
        :param dislinkprev: Параметр определяет генерировать предпросмотр для ссылки или нет
        :return update: Возвращает результат POST запроса
        """
        self.send_typing_on(chat_id)
        method = 'messages'
        params = (
            ('access_token', self.token),
            ('chat_id', chat_id),
            ('user_id', user_id),
            ('disable_link_preview', dislinkprev)
        )
        data = {
            "text": text,
            "attachments": attachments,
            "link": link,
            "notify": notify
        }
        flag = 'attachment.not.ready'
        while flag == 'attachment.not.ready':
            response = requests.post(self.url + method, params=params, data=json.dumps(data))
            upd = response.json()
            if 'code' in upd.keys():
                flag = upd.get('code')
                logger.info('ждем 5 сек...')
                time.sleep(5)
            else:
                flag = None
        if response.status_code == 200:
            update = response.json()
        else:
            logger.error("Error sending message: {}".format(response.status_code))
            update = None
        return update

    def send_answer_callback(self, callback_id, notification, text=None, attachments=None, link=None, notify=None):
        """
        https://dev.tamtam.chat/#operation/answerOnCallback
        Метод отправки ответа после того, как пользователь нажал кнопку. Ответом может
        быть обновленное сообщение или/и кратковременное всплывающее уведомление пользователя.
        :param callback_id: параметр, соответствующий нажатой кнопке
        :param notification: кратковременное, всплывающее уведомление
        :param text: обновленное (новое) текстовое сообщение
        :param attachments: измененный (новый) контент (изображения, видео, кнопки и т.д.)
        :param link: цитируемое сообщение
        :param notify: если false, то участники чата не получат уведомление (по умолчанию true)
        :return update: результат POST запроса
        """
        method = 'answers'
        params = (
            ('access_token', self.token),
            ('callback_id', callback_id),
        )
        message = {"text": text,
                   "attachments": attachments,
                   "link": link,
                   "notify": notify
                   }
        data = {
            "message": message,
            "notification": notification
        }
        flag = 'attachment.not.ready'
        while flag == 'attachment.not.ready':
            response = requests.post(self.url + method, params=params, data=json.dumps(data))
            upd = response.json()
            if 'code' in upd.keys():
                flag = upd.get('code')
                logger.info('ждем 5 сек...')
                time.sleep(5)
            else:
                flag = None
        if response.status_code == 200:
            update = response.json()
        else:
            logger.error("Error answer callback: {}".format(response.status_code))
            update = None
        return update
