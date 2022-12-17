# patterns
Паттерны проектирования

Будем писать свой WSGI фреймворк

Работает на waitress (
https://docs.pylonsproject.org/projects/waitress/en/latest/usage.html
pip install waitress
).

Работают страницы:
корневая и /contact

Почта не отправляется, пока складывается в каталог "savraska/mail" в формате json

Как запустить:
Или запустить run.py
Или выполнить: waitress-serve --listen=127.0.0.1:8000 main:app



