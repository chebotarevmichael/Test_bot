from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy

import settings
from bot.analyze import main

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return settings.confirmation_token
    elif data['type'] == 'message_new':
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
        main(user_id, body_to_ans.get(body), bool(body != "Назад"))
        return 'ok'

db.create_all()
