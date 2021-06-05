# botapitamtam   
*(новая версия, часть синтаксиса изменена, старая версия: [botapitamtam v.0.1.10.1](https://github.com/registriren/botapitamtam/releases/tag/ver_0.1.10.1))*  


Попытка создать набор простых инструментов для написания ботов на базе API мессенджера TamTam. Набор содержит базовый функционал взаимодействия бота с пользователями и предназначен для начинающих программистов. Синтаксис методов позволяет легко их модифицировать или создавать на их базе новые методы используя официальную документацию https://dev.tamtam.chat/ .

Примеры реализации ботов с использованем библиотеки:   

<https://github.com/registriren/filelink>

<https://github.com/registriren/yatranslate>
  

Библиотека находится в стадии разработки, поэтому возможны изменения синтаксиса, которые приведут к неработоспособности вашего кода, проверяйте перед применением изменений на своей системе.

Чат для обсуждения вопросов, связанных с работой библиотеки <https://tt.me/botapitamtam>

Принцип взаимодействия с библиотекой:
- 
1. Методы, которые начинаются с `get_` получают события, произошедшие с ботом (написанные или пересланные сообщения, результат нажатия кнопок, вложения и т.д.).
2. Методы, которые начинаются с `send_` формируют события в боте (отправляют сообщения, генерируют кнопки и т.д.).
3. Методы не имеющие указанные "префиксы" позволяют удалять, изменять сообщения, либо являются вспомогательными.
4. В основном цикле Вашей программы осуществляем запрос происходящих с ботом событий методом `get_updates`. Результат помещаем в переменную, например `upd = get_updates()`.
5. Результат работы сформированных вами событий так же можно поместить в переменную, например `res = send_message(text, chat_id)`. Чаще всего из результата сформированного события требуется получить параметр `message_id` с помощью которого в дальнейшем можно изменять (удалять) данное событие (сообщение, контент).  
6. Для получения "тела" события, которое необходимо обработать, передаем переменную `upd` выбранному методу `get_` , например `get_text(upd)`, работаем с результатом. Если запрошенное событие не произошло в ответ получим `None`.  
7. Предлагаемая конструкция кода:  
```python
from botapitamtam import BotHandler

bot = BotHandler('access_token_primebot')

def main():
    while True:
        upd = bot.get_updates()  # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # тут можно вставить любые действия которые должны выполняться во время ожидания события
        if upd: # основной код, для примера представлен эхо-бот
            chat_id = bot.get_chat_id(upd)
            text = bot.get_text(upd)
            bot.send_message(text, chat_id)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
```
8. Для работы с библиотекой поместите файл [botapitamtam.py](botapitamtam.py) в каталог с вашим кодом. Для удобного использования библиотеки во многих ботах с возможностью получения обновлений необходимо клонировать репозиторий в отдельный каталог
(`git clone https://github.com/registriren/botapitamtam`), а символьную ссылку на файл [botapitamtam.py](botapitamtam.py) разместить в каталогах с вашими ботами.
9. Отправка простого однотипного контента (текст и фото, текст и видео, текст и кнопки) в чат осуществляется с помощью методов `send_image, send_video, send_buttons`.
10. Формирование кнопок осуществляется в несколько этапов:
  - Готовим кнопки в зависимости от типа (`callback, link, request_contact, request_geo_location, chat`) с помощью соответствующих методов `button_callback, button_link, button_contact и т.п.` результат работы методов присваем переменной, например `key1 = button_callback('Кнопка1', 'payload-key1')`
  - Если необходимо объединить кнопки в строку `key_str = [[key1, key2, key3]]`
  - Если необходимо объединить кнопки в столбец `key_stb = [[key4], [key5]]`
  - Можно сочетать вышеуказанные правила или просто сложить подготавливаемые кнопки `key_res = key_str + key_stb`
  - Теперь можно отправить кнопки в бот методом `send_buttons(text, key_res, chat_id)` или сделать их частью `attachments` для совместной отправки с другим контентом (фото, видео и т.п.) при помощи соответствующих методов (`send_message, send_answer_callback, edit_message и др.`), содержащих в качестве параметра `attachments=`
  - Примеры в разделе [Examples](examples)
## Описание методов (также смотрите в основном коде):
### Получение информации о событиях в чате с ботом
- **[get_updates](#get_updatesmarkernone-limit100-timeout30) - получение событий, произошедших в чате с ботом (боту отправлено текстовое сообщение, картинка, видео, нажата кнопка и т.д.) С результатом работы, помещенным в переменную (например *update*) этого метода, работают нижеперечисленные методы:**  
  - [get_marker](#get_markerupdate) - получает маркер (порядковый номер) следующего события, необходим в технических целях.
  - [get_chat_id](#get_chat_idupdatenone) - получает идентификатор чата в которм происходит взаимодействие с ботом, только этот идентификатор требуется в следующих методах:
    - [get_chat](#get_chatchat_id) - получает информацию о текущем чате.
    - [get_chat_admins](#get_chat_adminschat_id) - получает информацию об администраторах чата.
    - [get_chat_membership](#get_chat_membershipchat_id) - получает информацию о членстве в чате для текущего бота.
  - [get_user_id](#get_user_idupdate) - получает идентификатор пользователя полученного сообщения.
  - [get_callback_id](#get_callback_idupdate) - получает значение callback_id (идентификатора клавиатуры), предназначенного для создания реакции на факт нажатия кнопки с помощью метода [send_answer_callback](#send_answer_callbackcallback_id-notification-textnone-attachmentsnone-linknone-notifynone).
  - [get_payload](#get_payloadupdate) - получает payload (текстовое значение, не путать с наименованием кнопки) нажатой кнопки.
  - [get_text](#get_textupdate) - получает значение поля text полученного сообщения (события).
  - [get_message_id](#get_message_idupdate) - получает идентификатор сообщения (события).
  - [get_name](#get_nameupdate) - получает имя пользователя, сформировавшего событие.
  - [get_username](#get_usernameupdate) - получает username пользователя, сформировавшего событие.  
  - [get_is_bot](#get_is_botupdate) - позволяет отличить пользователя от бота.  
  - [get_update_type](#get_update_typeupdate) - получает тип события (например bot_started), произошедшего с ботом.
  - [get_attachments](#get_attachmentsupdate) - получает весь прикрепленный к сообщению контент в различном сочетании (например несколько фото, видео).  
  - [get_url](#get_urlupdate) - получает значение поля URL полученного сообщения (события). 
  - [get_link_name](#get_link_nameupdate) - получает имя пользователя пересланного сообщения.  
  - [get_link_username](#get_link_usernameupdate) - получает username пользователя пересланного сообщения.  
  - [get_link_user_id](#get_link_user_idupdate) - получает идентификатор пользователя пересланного сообщения.
  - [get_link_chat_id](#get_link_chat_idupdate) - получает идентификатор чата пересланного сообщения.
  - [get_chat_type](#get_chat_typeupdate) - получает значение поля chat_type (диалог, чат, канал).
  - [get_attach_type](#get_attach_typeupdate) - получает тип вложения (file, contact, share и т.п.) к сообщению отправленному или пересланному боту  
- [get_members](#get_memberschat_id-user_ids-markernone-count20) - получает информацию о пользователях участвующих в чате.
- [get_all_chats](#get_all_chatscount50-markernone) - получает информацию о чатах, в которых участвовал бот.
- [get_bot_info](#get_bot_info) - получает информацию о текущем боте.
    - [get_bot_user_id](#get_bot_user_id) - возвращает идентификатор текущего бота.
    - [get_bot_name](#get_bot_name) - возращает имя текущего бота.
    - [get_bot_username](#get_bot_username) - возвращает username текущего бота.
    - [get_bot_avatar_url](#get_bot_avatar_url) - возвращает ссылку на аватар текущего бота.
    - [get_bot_full_avatar_url](#get_bot_full_avatar_url) - возвращает ссылку на аватар большого размера текущего бота.
    - [get_bot_commands](#get_bot_commands) - возвращает список команд текущего бота.
    - [get_bot_description](#get_bot_description) - возвращает описание текущего бота.
- [get_subscriptions](#get_subscriptions) - возвращает список подписок на WebHook.
- [add_members](#add_memberschat_id-user_ids) - добавляет пользователя в чат.
### Подготовка контента (фото, видео, файл, кнопки) к совместной отправке в чат через параметр `attachments=`
- [attach_audio](#attach_audiocontent) - готовит аудио к совместной отправке с другим контентом.
- [attach_file](#attach_filecontent-content_namenone) - готовит файл к совместной отправке с другим контентом.
- [attach_image](#attach_imagecontent) - готовит изображения к совместной отправке с другим контентом.
- [attach_image_url](#attach_image_urlurl) - готовит изображения (по их URL) к совместной отправке с другим контентом.
- [attach_video](#attach_videocontent) - готовит видео к совместной отправке с другим контентом.
- [attach_buttons](#attach_buttonsbuttons) - готовит массив кнопок к совместной отправке с другим контентом, при этом сами кнопки предварительно формируются следующими методами:
  - [button_callback](#button_callbacktext-payload-intentdefault) - готовит кнопку с реакцией callback для дальнейшего формирования в массив.
  - [button_contact](#button_contacttext) - готовит кнопку запроса контакта пользователя для дальнейшего формирования в массив.
  - [button_link](#button_linktext-url) - готовит кнопку со ссылкой на URL для дальнейшего формирования в массив.
  - [button_location](#button_locationtext-quickfalse) - готовит кнопку запроса местоположения для дальнейшего формирования в массив.  
  - [button_chat](#button_chattext-chat_title-chat_descriptionnone-start_payloadnone-uuidnone) - готовит кнопку для создания нового чата, например чата для обсуждения.    
### Формирование (отправка, изменение) событий в чатах с ботом
- [delete_message](#delete_messagemessage_id) - удаляет сообщение (контент) по его идентификатору (message_id).
- [edit_message](#edit_messagemessage_id-text-attachmentsnone-linknone-notifytrue) - изменяет контент по его идентификатору и сформированному аттач.
- [pin_message](#pin_messagechat_id-message_id-notifytrue) - закрепляет сообщение в верху чата. 
- [unpin_message](#unpin_messagechat_id) - открепляет сообщение в чате.  
- [get_pinned_message](#get_pinned_messagechat_id) - получает закрепленное сообщение в чате.  
- [send_answer_callback](#send_answer_callbackcallback_id-notification-textnone-attachmentsnone-linknone-notifynone) - отправляет уведомление (реакцию) после нажатия кнопки.
- [send_audio](#send_audiocontent-chat_id-textnone-formatnone) - отправляет аудиофайл с преобразованием в формат ТамТам.
- [send_buttons](#send_buttonstext-buttons-chat_id-formatnone) - отправляет текст с кнопками в чат.
- [send_file](#send_filecontent-chat_id-textnone-content_namenone-formatnone) - отправляет файл.
- [send_message](#send_messagetext-chat_id-user_idnone-attachmentsnone-linknone-notifytrue-dislinkprevfalse) - отправляет текстовое сообщение и любой контент по сформированному attachments.
  - [link_forward](#link_forwardmid) - формирует параметр `link` пересылаемого сообщения для отправки через `send_message`.
  - [link_reply](#link_replymid) - формирует параметр `link` цитируемого сообщения для отправки через `send_message`.
- [send_image](#send_imagecontent-chat_id-textnone-formatnone) - отправляет изображение (несколько изображений) из локального файла.  
- [send_image_url](#send_image_urlurl-chat_id-textnone-formatnone) - отправляет изображение из URL.  
- [send_video](#send_videocontent-chat_id-textnone-formatnone) - отправляет видео.  
- [send_forward_message](#send_forward_messagetext-mid-chat_id-formatnone) - пересылает сообщение по его идентификатору.  
- [send_reply_message](#send_reply_messagetext-mid-chat_id-formatnone) - формирует ответ на сообщение.  
### Методы работы с режимом конструктора
- [get_session_id](#get_session_idupdate) - получает значение session_id в режиме конструктора.  
- [get_start_payload](#get_start_payloadupdate) - получает данные для использования в чате, созданном ботом в режиме конструктора.  
- [send_construct_message](#send_construct_messagesession_id-hint-textnone-attachmentsnone-markupnone-formatnone-allow_user_inputtrue-datanone-buttonsnone-placeholdernone) - отправляет результат работы конструктора (сообщение, контент) в чат.    
- [markup](#markuptype-from_posit-length) - подготавливает формат для фрагмента текста обрабатываемого методом [send_construct_message](#send_construct_messagesession_id-hint-textnone-attachmentsnone-markupnone-formatnone-allow_user_inputtrue-datanone-buttonsnone-placeholdernone)
### Методы обслуживания ботов и чатов
- [edit_bot_info](#edit_bot_infoname-username-descriptionnone-commandsnone-photonone-photo_urlnone) - редактирует информацию о текущем боте.
- [edit_chat_info](#edit_chat_infochat_id-iconnone-icon_urlnone-titlenone-pinnone-notifytrue) - редактирует информацию о чате.
- [leave_chat](#leave_chatchat_id) - удаляет бота из текущего чата.
- [remove_member](#remove_memberchat_id-user_id) - удаляет пользователя из чата.
### Вспомогательные методы
- [mark_seen](#mark_seenchat_id) - отправляет уведомление о прочтении ботом сообщения.
- [sending_audio](#sending_audiochat_id) - отправляет уведомление об отправке аудио.
- [sending_file](#sending_filechat_id) - отправляет уведомление об отправке файла.
- [sending_photo](#sending_photochat_id) - отправляет уведомление об отправке изображения.
- [sending_image](#sending_imagechat_id) - отправляет уведомление об отправке изображения.
- [sending_video](#sending_videochat_id) - отправляет уведомление об отправке видео.
- [typing_on](#typing_onchat_id) - отправляет уведомление о печати сообщения.
- [token_upload_content](#token_upload_contenttype-content-content_namenone) - вспомогательная функция получения токена загружаемого изображения.
- [upload_url](#upload_urltype) - вспомогательная функция получения URL загружаемого изображения.
### Технические методы
- [subscribe](#subscribeurl-update_types-version) - подписывается на получение обновлений через WebHook.
- [unsubscribe](#unsubscribeurl) - отписывается от получения обновлений через WebHook.


## Подробное описание методов  
### get_updates(marker=None, limit=100, timeout=30): 
https://dev.tamtam.chat/#operation/getUpdates  
Основная функция опроса состояния (событий) бота методом long polling  
This method is used to get updates from bot via get request. It is based on long polling.  
**:param marker:** условный (очередной) номер события, которое необходимо получить, если параметр пуст, то получаем текущее событие.  
**:param limit:** количество событий, возвращаемых за один раз.  
**:param timeout:** время в течение которого держится соединение с сервером ТамТам в ожидании событий.  
**:return:** возвращает набор значений, соответствующих событию в боте в формате JSON, если событие не произошло, то через определенный интервал времени возвращается None.  
  
  
### get_subscriptions():  
https://dev.tamtam.chat/#operation/getSubscriptions  
Если ваш бот получает данные через WebHook, метод возвращает список всех подписок.  
In case your bot gets data via WebHook, the method returns list of all subscriptions  
**:return:** возвращает список подписок.


### subscribe(url, update_types, version):  
https://dev.tamtam.chat/#operation/subscribe  
Подписывает бот для получения обновлений через WebHook. После вызова этого метода бот будет получать
уведомления о новых событиях в чатах по указанному URL.  
Subscribes bot to receive updates via WebHook. After calling this method, the bot will receive notifications
about new events in chat rooms at the specified URL.  
**:param url:** URL HTTP(S) - точки входа вашего бота, должен начинаться с http(s)://  
**:param update_types:** список типов обновлений, которые хочет получить ваш бот [в разработке..]  
**:param version:** версия API  
**:return:** возвращает статус POST запроса  


### unsubscribe(url):    
https://dev.tamtam.chat/#operation/unsubscribe  
Отменяет подписку бота на получение обновлений через WebHook. После вызова метода бот перестает получать
уведомления о новых событиях. Уведомление через API длинного опроса становится доступным для бота  
Unsubscribes bot from receiving updates via WebHook. After calling the method, the bot stops receiving
notifications about new events. Notification via the long-poll API becomes available for the bot  
**:param url:** URL для удаления из подписок WebHook  
**:return:** возвращает результат DELETE запроса  


### get_marker(update):  
Метод получения маркера события  
**:param update:** результат работы метода [get_updates](README.md#get_updatesmarkernone-limit100-timeout30)   
**:return:** возвращает значение поля 'marker', при неудаче = None  

       
### get_bot_info():
https://dev.tamtam.chat/#operation/getMyInfo  
Возвращает информацию о текущем боте. Текущий бот может быть идентифицирован по токену доступа.  
Метод возвращает идентификатор бота, имя и аватар (если есть).  
Returns info about current bot. Current bot can be identified by access token.  
Method returns bot identifier, name and avatar (if any).  
**:return:** bot_info: возвращает информацию о боте.  

### get_bot_user_id():
Возвращает идентификатор текущего бота.  
Returns the ID of the current bot.  

### get_bot_name():
Возвращает имя текущего бота.  
Returns the name of the current bot.  

### get_bot_username():
Возвращает username текущего бота.  
Returns username of the current bot.  

### get_bot_avatar_url():
Возвращает ссылку на аватар текущего бота.  
Returns a link to the avatar of the current bot.  

### get_bot_full_avatar_url():
Возвращает ссылку на аватар большого размера текущего бота.  
Returns a link to a large-sized avatar of the current bot.  

### get_bot_commands():
Возвращает список команд текущего бота.  
Returns the list of commands of the current bot.  

### get_bot_description():
Возвращает описание текущего бота.  
Returns a description of the current bot.  
       
### edit_bot_info(name, username, description=None, commands=None, photo=None, photo_url=None):
https://dev.tamtam.chat/#operation/editMyInfo  
Редактирует текущую информацию о боте. Заполните только те поля, которые вы хотите обновить. Все остальные поля останутся нетронутыми.  
Edits current bot info. Fill only the fields you want to update. All remaining fields will stay untouched  
**:param name:** имя бота  
**:param username:** уникальное имя (@my_bot) бота без знака "@"  
**:param description:** описание бота  
**:param commands: =** 
```
[{"name": '/команда_1', "description": "Описание команды 1"},  
 {"name": '/команда_2', "description": "Описание команды 2"}]  
```
или используем вспомогательный метод `command(name, description)`  
**:param photo:** файл с изображением бота  
**:param photo_url:** ссылка на изображение бота  
**:return edit_bot_info:** возвращает результат PATCH запроса.  
подробнее в [Examples](examples/edit_bot_info.py)  


### get_chat(chat_id):
https://dev.tamtam.chat/#operation/getChat  
Метод получения информации о чате (какой информации?).    
Returns info about chat.  
**:param chat_id:** идентификатор чата о котором получаем информацию  
**:return:** возвращает информацию о чате в формате JSON или None при неудаче  

### get_chat_type(update):
https://dev.tamtam.chat/#operation/getUpdates  
Получает тип чата, канала, или диалога (Enum:"dialog" "chat" "channel")  
**:param update:** результат работы метода get_updates  
**:return:** возвращает значение поля chat_type.  
        
### get_all_chats(count=50, marker=None):
https://dev.tamtam.chat/#operation/getChats  
Возвращает информацию о чатах, в которых участвовал бот: список результатов и маркер указывают на следующую страницу    
Returns information about chats that bot participated in: a result list and marker points to the next page  
**:param count:** количествово анализируемых чатов (максмум 100)  
**:param marker:** указывает на следующую страницу данных, null для первой страницы  
**:return chats:** возвращает результат GET запроса  
        
### get_chat_admins(chat_id):
https://dev.tamtam.chat/#operation/getAdmins  
Возвращает сведения об администраторах чата и их правах.  
Returns users participated in chat.  
**:param chat_id:** идентификатор чата  
**:return chat_admins:** возвращает список администраторов чата  
        
### get_chat_membership(chat_id):
https://dev.tamtam.chat/#operation/getMembership        
Возвращает информацию о членстве в чате для текущего бота  
Returns chat membership info for current bot  
**:param chat_id:** идентификатор чата
**:return chat_membership:** возвращает информацию о членстве бота в чате
        
### leave_chat(chat_id):
https://dev.tamtam.chat/#operation/leaveChat  
Удаление бота из участников чата.  
Removes bot from chat members.  
**:param chat_id:** идентификатор изменяемого чата
**:return:** возвращает результат DELETE запроса


### edit_chat_info(chat_id, icon=None, icon_url=None, title=None, pin=None, notify=True):
https://dev.tamtam.chat/#operation/editChat  
Редактирование информации чата: заголовок и значок  
Edits chat info: title, icon, pin  
**:param chat_id:** идентификатор изменяемого чата    
**:param icon:** файл значка    
**:param icon_url:** ссылка на изображение  
**:param title:** заголовок    
**:param pin:** указать message_id закрепляемого сообщения  
**:param notify:** уведомление участников об изменениях в информации чата  
**:return:** возвращает информацию о параметрах измененного чата  
       
### get_members(chat_id, user_ids, marker=None, count=20):
https://dev.tamtam.chat/#operation/getMembers  
Возвращает пользователей, участвовавших в чате.  
Returns users participated in chat.  
**:param chat_id:** идентификатор чата  
**:param user_ids:** разделенный запятыми список идентификаторов пользователей для получения их членства, при передаче этого параметра счетчик и маркер игнорируются  
**:param marker:** маркер события  
**:param count:** количество (счетчик) пользователей о которых получаем информацию (максимум 100)  
**:return:** возвращает информацию о пользователях чата (канала)  
     
### add_members(chat_id, user_ids):
https://dev.tamtam.chat/#operation/addMembers  
Добавляет пользователя в чат. Могут потребоваться дополнительные разрешения.  
Adds members to chat. Additional permissions may require.  
**:param chat_id:** идентификатор чата  
**:param user_ids:** массив идентификаторов пользователей  
**:return add_members:** возвращает результат POST запроса  

### remove_member(chat_id, user_id):
https://dev.tamtam.chat/#operation/removeMember  
Удаляет участника из чата. Могут потребоваться дополнительные разрешения.  
Removes member from chat. Additional permissions may require.  
**:param chat_id:** идентификатор чата  
**:param user_id:** идентификатор пользователя  
**:return remove_member:** возвращает результат DELETE запроса  
       
### get_update_type(update):
https://botapi.tamtam.chat/updates  
Метод получения типа события произошедшего с ботом  
**:param update:** результат работы метода get_update  
**:return:** возвращает значение поля 'update_type' (bot_started, message_created, user_added) при неудаче = None    
      
### get_text(update):
https://botapi.tamtam.chat/updates  
Получение текста отправленного или пересланного боту  
**:param update:** результат работы метода get_update  
**:return:** возвращает, если это возможно, значение поля 'text' созданного или пересланного сообщения из 'body' или 'link'-'forward' соответственно, при неудаче 'text' = None    

### get_attachments(update):
https://botapi.tamtam.chat/updates  
Получение всех вложений (file, contact, share и т.п.) к сообщению отправленному или пересланному боту  
**:param update:** результат работы метода get_updates  
**:return attachments:** возвращает, если это возможно, значение поля 'attachments' созданного или пересланного контента, при неудаче 'attachments' = None 
               
### get_url(update):
https://botapi.tamtam.chat/updates  
Получение ссылки отправленного или пересланного боту файла  
**:param update:** результат работы метода get_update  
**:return:** возвращает, если это возможно, значение поля 'url' созданного или пересланного файла из 'body' или 'link' соответственно, при неудаче 'url' = None    

### get_chat_id(update=None):
https://botapi.tamtam.chat/updates  
Получения идентификатора чата, в котором произошло событие  
**:param update:** результат работы метода get_update, если update=None, то chat_id получается из последнего активного диалога  
**:return:** возвращает, если это возможно, значение поля 'chat_id' не зависимо от события, произошедшего с ботом если событие - "удаление сообщения", то chat_id = None  

### get_link_chat_id(update):
https://botapi.tamtam.chat/updates  
Получение идентификатора чата пересланного сообщения  
**:param update:** результат работы метода get_update    
**:return:** возвращает, если это возможно, значение поля 'chat_id' пересланного боту сообщения (от кого)  

### get_user_id(update):
https://botapi.tamtam.chat/updates  
Получения идентификатора пользователя, инициировавшего событие  
**:param update:** результат работы метода get_update  
**:return:** возвращает, если это возможно, значение поля 'user_id' не зависимо от события, произошедшего с ботом если событие - "удаление сообщения", то user_id = None  

### get_link_user_id(update):
https://botapi.tamtam.chat/updates  
Получения идентификатора пользователя пересланного сообщения  
**:param update:** результат работы метода get_update  
**:return:** возвращает, если это возможно, значение поля 'user_id' пересланного боту сообщения (от кого)  

### get_name(update):
https://botapi.tamtam.chat/updates  
Получение имени пользователя, инициировавшего событие  
**:param update:** результат работы метода get_update  
**:return:** возвращает, если это возможно, значение поля 'name' не зависимо от события, произошедшего с ботом если событие - "удаление сообщения", то name = None  

### get_username(update):
https://botapi.tamtam.chat/updates    
Получение username пользователя (если оно есть), инициировавшего событие, в том числе нажатие кнопки    
**:param update:** результат работы метода get_update  
**:return:** возвращает, если это возможно, значение поля 'username'

### get_is_bot(update):  
https://botapi.tamtam.chat/updates      
Проверка на принадлежность к боту участника, инициировавшего событие, в том числе нажатие кнопки    
**:param update:** результат работы метода get_update   
**:return:** возвращает, если это возможно, значение поля 'is_bot' (True, False) или None при неудаче    

### get_link_name(update):
https://botapi.tamtam.chat/updates  
Получение имени пользователя пересланного сообщения  
**:param update:** результат работы метода get_update  
**:return:** возвращает, если это возможно, значение поля 'name' пересланного боту сообщения (от кого)  

### get_link_username(update):
https://botapi.tamtam.chat/updates  
Получение username пользователя пересланного сообщения  
**:param update:** результат работы метода get_update  
**:return:** возвращает, если это возможно, значение поля 'username' пересланного боту сообщения (от кого)  

### get_payload(update):
https://botapi.tamtam.chat/updates  
Метод получения значения нажатой кнопки, заданного в send_buttons  
**:param update:** результат работы метода get_update  
**:return:** возвращает результат нажатия кнопки или None  

### get_callback_id(update):
https://botapi.tamtam.chat/updates  
Метод получения значения callback_id при нажатии кнопки  
**:param update:** результат работы метода get_update  
**:return:** возвращает callback_id нажатой кнопки или None  

### get_message_id(update):
https://botapi.tamtam.chat/updates  
Получение message_id отправленного или пересланного боту  
**:param update:**результат работы метода get_update  
**:return:** возвращает, если это возможно, значение поля 'mid'  

### edit_message(message_id, text, attachments=None, link=None, notify=True):
https://dev.tamtam.chat/#operation/editMessage  
Метод  изменения (обновления) любого контента по его идентификатору  
**:param message_id:** Идентификатор редактируемого контента  
**:param attachments:** Новый массив объектов (файл, фото, видео, аудио, кнопки)  
**:param text:** Обновленное текстовое сообщение  
**:param link:** Обновленное пересылаемые (цитируемые) сообщение  
**:param notify:** Уведомление о событии, если значение false, участники чата не будут уведомлены  
**:param format:** значение "markdown" или "html", текст будет отформатирован соответственно  
**:return update:** Возвращает результат PUT запроса  

### pin_message(chat_id, message_id, notify=True):  
https://dev.tamtam.chat/#operation/pinMessage  
Метод закрепления сообщений в чате  
**:param chat_id:** Идентификатор чата  
**:param message_id:** Идентификатор сообщения, которое будет закреплено  
**:param notify:** Уведомление о событии, если значение false, участники чата не будут уведомлены  
**:return update:** Возвращает результат PUT запроса    

### unpin_message(chat_id):  
https://dev.tamtam.chat/#operation/unpinMessage  
Метод открепления сообщения в чате  
**:param chat_id:** Идентификатор чата  

### get_pinned_message(chat_id):  
https://dev.tamtam.chat/#operation/getPinnedMessage  
Метод получения закрепленного собщения в чате  
**:param chat_id:** Идентификатор чата  
**:return message:** Возвращает закрепленное сообщение, с ним можно работать привычными методами, например get_text(message)  

### typing_on(chat_id):
https://dev.tamtam.chat/#operation/sendAction  
Отправка уведомления от бота в чат - 'печатает...'  
**:param chat_id:** чат куда необходимо отправить уведомление  
**:return:**

### mark_seen(chat_id):
https://dev.tamtam.chat/#operation/sendAction  
Отправка в чат маркера о прочтении ботом сообщения  
**:param chat_id:** чат куда необходимо отправить уведомление  
**:return:**

### sending_video(chat_id):
https://dev.tamtam.chat/#operation/sendAction   
Отправка уведомления от бота в чат - 'отправка видео...'  
**:param chat_id:** чат куда необходимо отправить уведомление  
**:return:**

### sending_audio(chat_id):
https://dev.tamtam.chat/#operation/sendAction  
Отправка уведомления от бота в чат - 'отправка аудио...'  
**:param chat_id:** чат куда необходимо отправить уведомление  
**:return:**

### sending_photo(chat_id):
https://dev.tamtam.chat/#operation/sendAction  
Отправка уведомления от бота в чат - 'отправка фото ...'  
**:param chat_id:** чат куда необходимо отправить уведомление  
**:return:**

### sending_image(chat_id):
https://dev.tamtam.chat/#operation/sendAction  
Отправка уведомления от бота в чат - 'отправка фото ...'  
**:param chat_id:** чат куда необходимо отправить уведомление  
**:return:**

### sending_file(chat_id):
https://dev.tamtam.chat/#operation/sendAction  
Отправка уведомления от бота в чат - 'отправка файла...'    
**:param chat_id:** чат куда необходимо отправить уведомление      
**:return:**

### delete_message(message_id):
Удаляет сообщение в соответствии с message_id  
Delete message to specific chat_id by post request  
**:param message_id:** идентификатор сообщения  

### attach_buttons(buttons):
Метод подготовки к отправке кнопок в качестве элемента attachments    
**:param buttons:** кнопки в формате списка, cформированные при помощи методов button_callback, button_contact, button_link, button_location и т.д.    
**:return attach:** подготовленный контент  

### button_callback(text, payload, intent='default'):
Подготавливает кнопку с реакцией callback  
**:param text:** подпись кнопки    
**:param payload:** значение кнопки при нажатии  
**:param intent:** цвет кнопки    
**:return:** возвращает подготовленную кнопку для последующего формирования массива  

### button_link(text, url):
Подготавливает кнопку с реакцией link  
**:param text:** подпись кнопки  
**:param url:** ссылка для перехода при нажатии    
**:return:** возвращает подготовленную кнопку для последующего формирования массива    

### button_contact(text):
Подготавливает кнопку с запросом контакта  
**:param text:** подпись кнопки  
**:return:** возвращает подготовленную кнопку для последующего формирования массива  

### button_location(text, quick=False):
Подготавливает кнопку с запросом местоположения  
**:param text:** подпись кнопки    
**:param quick:** если true, отправляет местоположение без запроса подтверждения пользователя    
**:return:** возвращает подготовленную кнопку для последующего формирования массива  

### button_chat(text, chat_title, chat_description=None, start_payload=None, uuid=None):  
Подготавливает кнопку, создающую новый чат (например, чат для комментариев)  
**:param text:** подпись кнопки  
**:param chat_title:** название создаваемого чата  
**:param chat_description:** описание чата  
**:param start_payload:** начальная полезная нагрузка будет отправлена боту сразу же после создания чата  
**:param uuid:** Уникальный идентификатор кнопки для всех кнопок чата на клавиатуре. Если uuid изменен, то новый чат будет создан при следующем щелчке мыши. Сервер сгенерирует его в тот момент, когда кнопка будет изначально размещена. Повторно используйте его при редактировании сообщения.    
**:return:** возвращает подготовленную кнопку для последующего формирования массива    

### send_buttons(text, buttons, chat_id, format=None):
Send buttons to specific chat_id by post request  
Отправляет кнопки (количество, рядность и функционал определяются параметром buttons) в соответствующий чат  
**:param text:** Текст выводимый над блоком кнопок  
**:param chat_id:** integer, chat id of user / чат где будут созданы кнопки  
**:param buttons:** массив кнопок, сформированный методами button_callback, button_contact, button_link и т.п.   
**:param format:** значение "markdown" или "html", текст будет отформатирован соответственно  
**:return update:** результат POST запроса на отправку кнопок  

### upload_url(type):
https://dev.tamtam.chat/#operation/getUploadUrl  
Вспомогательная функция получения URL для загрузки контента в ТамТам  
**:param type:** тип контента ('audio', 'video', 'file', 'photo')  
**:return:** URL на который будет отправляться контент  

### attach_file(content, content_name=None):
https://dev.tamtam.chat/#operation/sendMessage  
Метод подготовки файла (файлы загружаются только по одному) совместно с кнопками  
**:param content:** имя файла или полный путь доступный боту на машине где он запущен, например '/mnt/files/movie.mp4'  
**:param content_name:** имя с которым будет загружен файл  
**:return attach:** подготовленный контент  

### send_file(content, chat_id, text=None, content_name=None, format=None):
https://dev.tamtam.chat/#operation/sendMessage  
Метод отправки файла в указанный чат (файлы загружаются только по одному)  
**:param content:** имя файла или полный путь доступный боту на машине где он запущен, например 'movie.mp4'  
**:param chat_id:** чат куда будет загружен файл  
**:param text:** сопровождающий текст к отправляемому файлу  
**:param content_name:** имя с которым будет загружен файл  
**:param format:** значение "markdown" или "html", текст будет отформатирован соответственно  
**:return update:** результат работы POST запроса отправки файла  

### attach_image(content):
https://dev.tamtam.chat/#operation/sendMessage  
Метод подготовки изображений (нескольких изображений) в указанный чат  
**:param content:** имя файла или список имен файлов с изображениями  
**:return attach:** подготовленный контент  

### send_image(content, chat_id, text=None, format=None):
https://dev.tamtam.chat/#operation/sendMessage  
Метод отправки фoто (нескольких фото) в указанный чат  
**:param content:** имя файла или список имен файлов с изображениями  
**:param chat_id:** чат куда будут загружены изображения  
**:param text:** сопровождающий текст к отправляемому контенту  
**:param format:** значение "markdown" или "html", текст будет отформатирован соответственно  
**:return update:** результат работы POST запроса отправки файла  

### attach_image_url(url):
https://dev.tamtam.chat/#operation/sendMessage  
Метод подготовки изображений (нескольких изображений) к отправке по их url  
**:param url:** http адрес или список адресов с изображениями  
**:return attach:** подготовленный контент  

### send_image_url(url, chat_id, text=None, format=None):
https://dev.tamtam.chat/#operation/sendMessage  
Метод отправки фото (нескольких фото) в указанный чат по url  
**:param url:** http адрес или список адресов с изображениями  
**:param chat_id:** чат куда будут загружены изображения  
**:param text:** сопровождающий текст к отправляемому контенту  
**:param format:** значение "markdown" или "html", текст будет отформатирован соответственно  
**:return update:** результат работы POST запроса отправки фото  

### attach_video(content):
https://dev.tamtam.chat/#operation/sendMessage  
Метод подготовки к отправке видео (нескольких видео)  
**:param content:** имя файла или полный путь доступный боту на машине где он запущен, например 'movie.mp4'
или список файлов ['movie.mp4', 'movie2.mkv']  
**:return attach:** подготовленный контент  

### send_video(content, chat_id, text=None, format=None):
https://dev.tamtam.chat/#operation/sendMessage  
Метод отправки видео (нескольких видео) в указанный чат  
**:param content:** имя файла или полный путь доступный боту на машине где он запущен, например 'movie.mp4' или список файлов ['movie.mp4', 'movie2.mkv']
**:param chat_id:** чат куда будут загружены видео  
**:param text:** Сопровождающий текст к отправляемому(мым) видео  
**:param format:** значение "markdown" или "html", текст будет отформатирован соответственно  
**:return update:** результат работы POST запроса отправки видео  

### attach_audio(content):
https://dev.tamtam.chat/#operation/sendMessage  
Метод подготовки аудио (только по одному) к отправке  
**:param content:** имя файла или полный путь доступный боту на машине где он запущен (например 'audio.mp3'),
файлы защищенные авторскими правами не загружаются  
**:return attach:** подготовленный контент  

### send_audio(content, chat_id, text=None, format=None):
https://dev.tamtam.chat/#operation/sendMessage  
Метод отправки аудио (только по одному) в указанный чат  
**:param content:** имя файла или полный путь доступный боту на машине где он запущен (например 'audio.mp3'),
файлы защищенные авторскими правами не загружаются  
**:param chat_id:** чат куда будет загружено аудио  
**:param text:** сопровождающий текст к отправляемому аудио  
**:param format:** значение "markdown" или "html", текст будет отформатирован соответственно  
**:return update:** результат работы POST запроса отправки аудио  

### send_forward_message(text, mid, chat_id, format=None):
https://dev.tamtam.chat/#operation/sendMessage  
Send forward message specific chat_id by post request  
Пересылает сообщение в указанный чат  
**:param text:** текст к пересылаемому сообщению или None  
**:param mid:** message_id пересылаемого сообщения  
**:param chat_id:** integer, chat id of user / чат куда отправится сообщение  
**:param format:** значение "markdown" или "html", текст будет отформатирован соответственно  
**:return update:** response | ответ на POST message в соответствии с API  

### link_reply(mid):
https://dev.tamtam.chat/#operation/sendMessage  
Формирует параметр link на цитируемуе сообщение для отправки через send_message  
**:param mid:** идентификатор сообщения (get_message_id) на которое готовим link  
**:return link:** сформированный параметр link  

### link_forward(mid):
https://dev.tamtam.chat/#operation/sendMessage  
Формирует параметр link на пересылаемое сообщение для отправки через send_message  
**:param mid:** идентификатор сообщения (get_message_id) на которое готовим link  
**:return link:** сформированный параметр link  

### send_reply_message(text, mid, chat_id, format=None):
https://dev.tamtam.chat/#operation/sendMessage  
Send reply message specific chat_id by post request  
Формирует ответ на сообщение в указанный чат  
**:param text:** текст ответа на сообщение (обязательный параметр)  
**:param mid:** message_id сообщения на которое формируется ответ  
**:param chat_id:** integer, chat id of user / чат куда отправится сообщение  
**:param format:** значение "markdown" или "html", текст будет отформатирован соответственно  
**:return update:** response | ответ на POST запрос в соответствии с API  

### token_upload_content(type, content, content_name=None):
https://dev.tamtam.chat/#operation/sendMessage  
Вспомогательная функция получения токена для загрузки контента в ТамТам  
**:param type:** тип контента ('audio', 'video', 'file', 'photo')  
**:param content:** имя файла или полный путь доступный боту на машине где он запущен (например 'movie.mp4')  
**:param content_name:** Имя с которым будет загружен файл  
**:return update:** результат работы POST запроса отправки файла  

### send_message(text, chat_id, user_id=None, attachments=None, link=None, notify=True, dislinkprev=False):
https://dev.tamtam.chat/#operation/sendMessage  
Метод отправки любого контента, сформированного в соответсвии с документацией, в указанный чат  
**:param attachments:** Массив объектов (файл, фото, видео, аудио, кнопки и т.д.)  
**:param chat_id:** Чат куда отправляется контент  
**:param user_id:** Идентификатор пользователя, которому отправляем сообщение, если используете этот параметр, то установите chat_id=None в запросе    
**:param text:** Текстовое описание контента  
**:param link:** Пересылаемые (цитируемые) сообщения  
**:param notify:** Уведомление о событии, если значение false, участники чата не будут уведомлены  
**:param dislinkprev:** Параметр определяет генерировать предпросмотр для ссылки или нет  
**:param format:** значение "markdown" или "html", текст будет отформатирован соответственно  
**:return update:** Возвращает результат POST запроса  


### send_answer_callback(callback_id, notification, text=None, attachments=None, link=None, notify=None):
https://dev.tamtam.chat/#operation/answerOnCallback  
Метод отправки ответа после того, как пользователь нажал кнопку. Ответом может быть обновленное сообщение или/и кратковременное всплывающее уведомление пользователя.    
**:param callback_id:** параметр, соответствующий нажатой кнопке  
**:param notification:** кратковременное, всплывающее уведомление  
**:param text:** обновленное (новое) текстовое сообщение  
**:param attachments:** измененный (новый) контент (изображения, видео, кнопки и т.д.)  
**:param link:** цитируемое сообщение  
**:param notify:** если false, то участники чата не получат уведомление (по умолчанию true)  
**:param format:** значение "markdown" или "html", текст будет отформатирован соответственно  
**:return update:** результат POST запроса  

### get_attach_type(update):
https://dev.tamtam.chat/#operation/getUpdates  
Получение типа вложения (file, contact, share и т.п.) к сообщению отправленному или пересланному боту  
**:param update:** результат работы метода get_updates  
**:return att_type:** возвращает, если это возможно, значение поля 'type' созданного или пересланного контента из 'body' или 'link' соответственно, при неудаче 'type' = None  

### get_session_id(update):
https://dev.tamtam.chat/#operation/getUpdates  
Метод получения значения session_id в режиме конструктора.  
**:param update:** результат работы метода get_updates  
**:return:** возвращает session_id для дальнейшей работы с данным сеансом конструктора    

### get_construct_text(update):
https://dev.tamtam.chat/#operation/getUpdates  
(Метод устарел, необходимо использовать [get_text()](#get_textupdate))  
Получение текста набранного пользователем в режиме конструктора.  
**:param update:** результат работы метода get_updates  
**:return:** возвращает, если это возможно, значение поля 'text', сообщения набранного пользователем в режиме конструктора  
        
### get_construct_payload(update):  
https://dev.tamtam.chat/#operation/getUpdates  
(Метод устарел, необходимо использовать [get_payload()](#get_payloadupdate))  
Получение значения кнопки нажатой пользователем в режиме конструктора  
**:param update:** результат работы метода get_updates  
**:return:** возвращает, если это возможно, значение поля 'payload' в режиме конструктора  

### get_construct_attach(update):  
(Метод устарел, необходимо использовать [get_attachments()](#get_attachmentsupdate))  
https://dev.tamtam.chat/#operation/getUpdates  
Получение дополнительного контента (фото, видео и т.п.) к сообщению набранному пользователем в режиме конструктора  
**:param update:** результат работы метода get_updates  
**:return:** возвращает, если это возможно, значение поля 'attachments', сообщения набранного пользователем в режиме конструктора  

### get_construct_attach_type(update):  
(Метод устарел, необходимо использовать [get_attach_type()](#get_attach_typeupdate))  
https://dev.tamtam.chat/#operation/getUpdates  
Получение типа вложения (file, contact, share и т.п.) к сообщению формируемому в боте-конструкторе  
**:param update:** результат работы метода get_updates  
**:return:** возвращает, если это возможно, значение поля 'type' первого контента переданного боту в режиме коструктора  

### get_start_payload(update):  
https://dev.tamtam.chat/#operation/getUpdates  
Получение начальной полезной нагрузки при открытии чата, созданого ботом в режиме конструтора. С помощью данного метода можно передать данные боту, которые он сможет получить после активации чата (тип message_chat_created), созданного в режиме конструктора  
**:param update:** результат работы метода get_updates()  
**:return:** возвращает, если это возможно, значение поля 'start_payload'  

### send_construct_message(session_id, hint, text=None, attachments=None, markup=None, format=None, allow_user_input=True, data=None, buttons=None, placeholder=None):
https://dev.tamtam.chat/#operation/construct  
Метод отправки результата работы конструктора в чат.  
**:param session_id:** параметр, соответствующий вызванному конструктору  
**:param hint:** сообщение пользователю, вызвавшему конструктор  
**:param text:** текстовое сообщение, которое будет отправлено в результате в чат  
**:param attachments:** контент (изображения, видео, кнопки и т.д.), который будет отправлен в результате в чат  
**:param markup:** формат фрагмента текста, создается методом [markup](#markuptype-from_posit-length)   
**:param format:** значение "markdown" или "html", текст будет отформатирован соответственно  
**:param allow_user_input:** если True, у пользователя будет возможность набирать текст, иначе только технические кнопки  
**:param data:** любые данные в технических целях  
**:param buttons:** технические кнопки для произвольных действий  
**:param placeholder:** текст над техническими кнопками  
**:return:** результат POST запроса   

### markup(type, from_posit, length):
https://dev.tamtam.chat/#operation/construct
Подготавливает формат для модификации фрагмента текста
**:param type:** тип формата
**:param from_posit:** позиция в тексте откуда нужно начать форматирование
**:param length:** длина форматируемого фрагмента текста
**:return:** возвращает подготовленный формат для применения в методе [send_construct_message](#send_construct_messagesession_id-hint-textnone-attachmentsnone-markupnone-formatnone-allow_user_inputtrue-datanone-buttonsnone-placeholdernone)
