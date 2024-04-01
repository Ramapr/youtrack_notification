# tracker_bot

telegram notification for self-hosted youtrack


## How-to

```
$ cp .env-template .env
```
заполнить все поля в файле `.env`

### local run with pip
```
$ pip install -r requirements.txt
$ python main.py
```

### remote with Dockerfile

```
$ docker build --tag 'tracker' .
$ docker run --name utrack -d 'tracker'
```
## настройка и добавление бота

1. создание бота :
- найти в телеграм @BotFather
- /newbot
- name
- name '_bot'
- token его запомнить

2. узнать chat_id:
- добавить в чат бот @LeadConverter | Инструменты
- /get_chat_id

3. добавление бота : добавить бота в чата через настройки группы
