import re
from typing import List

from savraska.urls import Url
from savraska.exceptions import PageNotFound


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

    def __prepare_url(self, url: str):
        return url if url.endswith('/') else f'{url}/'

    def __find_view(self, raw_url: str):
        url = self.__prepare_url(raw_url)

        for path in self.urls:
            m = re.match(path.url, url)
            if m is not None:
                return path.view

        raise PageNotFound