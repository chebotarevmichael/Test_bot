# -*- coding: utf-8 -*-
from bot.survey import Survey, EndOfTest
from messageHandler import create_answer
import settings
from Artist import Artist


def touch(user_id, send=True):
    "Init a survey or do nothing"
    survey = Survey(user_id)
    if survey.newborn:
        return process(user_id, send=send)  # ask the first question


def process(user_id, points=0, send=True):
    artist = None
    survey = Survey(user_id)
    survey.change_points(points)
    try:
        text = survey.step_question()                   # next question
        path_to_img = ''
    except EndOfTest:
        create_answer(user_id, "Результат обрабатывается... ждите.")
        text = ""
        artist = Artist(user_id, survey.results())           # wait 4 seconds, hard computing
        path_to_img = artist.get_path_to_img()
        survey.cleanup()

    if send:
        create_answer(user_id, text, path_to_img)
        if artist is not None:
            artist.__del__()
    return text, survey.user


def go_back(user_id, send=True):
    survey = Survey(user_id)
    question = survey.step_question(backward=True)
    if send:
        create_answer(user_id, question)
    return question, survey.user

