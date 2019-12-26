# botapitamtam
Попытка создать набор простых инструментов для написания ботов на базе API мессенджера TamTam. Набор содержит базовый функционал взаимодействия бота с пользователями и предназначен для начинающих программистов. Синтаксис методов позволяет легко их модифицировать или создавать на их базе новые методы используя официальную документацию https://dev.tamtam.chat/ .

Примеры реализации ботов с использованем библиотеки:   

https://github.com/registriren/filelink

https://github.com/registriren/yatranslate
  

Библиотека находится в стадии разработки, поэтому возможны изменения синтаксиса, которые приведут к неработоспособности вашего кода, проверяйте перед применением изменений на своей системе.

Чат для обсуждения вопросов, связанных с работой библиотеки https://tt.me/botapitamtam

Принцип взаимодействия с библиотекой:
- 
1. Методы, которые начинаются с *get_* получают события, произошедшие с ботом (написанные или пересланные сообщения, результат нажатия кнопок, вложения и т.д.).
2. Методы, которые начинаются с *send_* формируют события в боте (отправляют сообщения, генерируют кнопки и т.д.).
3. Методы не имеющие указанные "префиксы" позволяют удалять, изменять сообщения, либо являются вспомогательными.
4. В основном цикле Вашей программы осуществляем запрос происходящих с ботом событий методом [get_updates()](doc/get_updates.md). Результат помещаем в переменную, например [upd = get_updates()](doc/get_updates.md).
5. Результат работы сформированных вами событий так же можно поместить в переменную, например [upd = send_message(text, chat_id)](doc/send_message.md). Чаще всего из результата сформированного события требуется получить параметр *message_id* с помощью которого в дальнейшем можно изменять (удалять) данное событие (сообщение, контент).  
6. Для получения "тела" события, которое необходимо обработать, передаем переменную *upd* выбранному методу *get_* , например [get_text(upd)](doc/get_text.md), работаем с результатом. Если запрошенное событие не произошло в ответ получим *None*.  
7. В зависимости от интенсивности событий и частоты запросов на получение обновлений, [get_updates()](doc/get_updates.md) может возвращать несколько событий списком, в этом случае потребуется добавить еще один цикл для обработки этого списка, пример подобной реализации: https://github.com/registriren/yatranslate или установить параметр *limit=1* в методе [get_updates()](doc/get_updates.md)
8. Для работы с библиотекой поместите файл [botapitamtam.py](botapitamtam.py) в каталог с вашим кодом. Для удобного использования библиотеки во многих ботах с возможностью получения обновлений необходимо клонировать репозиторий в отдельный каталог
(*git clone https://github.com/registriren/botapitamtam*), а символьную ссылку на файл [botapitamtam.py](botapitamtam.py) разместить в каталогах с вашими ботами.
9. Отправка простого однотипного контента (текст и фото, текст и видео, в чат  
## Описание методов (в разработке, смотрите в основном коде):
### Получение информации о событиях в чате с ботом
- **[get_updates](README.md#get_updatesmarkernone-limit100-timeout30) - получение событий, произошедших в чате с ботом (боту отправлено текстовое сообщение, картинка, видео, нажата кнопка и т.д.) С результатом работы, помещенным в переменную (например *update*) этого метода, работают нижеперечисленные методы:**  
  - [get_marker](doc/get_marker.md) - получает маркер (порядковый номер) следующего события, необходим в технических целях.
  - [get_chat_id](doc/get_chat_id.md) - получает идентификатор чата в которм происходит взаимодействие с ботом, только этот идентификатор требуется в следующих методах:
    - [get_chat](doc/get_chat.md) - получает информацию о текущем чате.
    - [get_chat_admins](doc/get_chat_admins.md) - получает информацию об администраторах чата.
    - [get_chat_membership](doc/get_chat_membership.md) - получает информацию о членстве в чате для текущего бота.
  - [get_user_id](doc/get_user_id.md) - получает идентификатор пользователя полученного сообщения.
  - [get_callback_id](doc/get_callback_id.md) - получает значение callback_id (идентификатора клавиатуры), предназначенного для создания реакции на факт нажатия кнопки с помощью метода [send_answer_callback](doc/send_answer_callback).
  - [get_payload](doc/get_payload.md) - получает payload (текстовое значение, не путать с наименованием кнопки) нажатой кнопки.
  - [get_text](doc/get_text.md) - получает значение поля text полученного сообщения (события).
  - [get_message_id](doc/get_message_id.md) - получает идентификатор сообщения (события).
  - [get_name](doc/get_name.md) - получает имя пользователя, сформировавшего событие.
  - [get_update_type](doc/get_update_type.md) - получает тип события (например bot_started), произошедшего с ботом.
  - [get_url](doc/get_url.md) - получает значение поля URL полученного сообщения (события). 
  - [get_link_name](doc/get_link_name.md) - получает имя пользователя пересланного сообщения.
  - [get_link_user_id](doc/get_link_user_id.md) - получает идентификатор пользователя пересланного сообщения.
  - [get_link_chat_id](doc/get_link_chat_id.md) - получает идентификатор чата пересланного сообщения.
  - [get_chat_type](doc/get_chat_type.md) - получает значение поля chat_type (диалог, чат, канал).
- [get_members](doc/get_members.md) - получает информацию о пользователях участвующих в чате.
- [get_all_chats](doc/get_all_chats.md) - получает информацию о чатах, в которых участвовал бот.
- [get_bot_info](doc/get_bot_info.md) - получает информацию о текущем боте.
- [get_subscriptions](doc/get_subscriptions.md) - возвращает список подписок на WebHook.

- [add_members](doc/add_members.md) - добавляет пользователя в чат.
### Подготовка контента (фото, видео, файл, кнопки) к совместной отправке в чат через параметр *attachments=*
- [attach_audio](doc/attach_audio.md) - готовит аудио к совместной отправке с другим контентом.
- [attach_file](doc/attach_file.md) - готовит файл к совместной отправке с другим контентом.
- [attach_image](doc/attach_image.md) - готовит изображения к совместной отправке с другим контентом.
- [attach_image_url](doc/attach_image_url.md) - готовит изображения (по их URL) к совместной отправке с другим контентом.
- [attach_video](doc/attach_video.md) - готовит видео к совместной отправке с другим контентом.
- [attach_buttons](doc/attach_buttons.md) - готовит массив кнопок к совместной отправке с другим контентом, при этом сами кнопки предварительно формируются следующими методами:
  - [button_callback](doc/button_callback.md) - готовит кнопку с реакцией callback для дальнейшего формирования в массив.
  - [button_contact](doc/button_contact.md) - готовит кнопку запроса контакта пользователя для дальнейшего формирования в массив.
  - [button_link](doc/button_link.md) - готовит кнопку со ссылкой на URL для дальнейшего формирования в массив.
  - [button_location](doc/button_location.md) - готовит кнопку запроса местоположения для дальнейшего формирования в массив.
- [delete_message](doc/delete_message.md) - удаляет сообщение (контент) по его идентификатору (message_id).
- [edit_bot_info](doc/edit_bot_info.md) - редактирует информацию о текущем боте.
- [edit_chat_info](doc/edit_chat_info.md) - редактирует информацию о чате.
- [edit_message](doc/edit_message.md) - изменяет контент по его идентификатору и сформированному аттач.
- [leave_chat](doc/leave_chat.md) - удаляет бота из текущего чата.
- [link_forward](doc/link_forward.md) - формирует параметр link пересылаемого сообщения для отправки через send_message.
- [link_reply](doc/link_reply.md) - формирует параметр link цитируемого сообщения для отправки через send_message.
- [remove_member](doc/remove_member.md) - удаляет пользователя из чата.
- [send_answer_callback](doc/send_answer_callback.md) - отправляет уведомление (реакцию) после нажатия кнопки.
- [send_audio](doc/send_audio.md) - отправляет аудиофайл с преобразованием в формат ТамТам.
- [send_buttons](doc/send_buttons.md) - отправляет текст с кнопками в чат.
- [send_file](doc/send_file.md) - отправляет файл.
- [send_forward_message](doc/send_forward_message.md) - пересылает сообщение по его идентификатору.
- [send_mark_seen](doc/send_mark_seen.md) - отправляет уведомление о прочтении ботом сообщения.
- [send_message](doc/send_message.md) - отправляет текстовое сообщение и любой контент по сформированному attachments.
- [send_image](doc/send_image.md) - отправляет изображение (несколько изображений) из локального файла.
- [send_image_url](doc/send_image_url.md) - отправляет изображение из URL.
- [send_reply_message](doc/send_reply_message.md) - формирует ответ на сообщение.
- [send_sending_audio](doc/send_sending_audio.md) - отправляет уведомление об отправке аудио.
- [send_sending_file](doc/send_sending_file.md) - отправляет уведомление об отправке файла.
- [send_sending_photo](doc/send_sending_photo.md) - отправляет уведомление об отправке изображения.
- [send_sending_video](doc/send_sending_video.md) - отправляет уведомление об отправке видео.
- [send_typing_on](doc/send_typing_on.md) - отправляет уведомление о печати сообщения.
- [send_video](doc/send_video.md) - отправляет видео.
- [subscribe](doc/subscribe.md) - подписывается на получение обновлений через WebHook.
- [token_upload_content](doc/token_upload_content.md) - вспомогательная функция получения токена загружаемого изображения.
- [unsubscribe](doc/unsubscribe.md) - отписывается от получения обновлений через WebHook.
- [upload_url](doc/upload_url.md) - вспомогательная функция получения URL загружаемого изображения.


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
Возвращает информацию о текущем боте. Текущий бот может быть идентифицирован по токену доступа. Метод
возвращает идентификатор бота, имя и аватар (если есть) Returns info about current bot. Current bot can be
identified by access token. Method returns bot identifier, name and avatar (if any)
**:return:** bot_info: возвращает информацию о боте.  
       
### edit_bot_info(name, username, description, commands, photo, photo_url=None):
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
**:param photo:** файл с изображением бота  
**:param photo_url:** ссылка на изображение бота  
**:return edit_bot_info:** возвращает результат PATCH запроса.  


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
Возвращает пользователей, участвовавших в чате.  
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


### edit_chat_info(chat_id, icon, title, icon_url=None):
https://dev.tamtam.chat/#operation/editChat  
Редактирование информации чата: заголовок и значок  
Edits chat info: title, icon  
**:param chat_id:** идентификатор изменяемого чата    
**:param icon:** файл значка    
**:param icon_url:** ссылка на изображение  
**:param title:** заголовок    
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

### get_link_name(update):
https://botapi.tamtam.chat/updates  
Получение имени пользователя пересланного сообщения  
**:param update:** результат работы метода get_update  
**:return:** возвращает, если это возможно, значение поля 'name' пересланного боту сообщения (от кого)  

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
**:param update:** = результат работы метода get_update  
**:return:** возвращает, если это возможно, значение поля 'mid'  

### edit_message(message_id, text, attachments=None, link=None, notify=True):
https://dev.tamtam.chat/#operation/editMessage  
Метод  изменения (обновления) любого контента по его идентификатору  
**:param message_id:** Идентификатор редактируемого контента  
**:param attachments:** Новый массив объектов (файл, фото, видео, аудио, кнопки)  
**:param text:** Обновленное текстовое сообщение  
**:param link:** Обновленное пересылаемые (цитируемые) сообщение  
**:param notify:** Уведомление о событии, если значение false, участники чата не будут уведомлены  
**:return update:** Возвращает результат PUT запроса  

### send_typing_on(chat_id):
https://dev.tamtam.chat/#operation/sendAction  
Отправка уведомления от бота в чат - 'печатает...'  
**:param chat_id:** чат куда необходимо отправить уведомление  
**:return:**

### send_mark_seen(chat_id):
https://dev.tamtam.chat/#operation/sendAction  
Отправка в чат маркера о прочтении ботом сообщения  
**:param chat_id:** чат куда необходимо отправить уведомление  
**:return:**

### send_sending_video(chat_id):
https://dev.tamtam.chat/#operation/sendAction   
Отправка уведомления от бота в чат - 'отправка видео...'  
**:param chat_id:** чат куда необходимо отправить уведомление  
**:return:**

### send_sending_audio(chat_id):
https://dev.tamtam.chat/#operation/sendAction  
Отправка уведомления от бота в чат - 'отправка аудио...'  
**:param chat_id:** чат куда необходимо отправить уведомление  
**:return:**

### send_sending_photo(chat_id):
https://dev.tamtam.chat/#operation/sendAction  
Отправка уведомления от бота в чат - 'отправка фото ...'  
**:param chat_id:** чат куда необходимо отправить уведомление  
**:return:**

### send_sending_image(chat_id):
https://dev.tamtam.chat/#operation/sendAction  
Отправка уведомления от бота в чат - 'отправка фото ...'  
**:param chat_id:** чат куда необходимо отправить уведомление  
**:return:**

### send_sending_file(chat_id):
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

### send_buttons(text, buttons, chat_id):
Send buttons to specific chat_id by post request  
Отправляет кнопки (количество, рядность и функционал определяются параметром buttons) в соответствующий чат  
**:param text:** Текст выводимый над блоком кнопок  
**:param chat_id:** integer, chat id of user / чат где будут созданы кнопки  
**:param buttons:** массив кнопок, сформированный методами button_callback, button_contact, button_link и т.п.    
**:return update:** результат POST запроса на отправку кнопок  

### upload_url(type):
https://dev.tamtam.chat/#operation/getUploadUrl
Вспомогательная функция получения URL для загрузки контента в ТамТам
:param type: тип контента ('audio', 'video', 'file', 'photo')
:return: URL на который будет отправляться контент

### attach_file(content, content_name=None):
https://dev.tamtam.chat/#operation/sendMessage
Метод подготовки файла (файлы загружаются только по одному) совместно с кнопками
:param content: имя файла или полный путь доступный боту на машине где он запущен, например '/mnt/files/movie.mp4'
:param content_name: имя с которым будет загружен файл
:return attach: подготовленный контент

### send_file(content, chat_id, text=None, content_name=None):
https://dev.tamtam.chat/#operation/sendMessage
Метод отправки файла в указанный чат (файлы загружаются только по одному)
:param content: имя файла или полный путь доступный боту на машине где он запущен, например 'movie.mp4'
:param chat_id: чат куда будет загружен файл
:param text: сопровождающий текст к отправляемому файлу
:param content_name: имя с которым будет загружен файл
:return update: результат работы POST запроса отправки файла

### attach_image(content):
https://dev.tamtam.chat/#operation/sendMessage
Метод подготовки изображений (нескольких изображений) в указанный чат
:param content: имя файла или список имен файлов с изображениями
:return attach: подготовленный контент

### send_image(content, chat_id, text=None):
https://dev.tamtam.chat/#operation/sendMessage
Метод отправки фoто (нескольких фото) в указанный чат
:param content: имя файла или список имен файлов с изображениями
:param chat_id: чат куда будут загружены изображения
:param text: Сопровождающий текст к отправляемому контенту
:return update: результат работы POST запроса отправки файла

### attach_image_url(url):
https://dev.tamtam.chat/#operation/sendMessage
Метод подготовки изображений (нескольких изображений) к отправке по их url
:param url: http адрес или список адресов с изображениями
:return attach: подготовленный контент

### send_image_url(url, chat_id, text=None):
https://dev.tamtam.chat/#operation/sendMessage
Метод отправки фото (нескольких фото) в указанный чат по url
:param url: http адрес или список адресов с изображениями
:param chat_id: чат куда будут загружены изображения
:param text: сопровождающий текст к отправляемому контенту
:return update: результат работы POST запроса отправки фото

### attach_video(content):
https://dev.tamtam.chat/#operation/sendMessage
Метод подготовки к отправке видео (нескольких видео)
:param content: имя файла или полный путь доступный боту на машине где он запущен, например 'movie.mp4'
иди список файлов ['movie.mp4', 'movie2.mkv']
:return attach: подготовленный контент

### send_video(content, chat_id, text=None):
https://dev.tamtam.chat/#operation/sendMessage
Метод отправки видео (нескольких видео) в указанный чат
:param content: имя файла или полный путь доступный боту на машине где он запущен, например 'movie.mp4'
иди список файлов ['movie.mp4', 'movie2.mkv']
:param chat_id: чат куда будут загружены видео
:param text: Сопровождающий текст к отправляемому(мым) видео
:return update: результат работы POST запроса отправки видео

### attach_audio(content):
https://dev.tamtam.chat/#operation/sendMessage
Метод подготовки аудио (только по одному) к отправке
:param content: имя файла или полный путь доступный боту на машине где он запущен (например 'audio.mp3'),
файлы защищенные авторскими правами не загружаются
:return attach: подготовленный контент

### send_audio(content, chat_id, text=None):
https://dev.tamtam.chat/#operation/sendMessage
Метод отправки аудио (только по одному) в указанный чат
:param content: имя файла или полный путь доступный боту на машине где он запущен (например 'audio.mp3'),
файлы защищенные авторскими правами не загружаются
:param chat_id: чат куда будет загружено аудио
:param text: сопровождающий текст к отправляемому аудио
:return update: результат работы POST запроса отправки аудио

### send_forward_message(text, mid, chat_id):
https://dev.tamtam.chat/#operation/sendMessage
Send forward message specific chat_id by post request
Пересылает сообщение в указанный чат
:param text: текст к пересылаемому сообщению или None
:param mid: message_id пересылаемого сообщения
:param chat_id: integer, chat id of user / чат куда отправится сообщение
:return update: response | ответ на POST message в соответствии с API

### link_reply(mid):
https://dev.tamtam.chat/#operation/sendMessage
Формирует параметр link на цитируемуе сообщение для отправки через send_message
:param mid: идентификатор сообщения (get_message_id) на которое готовим link
:return link: сформированный параметр link

### link_forward(mid):
https://dev.tamtam.chat/#operation/sendMessage
Формирует параметр link на пересылаемое сообщение для отправки через send_message
:param mid: идентификатор сообщения (get_message_id) на которое готовим link
:return link: сформированный параметр link

### send_reply_message(text, mid, chat_id):
https://dev.tamtam.chat/#operation/sendMessage
Send reply message specific chat_id by post request
Формирует ответ на сообщение в указанный чат
:param text: текст ответа на сообщение (обязательный параметр)
:param mid: message_id сообщения на которое формируется ответ
:param chat_id: integer, chat id of user / чат куда отправится сообщение
:return update: response | ответ на POST запрос в соответствии с API

### token_upload_content(type, content, content_name=None):
https://dev.tamtam.chat/#operation/sendMessage
Вспомогательная функция получения Tokena для загрузки контента в ТамТам
:param type: тип контента ('audio', 'video', 'file', 'photo')
:param content: имя файла или полный путь доступный боту на машине где он запущен (например 'movie.mp4')
:param content_name: Имя с которым будет загружен файл
:return update: результат работы POST запроса отправки файла

### send_message(text, chat_id, user_id=None, attachments=None, link=None, notify=True, dislinkprev=False):
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


### send_answer_callback(callback_id, notification, text=None, attachments=None, link=None, notify=None):
https://dev.tamtam.chat/#operation/answerOnCallback  
Метод отправки ответа после того, как пользователь нажал кнопку. Ответом может быть обновленное сообщение или/и кратковременное всплывающее уведомление пользователя.  
**:param callback_id:** параметр, соответствующий нажатой кнопке  
**:param notification:** кратковременное, всплывающее уведомление  
**:param text:** обновленное (новое) текстовое сообщение  
**:param attachments:** измененный (новый) контент (изображения, видео, кнопки и т.д.)  
**:param link:** цитируемое сообщение  
**:param notify:** если false, то участники чата не получат уведомление (по умолчанию true)  
**:return update:** результат POST запроса  

