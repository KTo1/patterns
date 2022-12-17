from urllib.parse import parse_qs


class Request:

    def __init__(self, environ: dict, settings: dict):
        self.build_get_param(environ['QUERY_STRING'])
        self.build_post_param(environ['wsgi.input'].read())

        self.settings = settings
        self.environ = environ
        self.extra = {}

    def __getattr__(self, item):
        return self.extra.get(item)

    def build_get_param(self, raw_param: str):
        self.GET = parse_qs(raw_param)

    def build_post_param(self, raw_bytes: bytes):
        raw_param = raw_bytes.decode('utf-8')
        self.POST = parse_qs(raw_param)