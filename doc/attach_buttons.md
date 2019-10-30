## attach_buttons(buttons)  
https://dev.tamtam.chat/#operation/sendMessage    
Метод подготовки кнопок к отправке через метод [send_content](send_content.md)
```bash
:param buttons = [
                          [{"type": 'callback',
                           "text": 'line1_key1_text',
                           "payload": 'payload1'},
                          {"type": 'link',
                           "text": 'line1_key2_API TamTam',
                           "url": 'https://dev.tamtam.chat',
                           "intent": 'positive'}],
                           [{"type": 'callback',
                           "text": 'line2_key1_text',
                           "payload": 'payload1'},
                          {"type": 'link',
                           "text": 'line2_key2_API TamTam',
                           "url": 'https://dev.tamtam.chat',
                           "intent": 'positive'}]
                         ]
                           :param type: реакция на нажатие кнопки
                           :param text: подпись кнопки
                           :param payload: результат нажатия кнопки
                           :param intent: цвет кнопки    
:return: attach: подготовленный контент  
```
## [Пример](https://github.com/registriren/botapitamtam/blob/master/doc/edit_content.md#пример)
