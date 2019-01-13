import vkapi
import settings


def create_answer(user_id, message, attachment=""):
    vkapi.send_message(user_id, settings.token, message[0:-1], attachment)
