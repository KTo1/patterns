import os
import logging

from datetime import datetime


savraska_log = logging.getLogger('savraska.main')
formatter = logging.Formatter("<%(asctime)s> <%(levelname)s> <%(module)s> <%(message)s>")

logs_dir = 'logs'

file_name = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(file_name, logs_dir)
if not os.path.isdir(file_name):
     os.mkdir(file_name)

file_name = os.path.join(file_name, 'savraska.log')

file_hand = logging.FileHandler(file_name, encoding='utf-8')
file_hand.setLevel(logging.DEBUG)
file_hand.setFormatter(formatter)

if not savraska_log.handlers:
    savraska_log.addHandler(file_hand)

savraska_log.setLevel(logging.DEBUG)


# region Порождающий паттерн синглтон
class SingletonByName(type):
    def __init__(self, name, bases, attr, **kwargs):
        super(SingletonByName, self).__init__(name, bases, attr)
        self.__instance = {}

    def __call__(self, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if not name in self.__instance:
            self.__instance[name] = super(SingletonByName, self).__call__(*args, **kwargs)

        return self.__instance[name]

# endregion


# region Поведенческий паттерн стратегия
# выбираем нужный райтер в зависимости от обстоятельств

class ConsoleWriter:
    def write(self, text):
        print(text)

class FileWriter:
    def __init__(self):
        self.file_name = os.path.join(os.path.dirname(__file__), 'logs\log.txt')

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(text)

# endregion

class Loger(metaclass=SingletonByName):
    def __init__(self, name, writer=ConsoleWriter):
        self.name = name
        self.writer = writer

    def write(self, text):
        text_to_log = f'{str(datetime.now())}: {text}'
        self.writer.write(text_to_log)

