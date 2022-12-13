from urllib.parse import parse_qs


class Request:

    def __init__(self):
        pass


    def build_get_param(self, raw_param: str):
        self.GET = parse_qs(raw_param)