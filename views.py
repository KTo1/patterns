import os
from datetime import datetime

from savraska.request import Request
from savraska.view import View
from savraska.response import Response
from savraska.templates import build_template
from savraska.utils import EMail


class IndexPage(View):

    def get(self, request: Request, *args, **kwargs):
        context = {'time': str(datetime.now())}
        body = build_template(request, context, 'index.html')

        return Response(request, body=body)


class StaticPages(View):
    def get(self, request: Request, *args, **kwargs):
        assert request.settings.get('BASE_DIR')
        assert request.settings.get('STATIC_DIR_NAME')

        static_dir = os.path.join(request.settings.get('BASE_DIR'), request.settings.get('STATIC_DIR_NAME'))

        static_path = os.path.join(static_dir, os.path.dirname(request.environ['PATH_INFO']))
        with open('F:\Projects\Learning\GB\patterns\static\style\style.css', 'r') as f:
            body = f.read()

        return Response(request, body=body)


class AboutPage(View):

    def get(self, request: Request, *args, **kwargs):
        context = {'session_id': str(request.session_id)}
        body = build_template(request, context, 'about.html')

        return Response(request, body=body)


class MailPage(View):

    def get(self, request: Request, *args, **kwargs):
        context = {}
        body = build_template(request, context, 'mail.html')

        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        name = name[0] if name else ''
        email = email[0] if email else ''
        subject = subject[0] if subject else ''
        message = message[0] if message else ''

        email = EMail(name, email, subject, message)
        email.send()

        context = {'info':'Сообщение успешно отправлено!'}
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
