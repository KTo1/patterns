from datetime import datetime

from savraska.database import MapperRegistry, UnitOfWork
from savraska.exceptions import InvalidGETException, InvalidPOSTException
from savraska.request import Request
from savraska.view import View, ListView, CreateView
from savraska.response import Response
from savraska.templates import build_template
from savraska.utils import EMail, SMSNotifier, EMAILNotifier, JsonSerializer
from savraska.logs import savraska_log, Loger
from savraska.engine import engine
from savraska.decorators import AppRoute, Debug
from savraska.urls import Url


savraska_loger = Loger('file')
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


urlpatterns = []


class IndexPage(View):

    @Debug()
    def get(self, request: Request, *args, **kwargs):
        context = {'time': str(datetime.now())}
        body = build_template(request, context, 'index.html')

        savraska_log.debug(f'Переход к главной странице, {str(request)}')
        savraska_loger.write(f'Переход к главной странице, {str(request)}')

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


class CoursePage(ListView):
    # queryset = engine.get_categories()
    template_name = 'courses.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        category_list = []
        for category in mapper.all():
            category_list.append({'category': category, 'level': '', 'id': category.id})

        return category_list


class CourseCategoryPage(View):
    def get(self, request: Request, *args, **kwargs):
        courses = []
        category = ''
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
            course_id = request.GET['course_id'][0]
            category_id = request.GET['category_id'][0]

            category = engine.get_category_by_id(category_id)
            course = engine.get_course_by_id(course_id)
        else:
            raise InvalidGETException

        context = {'course': course, 'category': category}
        body = build_template(request, context, 'courses-course-copy.html')

        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:

        if request.POST:
            category_id = request.POST['category_id'][0]
            name = request.POST['name'][0]
            source_course_id = request.POST['source_course_id'][0]

            category = engine.get_category_by_id(category_id)
            source_course = engine.get_course_by_id(source_course_id)
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


class CourseAddPage(CreateView):
    template_name = 'courses-category.html'

    def get(self, request: Request, *args, **kwargs):

        if request.GET:
            category_id = request.GET['category_id'][0]
            category = engine.get_category_by_id(category_id)
        else:
            raise InvalidGETException

        context = {'category': category}
        body = build_template(request, context, 'courses-course-add.html')

        return Response(request, body=body)

    def get_request_data(self, request):
        data = {'course_name': '', 'category': ''}
        if request.POST:
            category_id = request.POST['category_id'][0]
            category = engine.get_category_by_id(category_id)
            course_name = request.POST['name'][0]

            data['course_name'] = course_name
            data['category'] = category

        return data

    def create_obj(self, data):
        course_name = data['course_name']
        category = data['category']

        new_course = engine.create_course('record', course_name, category)
        new_course.add_observer(SMSNotifier())
        new_course.add_observer(EMAILNotifier())

        engine.add_course(new_course)

        UnitOfWork.new_current()
        UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

        new_course.mark_new()
        UnitOfWork.get_current().commit()

    def get_context_data(self):
        category = engine.courses[-1].category
        courses = engine.get_courses_by_category(category)

        context = {'courses': courses, 'category': category}
        return context


class CourseAddCategoryPage(CreateView):
    template_name = 'courses.html'

    def get(self, request: Request, *args, **kwargs):
        parent_category_id = None
        if request.GET:
            parent_category_id = request.GET['category_id'][0]
        context = {'parent_category_id': parent_category_id}
        body = build_template(request, context, 'courses-cat-add.html')

        return Response(request, body=body)

    def get_request_data(self, request):
        data = {'parent_category': '', 'category_name': ''}
        if request.POST:
            parent_category_id = request.POST.get('parent_category_id')
            parent_category = None
            if parent_category_id:
                parent_category_id = parent_category_id[0]
                parent_category = engine.get_category_by_id(parent_category_id)

            data['parent_category'] = parent_category
            data['category_name'] = request.POST['name'][0]

        return data

    def create_obj(self, data):
        parent_category = data['parent_category']
        category_name = data['category_name']

        new_category = engine.create_category(category_name)
        if not parent_category:
            engine.add_category(new_category)

        UnitOfWork.new_current()
        UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

        new_category.mark_new()
        UnitOfWork.get_current().commit()

    def get_context_data(self):
        mapper = MapperRegistry.get_current_mapper('category')
        category_list = []
        for category in mapper.all():
            category_list.append({'category': category, 'level': '', 'id': category.id})

        return {'objects_list': category_list}


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


@AppRoute(urlpatterns, '^/students/$')
class StudentsPage(View):
    def get(self, request: Request, *args, **kwargs):
        context = {}
        body = build_template(request, context, 'students.html')

        return Response(request, body=body)


@AppRoute(urlpatterns, '^/students-list/$')
class StudentsListPage(ListView):
    template_name = 'students-list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@AppRoute(urlpatterns, '^/students-add/$')
class StudentsAdd(CreateView):
    template_name = 'students.html'

    def get_request_data(self, request):
        student_name = ''
        if request.POST:
            student_name = request.POST.get('name')[0]
        return student_name

    def create_obj(self, data):
        UnitOfWork.new_current()
        UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

        student = engine.create_user('student', data)
        engine.add_student(student)
        student.mark_new()
        UnitOfWork.get_current().commit()

    def get(self, request: Request, *args, **kwargs):
        context = {}
        body = build_template(request, context, 'students-add.html')

        return Response(request, body=body)


@AppRoute(urlpatterns, '^/students-bind/$')
class StudentsBindPage(View):
    def get(self, request: Request, *args, **kwargs):
        context = {'students': engine.get_students(), 'courses': engine.get_courses()}
        body = build_template(request, context, 'students-bind.html')

        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        if request.POST:
            student_id = request.POST.get('student_id')[0]
            course_id = request.POST.get('course_id')[0]

            student = engine.get_student_by_id(student_id)
            course = engine.get_course_by_id(course_id)

            course.add_student(student)

        context = {}
        body = build_template(request, context, 'students.html')

        return Response(request, body=body)


@AppRoute(urlpatterns, '^/api-course/$')
class CourseApi(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(request, body=JsonSerializer.save(engine.courses))


urlpatterns.extend([
    Url('^/$', IndexPage),
    Url('^/contact/$', ContactPage),
    Url('^/schedules/$', SchedulesPage),
    Url('^/courses/$', CoursePage),
    Url('^/courses-category/$', CourseCategoryPage),
    Url('^/add-category/$', CourseAddCategoryPage),
    Url('^/add-course/$', CourseAddPage),
    Url('^/copy-course/$', CourseCopyPage),
])