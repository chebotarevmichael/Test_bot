import vkapi
import settings

def create_answer(user_id, message):
   token = settings.token
   vkapi.send_message(user_id, token, message[0:-1])