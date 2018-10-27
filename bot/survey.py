# -*- coding: utf-8 -*-

import os.path as path

from models import db, User, Category, HistoryItem
import settings

quest_text = [open(path.join(settings.path, name+".txt")).readlines()
              for name in settings.categories]


class EndOfTest(Exception):
    pass


class Survey:
    def __init__(self, user_id):
        # get corresponding user or create it
        self.user = db.session.query(User).get(user_id)
        if self.user is None:
            self.user = User(user_id)
            db.session.add(self.user)
            db.session.commit()

    def cleanup(self):
        for c in self.user.categories:
            for h in c.history:
                db.session.delete(h)
            db.session.delete(c)
        db.session.delete(self.user)
        db.session.commit()

    def category(self):
        category = db.session.query(Category).\
                              filter(Category.user==self.user).\
                              filter(Category.index==self.user.category_index).\
                              first()

        if category is None:
            category = Category(user=self.user, index=0,
                                name=settings.categories[0])
            db.session.add(category)
            db.session.commit()
        return category

    def history_item(self):
        "History is used to get points for given category and position"
        return db.session.query(HistoryItem).\
                          filter(HistoryItem.category==self.category()).\
                          filter(HistoryItem.position==self.user.position).\
                          first()

    def change_points(self, value):
        self.category().points += value
        db.session.commit()

    def step_question(self, backward=False):
        "Raises EndOfTest if there is no more questions"
        if backward:
            step = -1
            self.restore_points()
        else:
            step = 1
            self.log_to_history()  # save previous state

        category = quest_text[self.category().index]

        if (self.user.position+step == len(category)
                or self.user.position+step < 0):
            category = quest_text[self.step_category(backward)]
        else:
            self.user.position += step

        db.session.commit()
        return category[self.user.position]

    def restore_points(self):
        item = self.history_item()
        category = self.category()
        category.points = item.points

    def log_to_history(self):
        item = self.history_item()
        category = self.category()
        if item is None:
            item = HistoryItem(category=category, position=self.user.position)
            db.session.add(item)
        item.points = category.points
        db.session.commit()

    def step_category(self, backward=False):
        if self.user.category_index == len(quest_text)-1 and not backward:
            raise EndOfTest
        if self.user.category_index == 0 and backward:
            return

        self.user.category_index += -1 if backward else 1
        self.user.position = len()-1 if backward else 0
        return self.category()

