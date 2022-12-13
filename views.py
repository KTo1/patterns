from savraska.view import View
from savraska.response import Response


class HomePage(View):

    def get(self, request, *args, **kwargs):
        return Response(body='Home page')


class Math(View):
    def get(self, request, *args, **kwargs):
        first = request.GET.get('first')
        if not first or not first[0].isnumeric():
            return Response(body='first не задан')

        second = request.GET.get('second')
        if not second or not second[0].isnumeric():
            return Response(body='second не задан')

        return Response(body=f'Sum: {int(first[0]) + int(second[0])}')