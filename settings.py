import os.path as os_path

# Community access token for vk
token = None

# Callback API confirmation code
confirmation_token = None

# Location of categoryname.txt files containing questions
path_fonts = "mysite/bot/fonts"
path_images = "mysite/bot/images"
path_question = "mysite/bot/question"

# VK group and Photo id
group_id = -176434873                   # negative number
photo_id = 456239017

categories = {
    "economic": [True, 0, 0],           # True/False - to be inversed or not to be
    "social": [False, 0, 1],            # 0 - number of questions in category (i will be inited below)
    "national": [True, 0, 2],           # 0,1,2,...7 - id of categories, therefore map has not indexes
    "central": [False, 0, 3],
    "revolution": [True, 0, 4],
    "ecological": [False, 0, 5],
    "individualism": [True, 0, 6],
    "scientism": [False, 0, 7]
}

# init list of questions
quest_text = []
q = []
for name in categories.keys():
    with open(os_path.join(path_question, name + ".txt"), 'r', encoding='utf-8') as textfile:
        for line in textfile:
            q.append(line.strip())
    quest_text.append(q)
    categories[name][1] = len(q)
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
