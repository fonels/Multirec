Файлик [gpt_request.py](https://github.com/fonels/Multirec/blob/main/gpt_request.py) отправляет запросы в api OpenAI и api omdb, получает и обрабатывает их.

В файле [config.py](https://github.com/fonels/Multirec/blob/main/config.py) хранятся важные данные для отправки запросов:
```
open_ai_api_key -  api-ключ OpenAI
http_proxy_data -  данные от proxy-сервера, необходимые для отправки запроса к api OpenAI (недоступен для российских ip-адресов)
omdb_api_key -  api-ключ omdb
```
