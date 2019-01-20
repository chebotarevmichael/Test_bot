import os.path as os_path

# Community access token for vk
token = None

# Callback API confirmation code
confirmation_token = None

# Location of categoryname.txt files containing questions
path_fonts = "mysite/bot/fonts"
path_images = "mysite/bot/images"
path_question = "mysite/bot/question"

# Buttons name
btn_absolutely_yes = "Полностью согласен"
btn_probably_yes = "Скорее согласен"
btn_idk = "Не знаю | Смешанно"                      # idk = i don`t know
btn_probably_no = "Скорее не согласен"
btn_absolutely_no = "Полностью не согласен"
btn_back = "Назад"
btn_restart = "Сначала"

# Categories
categories = {
    "economic": [True, 0, 0, "Экономика"],           # True/False - to be inversed or not to be
    "social": [False, 0, 1, "Социальная сфера"],     # 0 - number of questions in category (i will be inited below)
    "national": [True, 0, 2, "Национализм"],         # 0,1,2,...7 - id of categories, therefore map has not indexes
    "central": [False, 0, 3, "Централизация"],       # "Экономика" - name which user will see
    "revolution": [True, 0, 4, "Революционность"],
    "ecological": [False, 0, 5, "Экология"],
    "individualism": [True, 0, 6, "Индивидуализм"],
    "scientism": [False, 0, 7, "Сциентизм"]
}

# Init list of questions
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
    btn_absolutely_yes: 1,
    btn_probably_yes: 0.5,
    btn_idk: 0,
    btn_probably_no: -0.5,
    btn_absolutely_no: -1,
}
