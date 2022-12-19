class PageNotFound(Exception):
    code = 404
    text = 'Страница не найдена'


class MethodNotAllowed(Exception):
    code = 405
    text = 'Неподдерживаемый HTTP метод'


class UserException(Exception):
    text = ''


class InvalidGETException(Exception):
    text = 'Неверные параметры GET'


class InvalidPOSTException(Exception):
    text = 'Неверные параметры POST'