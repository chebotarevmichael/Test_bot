# -*- coding: utf-8 -*-
from botFlask import db
from bot.survey import Survey
from messageHandler import create_answer
db.create_all()


def process(user_id, points):
    survey = Survey(user_id)
    survey.change_points(points)
    question = survey.step_question()
    create_answer(user_id, question)


def go_back(user_id):
    question = Survey(user_id).step_question(backward=True)
    create_answer(user_id, question)

