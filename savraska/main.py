import re
from typing import List, Type

from savraska.urls import Url
from savraska.exceptions import PageNotFound, MethodNotAllowed
from savraska.view import View
from savraska.request import Request
from savraska.response import Response
from savraska.middleware import BaseMiddleWare


class Savraska:

    def __init__(self, urls: List[Url], settings: dict, middlewares: List[Type[BaseMiddleWare]]):
        self.urls = urls
        self.settings = settings
        self.middlewares = middlewares

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """

        view = self.__get_view(environ)
        request = self.__get_request(environ)
        self.__apply_middleware_to_request(request)

        response = self.__get_response(environ, view, request)
        self.__apply_middleware_to_response(response)

        start_response(str(response.status_code), response.headers.items())

        return [response.body]

    def __prepare_url(self, url: str):
        return url if url.endswith('/') else f'{url}/'

    def __find_view(self, raw_url: str) -> Type[View]:
        url = self.__prepare_url(raw_url)
        for path in self.urls:
            m = re.match(path.url, url)
            if m is not None:
                return path.view

        raise PageNotFound

    def __get_view(self, environ: dict) -> View:
        raw_url = environ['PATH_INFO']
        return self.__find_view(raw_url)()

    def __get_request(self, environ: dict) -> Request:
        return Request(environ, self.settings)

    def __get_response(self, environ: dict, view: View, request: Request) -> Response:
        method = environ['REQUEST_METHOD'].lower()

        if not hasattr(view, method):
            raise MethodNotAllowed

        return getattr(view, method)(request)

    def __apply_middleware_to_request(self, request):
        for middleware in self.middlewares:
            middleware().to_request(request)

    def __apply_middleware_to_response(self, response):
        for middleware in self.middlewares:
            middleware().to_response(response)


class SavraskaFake(Savraska):
    """ Фейковое приложение, всегда вощвращает 200 ок"""

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """

        start_response('200 OK', [('Content-Type', 'text/html')])

        return [b'Hello from Fake']


class SavraskaDebug(Savraska):
    """ Отладочное приложение, выводит параметры запроса в консоль """

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """
        print('DEBUG MODE')
        print(environ)

        return super(SavraskaDebug, self).__call__(environ, start_response)
