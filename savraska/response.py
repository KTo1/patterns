from savraska.request import Request


class Response:

    def __init__(self, request: Request, status_code: int=200, headers: dict=None, body: str='' ):
        self.status_code = status_code
        self.headers = {}
        self.body = b''

        self.__set_base_headers()
        if headers:
            self.update_headers(headers)

        self.__set_body(body)

        self.request = request
        self.extra = {}

    def __getattr__(self, item):
        return self.extra.get(item)

    def __set_base_headers(self):
        self.headers = {
            'Content-Type': 'text/html; charset=UTF-8'
        }

    def __set_body(self, raw_body: str):
        self.body = raw_body.encode('utf-8')

    def update_headers(self, headers: dict):
        self.headers.update(headers)