from savraska.view import View


class HomePage(View):

    def get(self, request, *args, **kwargs):
        return 'Home page'