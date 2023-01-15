from threading import local
from engine import Student
from savraska.exceptions import RecordNotFoundException, DbCommitException, DbDeleteException, DbUpdateException
from sqlite3 import connect


connection = connect('database.sqlite')


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

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

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f'UPDATE {self.tablename} SET name=? WHERE id=?'

        self.cursor.execute(statement, (obj.name, obj.id))
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
        for elem in self.new_objects:
            self.mr.get_mapper(elem).update(elem)

    def delete(self):
        for elem in self.new_objects:
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

