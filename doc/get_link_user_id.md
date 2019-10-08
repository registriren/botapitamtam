 ## get_link_user_id(update)
 https://dev.tamtam.chat/#operation/getUpdates  
 Получения идентификатора пользователя пересланного сообщения  
 API = subscriptions/Get updates/[updates][0][message][link][sender][user_id]  
 **:param** update = результат работы метода [get_updates](get_updates.md)  
 **:return:** возвращает, если это возможно, значение поля 'user_id' пересланного боту сообщения (от кого)  
