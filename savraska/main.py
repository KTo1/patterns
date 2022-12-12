from typing import List
from savraska.urls import Url


class Savraska:

    def __init__(self, urls: List[Url]):
        self.urls = urls

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """

        # сначала в функцию start_response передаем код ответа и заголовки
        start_response('200 OK', [('Content-Type', 'text/html')])
        # возвращаем тело ответа в виде списка из bite
        return [b'Hello world from a simple WSGI application!']
