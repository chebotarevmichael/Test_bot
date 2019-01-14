import os.path as os_path

# Community access token for vk
token = None

# Callback API confirmation code
confirmation_token = None

# Location of categoryname.txt files containing questions
path = "mysite/bot/question"

# VK group and Photo id
group_id = -176434873                   # negative number
photo_id = 456239017

categories = ["economic", "social", "national",
              "traditional", "revolution", "ecological",
              "individualism", "scientism"]

# init list of questions
quest_text = []
q = []
for name in categories:
    with open(os_path.join(path, name + ".txt"), 'r') as textfile:
        for line in textfile:
            q.append(line.strip())
    quest_text.append(q)
    q = []


# Points user gets choosing answer on bot keyboard
body_to_ans = {
    "Полностью согласен": 1,
    "Скорее согласен": 0.5,
    "Не знаю | Смешанно": 0,
    "Скорее не согласен": -0.5,
    "Полностью не согласен": -1,
}

back_label = "Назад"
