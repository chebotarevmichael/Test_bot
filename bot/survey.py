# -*- coding: utf-8 -*-

import os.path as path

from models import db, User, Category
import settings

quest_text = []
q = []
for name in settings.categories:
    with open(path.join(settings.path, name+".txt"), 'r') as textfile:
        for line in textfile:
            q.append(line.strip())
    quest_text.append(q)
    q = []


class EndOfTest(Exception):
    pass


class Survey:
    def __init__(self, user_id):
        # get corresponding user or create it
        self.user = db.session.query(User).get(user_id)
        self.newborn = False
        if self.user is None:
            self.newborn = True
            self.user = User(user_id)
            db.session.add(self.user)
            db.session.commit()

    def cleanup(self):
        for c in self.user.categories:
            db.session.delete(c)
        db.session.delete(self.user)
        db.session.commit()

    def results(self):
        return {c.name: c.points for c in self.user.categories}

    def category(self) -> Category:
        category = db.session.query(Category).\
                              filter(Category.user == self.user).\
                              filter(Category.index == self.user.category_index).\
                              first()

        if category is None:
            index = self.user.category_index
            category = Category(user=self.user, index=index,
                                name=settings.categories[index])
            db.session.add(category)
            db.session.commit()
        return category

    def change_points(self, value):
        self.category().points += value
        db.session.commit()

    def step_question(self, backward=False):
        """Raises EndOfTest if there is no more questions"""
        category = quest_text[self.category().index]            # get list of questions for user`s current category
        step = -1 if backward else 1                            # step to forward or backward

        if (self.user.position+step == len(category)
                or self.user.position+step < 0):
            category = quest_text[self.step_category(backward).index]
        else:
            self.user.position += step
        db.session.commit()

        return category[self.user.position]

    def step_category(self, backward=False):
        if self.user.category_index == len(quest_text)-1 and not backward:
            raise EndOfTest
        if self.user.category_index == 0 and backward:
            return self.category()

        self.user.category_index += -1 if backward else 1
        quest_num = len(quest_text[self.user.category_index])
        self.user.position = quest_num-1 if backward else 0
        db.session.commit()
        return self.category()

