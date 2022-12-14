# patterns
Паттерны проектирования

Будем писать свой WSGI фреймворк

Работает на waitress (
https://docs.pylonsproject.org/projects/waitress/en/latest/usage.html
pip install waitress
).

Есть две страницы:
корневая и /about

Как запустить:
Или запустить run.py
Или выполнить: waitress-serve --listen=127.0.0.1:8000 main:app



