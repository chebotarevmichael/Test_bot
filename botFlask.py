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
        body_to_ans = {
            "Полностью согласен": 1,
            "Скорее согласен": 0.5,
            "Не знаю | Смешанно": 0,
            "Скорее не согласен": -0.5,
            "Полностью не согласен": -1,
            "Назад": 0
        }

        if body == "Назад":
            analyze.go_back(user_id)
        else:
            analyze.process(user_id, body_to_ans[body])

        return 'ok'

if __name__ == "__main__": analyze.process(1,1)
