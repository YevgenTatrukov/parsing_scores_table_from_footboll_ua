from bs4 import BeautifulSoup
import requests
import json
import csv


"""Збираємо данні про сайт який будемо парсити"""
# url = "https://football.ua/"
#
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

}

""" Отримуємо необхідну сторінку"""
# req = requests.get(url, headers=headers)
# src = req.text

""" Зберігаємо данні з сторінки в html файлі"""
# with open("index.html", "w") as file:
#     file.write(src)

""" Відкриваємо збережений html файл та надалі працюємо з ним"""
# with open("index.html") as file:
#     src = file.read()

""" Передаємо усі данні з файлу бібліотеці BeautifulSoup, використовуючи бібліотеку lxml яка оброблює html"""
# soup = BeautifulSoup(src, "lxml")
# # all_league_hrefs = soup.find_all("li")
# all_hrefs = soup.find_all("a")

"""Створюємо список країн таблиці яких нас цікавить, та по яким ми будемо шукати посилання"""
# all_country = ["Україна", "Англія", "Німеччина", "Іспанія", "Італія",
#                "Нідерланди", "Португалія", "Туреччина", "Франція"]
#
"""Створюємо словник для зберігання необхідних нас посилань"""
# all_country_dict = {}
#
"""Шукаємо необхідні нам країни, посилання на їх таблиці та додаємо данні до словника"""
# for country in all_country:
#     for item in all_hrefs:
#         if (len(item.get("href")) < 40) and (len(item.get("href")) > 20) and item.text == country:
#             item_text = item.text
#             item_href = item.get("href")
#             item_href = item_href[:len(item_href) - len('.html')]+'/table.html'
#             all_country_dict[item_text] = item_href
#
"""Створюємо json файл в якій збережемо наш словник с країною та посиланням
# (indent=4 - відступи від краю, ensure_ascii=False- щоб не було проблем з кирилицею)"""
# with open("all_country_dict.json", 'w') as file:
#     json.dump(all_country_dict, file, indent=2, ensure_ascii=False)


"""Відкриваємо json файл та працюємо з ним"""
with open("all_country_dict.json") as file:
    all_scores = json.load(file)

"""За допомогою цикла пробігаємося по json файлу та збираємо потрібну нам інформацію з посилань json файлу"""
count = 0
for scores_name, scores_href in all_scores.items():
    if count == 0:
        req = requests.get(url=scores_href, headers=headers)
        src = req.text

        """Створюємо html файли сторінок з посилань json файлу"""
        # with open(f"data/{count}_{scores_name}.html", "w") as file:
        #     file.write(src)

        """Відкриваємо html файл та працюємо з ним"""
        # with open(f"data/{count}_{scores_name}.html") as file:
        #     src = file.read()

        """ Передаємо усі данні з файлу бібліотеці BeautifulSoup, використовуючи бібліотеку lxml яка оброблює html"""
        soup = BeautifulSoup(src, "lxml")

        """ Знаходимо всі назви стовбців таблиці та зберігаємо їх в змінних"""
        place = soup.find(class_="main-tournament-table").find(class_="num").text
        date = soup.find(class_="main-tournament-table").find(class_="date").text
        changed_date_str_digit = ''
        changed_date_str_digit

        for item in date:
            if item.isdigit() or item.isalpha():
                changed_date_str_digit += item
        games = soup.find(class_="main-tournament-table").find(class_="games").text
        win = soup.find(class_="main-tournament-table").find(class_="win").text
        draw = soup.find(class_="main-tournament-table").find(class_="draw").text
        lose = soup.find(class_="main-tournament-table").find(class_="lose").text
        goal = soup.find(class_="main-tournament-table").find(class_="goal").text
        miss = soup.find(class_="main-tournament-table").find(class_="miss").text
        diff = soup.find(class_="main-tournament-table").find(class_="diff").text
        score = soup.find(class_="main-tournament-table").find(class_="score").text

        """ Збираємо усі стовбці у файл csv"""
        with open(f"data/{count}_{scores_name}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    place,
                    changed_date_str_digit,
                    games,
                    win,
                    draw,
                    lose,
                    goal,
                    miss,
                    diff,
                    score
                )
            )
        """ Знаходимо всі назви рядків таблиці та зберігаємо їх в змінних"""
        # teem_place = soup.find(class_="main-tournament-table").find_all(class_="num")
        # title_teem = teem_place[1:]
        # teem_name = soup.find(class_="main-tournament-table").find_all('a')
        # games = soup.find(class_="main-tournament-table").find_all(class_="games")
        # title_games = games[1:]
        # win = soup.find(class_="main-tournament-table").find_all(class_="win")
        # title_win = win[1:]
        # draw = soup.find(class_="main-tournament-table").find_all(class_="draw")
        # title_draw = draw[1:]
        # lose = soup.find(class_="main-tournament-table").find_all(class_="lose")
        # title_lose = lose[1:]
        # goal = soup.find(class_="main-tournament-table").find_all(class_="goal")
        # title_goal = goal[1:]
        # miss = soup.find(class_="main-tournament-table").find_all(class_="miss")
        # title_miss = miss[1:]
        # diff = soup.find(class_="main-tournament-table").find_all(class_="diff")
        # title_diff = diff[1:]
        # score = soup.find(class_="main-tournament-table").find_all(class_="score")
        # title_score = score[1:]
        #
        # list_for_all_teem = []
        #
        # for i_elem in title_teem:
        #     for k_elem in i_elem:
        #         if k_elem.isdigit():
        #             title_teem = k_elem
        #
        # for i in teem_name:
        #     title = i.text
        #
        # for i_elem in title_games:
        #     for k_elem in i_elem:
        #         if k_elem.isdigit():
        #             title_games = k_elem
        #
        # for i_elem in title_win :
        #     for k_elem in i_elem:
        #         if k_elem.isdigit():
        #             title_win = k_elem
        #
        # for i_elem in title_draw:
        #     for k_elem in i_elem:
        #         if k_elem.isdigit():
        #             title_draw = k_elem
        #
        # for i_elem in title_lose:
        #     for k_elem in i_elem:
        #         if k_elem.isdigit():
        #             title_lose = k_elem
        #
        # for i_elem in title_goal:
        #     for k_elem in i_elem:
        #         if k_elem.isdigit():
        #             title_goal = k_elem
        #
        # for i_elem in title_miss:
        #     for k_elem in i_elem:
        #         if k_elem.isdigit():
        #             title_miss = k_elem
        #
        # for i_elem in title_diff:
        #     for k_elem in i_elem:
        #         if k_elem.isdigit():
        #             title_diff = k_elem
        #
        # for i_elem in title_score:
        #     for k_elem in i_elem:
        #         if k_elem.isdigit():
        #             title_score = k_elem

        place_1 = soup.find(class_="main-tournament-table").find_all("tr")
        title = place_1[1:]
        print(title)

        count += 1
