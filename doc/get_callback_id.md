## get_callback_id(update)
API = subscriptions/Get updates/[updates][0][callback][callback_id]  
Метод получения значения callback_id нажатой кнопки для передачи методу [send_answer_callback](send_answer_callback.md)  
:param update: результат работы метода [get_updates](doc/get_updates.md)  
:return: возвращает callback_id нажатой кнопки или None  
