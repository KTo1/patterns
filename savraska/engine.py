from savraska.database import Teacher, Student, Category, Course, InteractiveCourse, RecordCourse, MapperRegistry, CourseStudent


class UserFactory:
    """ Паттерн фабричный метод """

    user_types = {
        'teacher': Teacher,
        'student': Student
    }

    @classmethod
    def create(cls, user_type: str, id:int, name: str):
        return cls.user_types[user_type](id, name)


class CourseFactory:
    course_types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, course_type: str, id_category:int, name:str):
        return cls.course_types[course_type](0, id_category, name)


class Engine:
    """ Интерфейс проекта """

    def __init__(self):
        self.data = {}

    def __get_categories_rec(self, categories, category_list, level):
        for category in categories:
            if category.categories:
                self.__get_categories_rec(category.categories, category_list, level + 2)
                category_list.append({'category': category, 'level': level, 'id': category.id})
            else:
                category_list.append({'category': category, 'level': level, 'id': category.id})

    def get_courses(self):
        return MapperRegistry.get_current_mapper('course').all()

    def get_students(self):
        return MapperRegistry.get_current_mapper('student').all()

    def get_categories(self):

        #TODO переделать на соединение

        mapper_category = MapperRegistry.get_current_mapper('category')
        mapper_courses = MapperRegistry.get_current_mapper('course')

        category_list = []
        for category in mapper_category.all():
            courses = mapper_courses.get_by_category_id(category.id)
            category_list.append({'category': category, 'level': '', 'id': category.id, 'len': len(courses)})

        return category_list

        # category_list = []
        # categories = self.categories
        #
        # self.__get_categories_rec(categories, category_list, level=1)
        #
        # category_list = category_list[::-1]
        # for item in category_list:
        #     item['level'] = '_' * item['level']
        # return category_list

    @staticmethod
    def create_user(user_type, name):
        return UserFactory.create(user_type, 0, name)

    @staticmethod
    def create_category(name, parent_category=None):
        return Category(0, parent_category, name)

    @staticmethod
    def create_course(course_type, id_category, name) -> Course:
        return CourseFactory.create(course_type, id_category, name)

    def student_bind_course(self, student, course):
        return CourseStudent(student.id, course.id)

    def get_category_by_id(self, category_id):
        return MapperRegistry.get_current_mapper('category').get(category_id)

    def get_course_by_id(self, course_id: str):
        return MapperRegistry.get_current_mapper('course').get(course_id)

    def get_courses(self):
        return MapperRegistry.get_current_mapper('course').all()

    def get_student_by_id(self, student_id: str):
        return MapperRegistry.get_current_mapper('student').get(student_id)

    def get_courses_by_category_id(self, category_id):
        return MapperRegistry.get_current_mapper('course').get_by_category_id(category_id)


engine = Engine()