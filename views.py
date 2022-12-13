from datetime import datetime

from savraska.view import View
from savraska.response import Response
from savraska.templates import build_template

class HomePage(View):

    def get(self, request, *args, **kwargs):
        context = {'time': str(datetime.now())}
        body = build_template(request, context, 'home.html')
        return Response(body=body)


class Math(View):
    def get(self, request, *args, **kwargs):
        first = request.GET.get('first')
        if not first or not first[0].isnumeric():
            return Response(body='first не задан')

        second = request.GET.get('second')
        if not second or not second[0].isnumeric():
            return Response(body='second не задан')

        return Response(body=f'Sum: {int(first[0]) + int(second[0])}')