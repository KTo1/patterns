import re
from typing import List, Type

from savraska.urls import Url
from savraska.exceptions import PageNotFound, MethodNotAllowed
from savraska.view import View


class Savraska:

    def __init__(self, urls: List[Url]):
        self.urls = urls

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """

        from pprint import pprint
        pprint(environ)

        raw_url = environ['PATH_INFO']
        view = self.__find_view(raw_url)()

        method = environ['REQUEST_METHOD'].lower()

        if not hasattr(view, method):
            raise MethodNotAllowed

        raw_response = getattr(view, method)(None)
        response = raw_response.encode('utf-8')

        print('response - >', response)

        # сначала в функцию start_response передаем код ответа и заголовки
        start_response('200 OK', [('Content-Type', 'text/html')])
        # возвращаем тело ответа в виде списка из bite
        return [response]

    def __prepare_url(self, url: str):
        return url if url.endswith('/') else f'{url}/'

    def __find_view(self, raw_url: str) -> Type[View]:
        url = self.__prepare_url(raw_url)
        for path in self.urls:
            m = re.match(path.url, url)
            if m is not None:
                return path.view

        raise PageNotFound