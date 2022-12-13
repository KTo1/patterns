import re
from typing import List, Type

from savraska.urls import Url
from savraska.exceptions import PageNotFound, MethodNotAllowed
from savraska.view import View
from savraska.request import Request
from savraska.response import Response


class Savraska:

    def __init__(self, urls: List[Url], settings: dict):
        self.urls = urls
        self.settings = settings

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """

        # from pprint import pprint
        # pprint(environ)

        view = self.__get_view(environ)
        request = self.__get_request(environ)
        response = self.__get_response(environ, view, request)

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