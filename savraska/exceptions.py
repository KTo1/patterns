class PageNotFound(Exception):
    code = 404
    text = 'Страница не найдена'


class MethodNotAllowed(Exception):
    code = 405
    text = 'Неподдерживаемый HTTP метод'


class UserException(Exception):
    text = ''