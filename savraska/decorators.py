from time import time

from savraska.urls import Url
from typing import List


class AppRoute:
    """ Декоратор для добавления урла к вьюхе """

    def __init__(self, urlpatterns: List[Url], url: str):
        self.__urlpatterns = urlpatterns
        self.__url = url

    def __call__(self, cls):
        self.__urlpatterns.append(Url(self.__url, cls))


class Debug:
    """ Декоратор для замера времени выполнения метода """

    def __call__(self, method, *args, **kwargs):

        def wrapper(*args, **kwargs):
            time_start = time()
            result = method(*args, **kwargs)
            print(f'Debug log {method.__name__} spent -> {(time() - time_start):2.2f} ms')
            return result
        return wrapper

