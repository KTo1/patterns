from copy import deepcopy
from uuid import uuid4


class User:
    pass


class Teacher(User):
    pass


class Student(User):
    pass


class UserFactory:
    """ Паттерн фабричный метод """

    user_types = {
        'teacher': Teacher,
        'student': Student
    }

    @classmethod
    def create(cls, user_type):
        return cls.user_types[user_type]()


class CoursePrototype:
    """ Паттерн прототип """

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category


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


class Category:

    def __init__(self, name, parent_category):
        self.id = uuid4()
        self.name = name
        self.parent = parent_category
        self.courses = []

    def course_add(self, course):
        self.courses.append(course)

    def course_count(self):
        result = len(self.courses)
        if self.parent:
            result += self.parent.course_count()
        return result


class Engine:
    """ Интерфейс проекта """

    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(user_type):
        return UserFactory.create(user_type)

    @staticmethod
    def create_category(name, parent_category=None):
        return Category(name, parent_category)

    @staticmethod
    def create_course(course_type, name, category):
        course = CourseFactory.create(course_type, name, category)
        category.course_add(course)

        return course

    def add_category(self, category):
        self.categories.append(category)


engine = Engine()