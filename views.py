from datetime import datetime

from savraska.exceptions import InvalidGETException, InvalidPOSTException
from savraska.request import Request
from savraska.view import View
from savraska.response import Response
from savraska.templates import build_template
from savraska.utils import EMail
from savraska.logs import savraska_log
from savraska.engine import engine
from savraska.decorators import AppRoute, Debug
from savraska.urls import Url


urlpatterns = []


class IndexPage(View):

    @Debug()
    def get(self, request: Request, *args, **kwargs):
        context = {'time': str(datetime.now())}
        body = build_template(request, context, 'index.html')

        savraska_log.debug(f'Переход к главной странице, {str(request)}')

        return Response(request, body=body)


class SchedulesPage(View):

    def get(self, request: Request, *args, **kwargs):
        context = {}
        body = build_template(request, context, 'schedules.html')

        return Response(request, body=body)


class ContactPage(View):

    def get(self, request: Request, *args, **kwargs):
        context = {}
        body = build_template(request, context, 'contact.html')

        savraska_log.debug(f'Переход к странице контактов, {str(request)}')

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
        body = build_template(request, context, 'contact.html')

        return Response(request, body=body)


class CoursePage(View):

    def get(self, request: Request, *args, **kwargs):
        context = {'categories': engine.categories}
        body = build_template(request, context, 'courses.html')

        return Response(request, body=body)


class CourseCategoryPage(View):
    def get(self, request: Request, *args, **kwargs):
        courses = []
        if request.GET:
            category_id = request.GET['id'][0]
            category = engine.get_category_by_id(category_id)
            courses = engine.get_courses_by_category(category)

        context = {'courses': courses, 'category': category}
        body = build_template(request, context, 'courses-category.html')

        return Response(request, body=body)


class CourseCopyPage(View):

    def get(self, request: Request, *args, **kwargs):

        if request.GET:
            course_name = request.GET['name'][0]
            category_id = request.GET['category_id'][0]

            category = engine.get_category_by_id(category_id)

        else:
            raise InvalidGETException

        context = {'course_name': course_name, 'category': category}
        body = build_template(request, context, 'courses-course-copy.html')

        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:

        if request.POST:
            category_id = request.POST['category_id'][0]
            name = request.POST['name'][0]
            source_course_name = request.POST['source_course_name'][0]

            category = engine.get_category_by_id(category_id)
            source_course = engine.get_course_by_name(source_course_name)
            new_course = source_course.clone()
            new_course.name = name

            category.course_add(new_course)
            engine.add_course(new_course)

            courses = engine.get_courses_by_category(category)
        else:
            raise InvalidPOSTException

        context = {'courses': courses, 'category': category}
        body = build_template(request, context, 'courses-category.html')

        return Response(request, body=body)


class CourseAddPage(View):

    def get(self, request: Request, *args, **kwargs):

        if request.GET:
            category_id = request.GET['category_id'][0]
            category = engine.get_category_by_id(category_id)
        else:
            raise InvalidGETException

        context = {'categories': engine.categories, 'category': category}
        body = build_template(request, context, 'courses-course-add.html')

        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:

        if request.POST:
            category_id = request.POST['category_id'][0]
            category = engine.get_category_by_id(category_id)
            new_course = engine.create_course('record', request.POST['name'][0], category)
            engine.add_course(new_course)
            courses = engine.get_courses_by_category(category)
        else:
            raise InvalidPOSTException

        context = {'courses': courses, 'category': category}
        body = build_template(request, context, 'courses-category.html')

        return Response(request, body=body)


class CourseAddCategoryPage(View):

    def get(self, request: Request, *args, **kwargs):
        context = {'categories': engine.categories}
        body = build_template(request, context, 'courses-cat-add.html')

        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:

        if request.POST:
            new_category = engine.create_category(request.POST['name'][0])
            engine.add_category(new_category)

        context = {'categories': engine.categories}
        body = build_template(request, context, 'courses.html')

        return Response(request, body=body)


@AppRoute(urlpatterns, '^/math.*$')
class Math(View):

    def get(self, request, *args, **kwargs):
        first = request.GET.get('first')
        if not first or not first[0].isnumeric():
            return Response(request, body='first не задан')

        second = request.GET.get('second')
        if not second or not second[0].isnumeric():
            return Response(request, body='second не задан')

        return Response(request, body=f'Sum: {int(first[0]) + int(second[0])}')


urlpatterns.extend([
    Url('^/$', IndexPage),
    # Url('^/math.*$', Math),
    Url('^/contact/$', ContactPage),
    Url('^/schedules/$', SchedulesPage),
    Url('^/courses/$', CoursePage),
    Url('^/courses-category/$', CourseCategoryPage),
    Url('^/add-category/$', CourseAddCategoryPage),
    Url('^/add-course/$', CourseAddPage),
    Url('^/copy-course/$', CourseCopyPage),
])