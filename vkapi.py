import vk
import json

session = vk.Session()
api = vk.API(session, v=5.80)


def button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

keyboard = {
    "one_time": False,
    "buttons": [

    [button(label="Полностью согласен", color="positive")],
    [button(label="Скорее согласен", color="positive")],
    [button(label="Не знаю | Смешанно", color="primary")],
    [button(label="Скорее не согласен", color="negative")],
    [button(label="Полностью не согласен", color="negative")],
    [button(label="Назад", color="primary")]

    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

def send_message(user_id, token, message):
    api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment="", keyboard = keyboard)
