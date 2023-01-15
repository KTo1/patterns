class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


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