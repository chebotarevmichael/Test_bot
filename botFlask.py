
from flask import Flask, request, json
from settings import confirmation_token
from bot.analyze import main
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
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
        main(user_id, body_to_ans.get(body), False if body == "Назад" else True)
        return 'ok'