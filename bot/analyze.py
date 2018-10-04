## -*- coding: utf-8 -*-
from messageHandler import create_answer
import sqlite3

maximum = {
    0: 10,
    1: 50,
    2: 11,
    3: 13,
    4: 11,
    5: 8,
    6: 7
}

num_to_group = {
    0: 'economic_point',
    1: 'social_point',
    2: 'national_point',
    3: 'traditional_point',
    4: 'revolution_point',
    5: 'ecological_point'
}


def main(name, points, is_back):
    central = open('mysite/bot/question/central.txt')
    ecological = open('mysite/bot/question/ecological.txt')
    economic = open('mysite/bot/question/economic.txt')
    national = open('mysite/bot/question/national.txt')
    revolution = open('mysite/bot/question/revolution.txt')
    social = open('mysite/bot/question/social.txt')
    traditional = open('mysite/bot/question/traditional.txt')
    quest_text = [economic, social, central, national, traditional, revolution, ecological]

    def is_new(name):
        try:
            cursor.execute("""SELECT * FROM `main` WHERE Name={}""".format(name))
        except sqlite3.OperationalError:
            return True
        else:
            return False

    def update(name, points):  # Обновляет данные/загружает в логги
        cursor.execute("""SELECT test_group, quest_number FROM `main` WHERE Name = {}""".format(name))
        sqldata = cursor.fetchone()
        test_group, quest_number = num_to_group.get(sqldata[0]), sqldata[1]  # По номеру группы получаем саму группу
        if quest_number + 1 != maximum.get(test_group):  # Макс. число вопросов достигнуто
            quest_number += 1
        elif (quest_number == maximum.get(test_group)) and (test_group == 6):
            test_group = 0
            quest_number = 0
        else:
            test_group += 1
            quest_number = 0
        sql = """UPDATE `main` SET {test}={points}, quest_number = {quest_number} WHERE Name={name}""".format(
            test=test_group, name=name, points=points, quest_number=quest_number)
        cursor.execute(sql)
        conn.commit()
        # Теперь загрузка в логи
        cursor.execute("""insert into `logs` values ({name}, {test_group}, {quest}, {res})""".format(
            name=name, test_group=test_group, quest=quest_number, res=points))
        conn.commit()

    def create(name):  # Создает нового пользователя в main
        cursor.execute(""" insert into `main` values ({}, 0, 0, 0, 0, 0, 0, 0, 0)  """.format(name))
        conn.commit()

    def find_str(name):  # Поиск номера вопроса
        cursor.execute(""" SELECT test_group, quest_number FROM `main` WHERE Name={}""".format(name))
        sqldata = cursor.fetchone()
        return sqldata[0], sqldata[1]

    def back_quest(name):  # Если нужно уйти на прошлый вопрос
        cursor.execute("""SELECT test_group, quest_number FROM `main` WHERE NAME={}""".format(name))
        sqldata = cursor.fetchone()
        cursor.execute("""SELECT point_diff FROM `logs` WHERE NAME={} AND test_group ={} AND quest_number = {}""".
                       format(name, sqldata[0], sqldata[1]))
        sqldata[3] = cursor.fetchone()  # 0 - test_group, 1 - quest_number, 3 - point_diff, 4 - test
        if sqldata[1] != 0:  # Вопросы начинаются с нуля, проверка на 0
            sqldata[1] -= 1
        elif (sqldata[1] == 0) and (sqldata[0] == 0):
            pass
        else:
            sqldata[0] -= 1
            sqldata[1] = maximum.get(sqldata[0]) - 1
        sqldata[4] = num_to_group.get(sqldata[0])
        cursor.execute("""UPDATE `main` SET test_group = {test_group}, quest_number = {quest_number},
                          {test} = {res_back}""".format(test_group=sqldata[0], quest_number=sqldata[1],
                                                        test=sqldata[4], res_back=sqldata[3]))
        conn.commit()

    def delete(inp):  # Удаляет пользователя
        cursor.execute(""" DELETE FROM `main` WHERE Name={}""".format(inp))
        conn.commit()

    def give_question(quest_text, quest_list, quest_line):
        used_list = quest_text[quest_list]
        for i, line in enumerate(used_list):
            if i == quest_line:
                create_answer(name, line[:-2])
            elif i > quest_line:
                break

    conn = sqlite3.connect("new.db")
    cursor = conn.cursor()

    if not is_back and not is_new:
        update(name, points)
        give_question(quest_text, find_str(name))
    elif is_new:
        create(name)
    else:
        back_quest(name)


if __name__ == '__main__':
    main(input(), input(), False)


