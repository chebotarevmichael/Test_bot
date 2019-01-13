# -*- coding: utf-8 -*-
from bot.survey import Survey, EndOfTest
from messageHandler import create_answer
import settings


def touch(user_id, send=True):
    "Init a survey or do nothing"
    survey = Survey(user_id)
    if survey.newborn:
        return process(user_id, send=send)  # ask the first question


def process(user_id, points=0, send=True):
    survey = Survey(user_id)
    survey.change_points(points)
    try:
        text = survey.step_question()                   # next question
        attachment = ''
    except EndOfTest:
        text = str(survey.results())  # TODO: nice results
        attachment = 'photo{}_{}'.format(settings.group_id, settings.photo_id)
        survey.cleanup()
    if send:
        create_answer(user_id, text, attachment)
    return text, survey.user


def go_back(user_id, send=True):
    survey = Survey(user_id)
    question = survey.step_question(backward=True)
    if send:
        create_answer(user_id, question)
    return question, survey.user

