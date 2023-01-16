from copy import deepcopy
from uuid import uuid4

from savraska.database import Teacher, Student, Category
from savraska.utils import Subject


class UserFactory:
    """ Паттерн фабричный метод """

    user_types = {
        'teacher': Teacher,
        'student': Student
    }

    @classmethod
    def create(cls, user_type: str, name: str):
        return cls.user_types[user_type](name)


class CoursePrototype:
    """ Паттерн прототип """

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):

    def __init__(self, name, category):
        self.id = uuid4()
        self.name = name
        self.category = category
        self.students = []

        super(Course, self).__init__()

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    course_types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, course_type, name, category):
        return cls.course_types[course_type](name, category)


class Engine:
    """ Интерфейс проекта """

    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    def get_students(self):
        return self.students

    def get_courses(self):
        return self.courses

    def __get_categories_rec(self, categories, category_list, level):
        for category in categories:
            if category.categories:
                self.__get_categories_rec(category.categories, category_list, level + 2)
                category_list.append({'category': category, 'level': level, 'id': category.id})
            else:
                category_list.append({'category': category, 'level': level, 'id': category.id})

    def get_categories(self):
        category_list = []
        categories = self.categories

        self.__get_categories_rec(categories, category_list, level=1)

        category_list = category_list[::-1]
        for item in category_list:
            item['level'] = '_' * item['level']
        return category_list

    @staticmethod
    def create_user(user_type, name):
        return UserFactory.create(user_type, name)

    @staticmethod
    def create_category(name, parent_category=None):
        return Category(name, parent_category)

    @staticmethod
    def create_course(course_type, name, category) -> Course:
        course = CourseFactory.create(course_type, name, category)
        category.course_add(course)

        return course

    def get_category_by_id(self, category_id):
        for category in self.get_categories():
            if str(category['id']) == category_id:
                return category['category']
        return None

    def get_course_by_id(self, course_id: str):
        for course in self.courses:
            if str(course.id) == course_id:
                return course
        return None

    def get_student_by_id(self, student_id: str):
        for student in self.students:
            if str(student.id) == student_id:
                return student
        return None

    def get_courses_by_category(self, category):
        return  category.courses

    def add_category(self, category):
        self.categories.append(category)

    def add_course(self, course):
        self.courses.append(course)

    def add_student(self, student: Student):
        self.students.append(student)


engine = Engine()