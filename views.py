from savraska.view import View


class HomePage(View):

    def get(self, request, *args, **kwargs):
        return 'Home page'


class Math(View):
    def get(self, request, *args, **kwargs):
        first = request.GET.get('first')
        if not first or not first[0].isnumeric():
            return 'first не задан'

        second = request.GET.get('second')
        if not second or not second[0].isnumeric():
            return 'second не задан'

        return f'Sum: {int(first) + int(second)}'