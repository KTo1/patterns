import os
import json

from datetime import datetime


class EMail:
    """ Класс для работы с почтой"""

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
