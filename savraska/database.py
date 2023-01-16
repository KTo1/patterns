from threading import local
from uuid import uuid4

from savraska.exceptions import RecordNotFoundException, DbCommitException, DbDeleteException, DbUpdateException
from sqlite3 import connect


connection = connect('database.sqlite', check_same_thread=False)


class UnitOfWork:
    current = local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.del_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_del(self, obj):
        self.del_objects.append(obj)

    def set_mapper_registry(self, MapperRegistry):
        self.mr = MapperRegistry

    def insert(self):
        for elem in self.new_objects:
            self.mr.get_mapper(elem).insert(elem)

    def update(self):
        for elem in self.dirty_objects:
            self.mr.get_mapper(elem).update(elem)

    def delete(self):
        for elem in self.del_objects:
            self.mr.get_mapper(elem).delete(elem)

    def commit(self):
        self.insert()
        self.update()
        self.delete()

        self.new_objects.clear()
        self.dirty_objects.clear()
        self.del_objects.clear()

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_update(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_delete(self):
        UnitOfWork.get_current().register_del(self)


class User:
    def __init__(self, name: str):
        self.id = uuid4()
        self.name = name


class Teacher(User):
    pass


class Student(User, DomainObject):
    def __init__(self, name: str):
        super(Student, self).__init__(name)
        self.courses = []


class Category:

    def __init__(self, name, parent_category):
        self.id = uuid4()
        self.name = name
        self.parent = parent_category
        self.courses = []
        self.categories = []
        if parent_category:
            parent_category.categories.append(self)

    def course_add(self, course):
        self.courses.append(course)

    def course_count(self):
        result = len(self.courses)
        if self.parent:
            result += self.parent.course_count()
        return result

    def __str__(self):
        return f'{self.name}: {self.id}'


class BaseMapper:
    """ Базовый маппер """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'some_table'

    def all(self):
        pass

    def get(self, id):
        pass

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f'UPDATE {self.tablename} SET name=? WHERE id=?'

        self.cursor.execute(statement, (obj.id, obj.name))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CategoryMapper(BaseMapper):
    """ Маппер категорий """

    def __init__(self, connection):
        super(CategoryMapper, self).__init__(connection)
        self.tablename = 'categories'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, parent_id, name = item
            category = Category(name, parent_id)
            category.id = id
            result.append(category)

        return result

    def get(self, id):
        statement = f'SELECT id, name FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')


class StudentMapper(BaseMapper):
    """ Маппер студентов """

    def __init__(self, connection):
        super(StudentMapper, self).__init__(connection)
        self.tablename = 'students'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)

        return result

    def get(self, id):
        statement = f'SELECT id, name FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

class MapperRegistry:

    mappers = {
        'student': StudentMapper,
        'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Student):

            return StudentMapper(connection)

        if isinstance(obj, Category):

            return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
