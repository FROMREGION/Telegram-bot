About Bot:

This is a Telegram bot with a database.
Features:
- Full administration through the bot
- Automatic distribution of created events for selected user groups.
- purchase a subscription for a specific group of users
-

###############################################################

BOT CREATED BY
    1.  Evgeniy Malyh
        VK http://vk.com/evgeniymalyh
    2.  Vadim Tchunikhin
        VK https://vk.com/duuuda

###############################################################

Подготовка к запуску бота:

Часть 1: Установите библиотеки необходимые для запуска бота
Откройте консоль и введите:
pip install pytelegrambotapi
pip install SQLAlchemy
pip install pysocks


Часть 2: Регистрация бота
Самая простая и описанная часть. 
Очень коротко: нужно найти бота @BotFather, написать ему /start, или /newbot, заполнить поля, которые он спросит (название бота и его короткое имя). 
Получить сообщение с токеном бота и ссылкой на документацию. 
Токен нужно сохранить, это единственный ключ для авторизации бота и взаимодействия с ним.
Ещё нам нужно узнать свой ID - это можно сделать написав боту в телеграмме @userinfobot

Часть 2.1: Активация платёжки
В BotFather выбрать своего бота -> выбрать Payments -> Выбрать подходящую вам платёжную систему и следовать инструкции.
По окончанию BotFather пришлёт вам PAYMENTS_PROVIDER токен, его нужно изменить в файле config.json

Часть 3: Редактирование бота
Открыть файл "config.json" в любом текстовом редакторе.
И изменить все параметры

Цена записывается в формате 100 рублей 00 копеек = 10000
"PRICE": "10000" / 100.00 руб

Часть 4: Запуск
Запустить файл main.py через терминал
Если появляется ошибка подключения:
Зайти в файл bot.py и изменить IP:PORT в строке apihelper.proxy = {'https': 'socks5://IP:PORT'}
/ apihelper.proxy = {'https': 'socks5://5.133.202.167:19619'}
/
/	На хостинге данная строка должна быть закомментирована!!!!!!
/
Если снова появляется ошибка подключения
Переходим на один из этих сайтов
http://free-proxy.cz/ru/proxylist/country/all/socks5/ping/all
http://spys.one/proxys/US/
http://spys.one/proxys/GB/
http://spys.one/proxys/DE/
http://spys.one/proxys/SE/
И пробуем подставлять IP адрес и порт в строку которую расскоментировали

apihelper.proxy = {'https': 'socks5://СЮДА_IP:СЮДА_ПОРТ'}