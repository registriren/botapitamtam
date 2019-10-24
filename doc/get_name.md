## get_name(update)
https://dev.tamtam.chat/#operation/getUpdates
Получение имени пользователя, инициировавшего событие  
:param **update** = результат работы метода get_update  
:return: **name:** возвращает, если это возможно, значение поля 'name' не зависимо от события, произошедшего с ботом, если событие - "удаление сообщения", то name = None
