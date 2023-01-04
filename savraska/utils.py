import os
import json

from datetime import datetime
from typing import List


# region Поведенческий паттерн наблюдатель
# Subject - то за чем наблюдают (сейчас курсы)
# Observer - те кто наблюдают

class Subject:
    def __init__(self):
        self.observers: List[Observer] = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for item in self.observers:
            item.update(subject=self)


class Observer:
    def update(self, subject: Subject):
        pass


class SMSNotifier(Observer):
    def update(self, subject: Subject):
        print('SMS -> к нам присоединился ,)', subject.students[-1].name)


class EMAILNotifier(Observer):
    def update(self, subject: Subject):
        print('EMAIL -> к нам присоединился ,)', subject.students[-1].name)


# endregion


class JsonAdapter:
    def __init__(self, elem):
        self.elem = elem

    def to_json(self):
        return json.dumps({'name': self.elem.name}, ensure_ascii=False, sort_keys=True, indent=4)


class JsonSerializer:
    """ Сериализатор JSON """

    @staticmethod
    def save(obj):
        if isinstance(obj, list):
            return json.dumps([JsonAdapter(elem).to_json() for elem in obj], ensure_ascii=False, sort_keys=True, indent=4)
        else:
            return json.dumps(JsonAdapter(obj).to_json(), ensure_ascii=False, sort_keys=True, indent=4)

    @staticmethod
    def load(data):
        return json.loads(data)

class EMail:
    """ Класс для работы с почтой """

    def __init__(self, name: str, address: str, subject: str, message: str):
        self.__name = name
        self.__address = address
        self.__subject = subject
        self.__message = message
        self.__mail_dir = 'mail'

    def send(self, to_file: bool = True):
        if to_file:
            framework_dir = os.path.dirname(os.path.abspath(__file__))
            file_name = f'{self.__address}@{datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}.json'
            full_file_name = os.path.join(framework_dir, self.__mail_dir, file_name)

            message = {
                'Имя': self.__name,
                'Адрес': self.__address,
                'Тема': self.__subject,
                'Сообщение': self.__message
            }

            with open(full_file_name, 'w', encoding='utf-8') as f:
                json.dump(message, f, indent=4, ensure_ascii=False)
