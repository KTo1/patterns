from datetime import datetime

from savraska.view import View
from savraska.response import Response
from savraska.templates import build_template

class HomePage(View):

    def get(self, request, *args, **kwargs):
        context = {'time': str(datetime.now())}
        body = build_template(request, context, 'home.html')
        return Response(request, body=body)


class AboutPage(View):

    def get(self, request, *args, **kwargs):
        context = {'session_id': str(request.session_id)}
        body = build_template(request, context, 'about.html')
        return Response(request, body=body)

class MailPage(View):

    def get(self, request, *args, **kwargs):
        context = {'session_id': str(request.session_id)}
        body = build_template(request, context, 'mail.html')
        return Response(request, body=body)

class Math(View):

    def get(self, request, *args, **kwargs):
        first = request.GET.get('first')
        if not first or not first[0].isnumeric():
            return Response(request, body='first не задан')

        second = request.GET.get('second')
        if not second or not second[0].isnumeric():
            return Response(request, body='second не задан')

        return Response(request, body=f'Sum: {int(first[0]) + int(second[0])}')