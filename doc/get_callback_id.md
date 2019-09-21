## get_callback_id(update)
Метод получения значения callback_id при нажатии кнопки, callback_id необходим для метода [send_answer_callback](doc/send_answer_callback)  
API = subscriptions/Get updates/[updates][0][callback][callback_id]  
:param update: результат работы метода [get_updates](doc/get_updates)  
:return: возвращает callback_id нажатой кнопки или None  
