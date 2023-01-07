from savraska.request import Request
from savraska.response import Response
from savraska.templates import build_template


class View:

    def get(self, request: Request, *args, **kwargs) -> Response:
        pass

    def post(self, request: Request, *args, **kwargs) -> Response:
        pass


# поведенческий паттерн - Шаблонный метод
class TemplateView(View):
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def get_body(self, request, context, template_name):
        return build_template(request, context, template_name)

    def render_template_with_context(self, request):
        template_name = self.get_template()
        context = self.get_context_data()
        body = self.get_body(request, context, template_name)

        return Response(request, body=body)

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.render_template_with_context(request)


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'
    redirect_name = 'list.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def post(self, request: Request, *args, **kwargs) -> Response:
        # метод пост
        data = self.get_request_data(request)
        self.create_obj(data)

        return self.render_template_with_context(request)
