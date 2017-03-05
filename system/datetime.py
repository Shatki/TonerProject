# -*- coding: utf-8 -*-
# Класс для работы с системным временем
from datetime import datetime


class SystemDateTime:
    # кодирование даты формата бэкэнда для отправики на фронтэнд
    @staticmethod
    def encode(data):
        date = data.split('-', 3)
        return date[2] + '/' + date[1] + '/' + date[0]

    # декодирование даты с фронтенда для работы с ней на бэкэнде
    @staticmethod
    def decode(data):
        date = data.split('/', 3)
        return date[2] + '-' + date[1] + '-' + date[0]

    # возвращает текущую дату для отправки на фронтэнд
    @staticmethod
    def today():
        return str(datetime.today().day) + '/' + str(datetime.today().month) + '/' + str(datetime.today().year)

    # возвращает текущую дату для бэкэнда
    @staticmethod
    def db_today():
        return datetime.today()
