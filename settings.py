# Community access token for vk
token = None

# Callback API confirmation code
confirmation_token = None

# Location of categoryname.txt files containing questions
path = "mysite/bot/question"

categories = ["economic", "social", "national",
              "traditional", "revolution", "ecological"]

# Points user gets choosing answer on bot keyboard
body_to_ans = {
    "Полностью согласен": 1,
    "Скорее согласен": 0.5,
    "Не знаю | Смешанно": 0,
    "Скорее не согласен": -0.5,
    "Полностью не согласен": -1,
}

back_label = "Назад"
