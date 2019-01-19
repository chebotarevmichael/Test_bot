import vk
import requests
import json
import settings

session = vk.Session(access_token=settings.token)
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
        [button(label="Назад", color="primary"), button(label="Сначала", color="default")]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


def send_message(user_id, token, message, path_to_img):
    attachment = ""
    if path_to_img != "":
        r = api.photos.getMessagesUploadServer(access_token=token, peer_id=int(user_id))
        r = requests.post(r['upload_url'], files={'photo': open(path_to_img, 'rb')}).json()
        r = api.photos.saveMessagesPhoto(photo=r['photo'], server=r['server'], hash=r['hash'], access_token=token)[0]
        attachment = 'photo{}_{}'.format(r['owner_id'], r['id'])

    api.messages.send(access_token=token,
                      user_id=str(user_id),
                      message=message,
                      attachment=attachment,
                      keyboard=keyboard)

