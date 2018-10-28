from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
db = SQLAlchemy(app)

import settings
from bot import analyze


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return settings.confirmation_token
    if data['type'] == 'message_new':
        data = data['object']
        user_id = data['from_id']
        body = data['text']

        points = settings.body_to_ans.get(body)
        if body == settings.back_label:
            analyze.go_back(user_id)
        elif points is not None:
            analyze.process(user_id, points)
        else:
            analyze.touch(user_id)

        return 'ok'

