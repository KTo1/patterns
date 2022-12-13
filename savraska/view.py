from savraska.request import Request
from savraska.response import Response


class View:

    def get(self, request: Request, *args, **kwargs) -> Response:
        pass

    