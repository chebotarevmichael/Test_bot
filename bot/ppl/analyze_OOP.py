# Текстовый файл с данными должен выглядить так:
# id0
# "Номер группы вопросов" "Номер вопроса"
# "Кол-во баллов за группу вопросов" * 7 (Семь групп вопросов)
# "Сохраненные ответы на вопросы"


class Person:
    def __init__(self, name, is_created):  # где name - user_id
        self.name = name
        if is_created:  # Инициирование прям нового аккаунта
            with open("{}.txt".format(self.name), "r") as self.file_name:
                self.is_First_quest = False
                self.name = self.file_name.readline()[:-1]
                self.quest_list_number = self.file_name.readline().split(" ")  # самый глупый способ "собрать"
                self.quest_number = self.quest_list_number[1]                  # данные со строки
                self.quest_list_number = self.quest_list_number[0]
                self.points = self.file_name.readline()[:-2].split(" ")
                self.answers = self.file_name.readline()[:-2].split(" ")
                self.pointsres = []
            self.file_name.close()
        else:
            self.is_First_quest = True
            self.quest_list_number, self.quest_number = 0, 0
            self.points = [0, 0, 0, 0, 0, 0, 0]
            self.answers = [0]
            with open("{}.txt".format(self.name), "w") as self.file_name:
                self.file_name.write(self.name + "\n0 0\n" + "0 " * 6 + "0")
            self.file_name.close()

    def rewrite(self):  # Для сохранения данных, используется только внутри класса
        with open('{}.txt'.format(self.name), 'w') as self.file_name:
            self.file_name.write(self.name + "\n" + str(self.quest_list_number) + " " + str(self.quest_number) + "\n" +
                                 " ".join(str(self.points)) + "\n" + " ".join(str(self.answers)))
        self.file_name.close()

    def set_ans(self, answer_point):
        self.points[self.quest_list_number] += answer_point
        self.answers.append(answer_point)
        self.quest_number += 1
        self.rewrite()

    def get_quest(self):  # Возращает номер группы вопросов и сам номер вопроса в группе
        return int(self.quest_list_number), int(self.quest_number)

    def lvl_up(self):  # Меняет группу вопросов на следующий
        self.quest_list_number += 1
        self.quest_number = 0
        self.rewrite()

    def back(self, max_dict):  # Возрат к старому вопросу + исправление последнего ответа
        self.points[self.quest_list_number] -= self.answers[-1]
        self.answers.pop()
        if self.quest_number > 0:
            self.quest_number -= 1
        elif self.quest_list_number > 0:
            self.quest_list_number -= 1
            self.quest_number = max_dict.get(self.quest_list_number) - 1
        self.rewrite()

    def get_first_quest_status(self):
        return self.is_First_quest

    def showres(self, max_dict):  # Заканчиваем тест, скидываем данные
        self.is_First_quest = True
        self.quest_list_number, self.quest_number = 0, 0
        self.answers = [0]
        self.points = [0, 0, 0, 0, 0, 0, 0]
        with open("{}.txt".format(self.name), "w") as self.file_name:
            self.file_name.write(self.name + "\n0\n" + "0 " * 6 + "0")
        self.file_name.close()
        for i in range(7):
            self.pointsres[i] = self.points[i] / max_dict.get(i) * 100
        return "economic - {}%\nsocial - {}%\ncentral - {}%\nnational - {}%\ntraditional - []%\n revolution - []%\n" \
               "ecological - []%".format(self.pointsres[0], self.pointsres[1], self.pointsres[2], self.pointsres[3],
                                         self.pointsres[4], self.pointsres[5], self.pointsres[6])
