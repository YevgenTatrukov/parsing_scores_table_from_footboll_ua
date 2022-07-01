import random

from bs4 import BeautifulSoup
import requests
import json
import csv
import time


""" Збираємо данні про сайт який будемо парсити """
# url = "https://football.ua/"
#
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

}

""" Отримуємо необхідну сторінку """
# req = requests.get(url, headers=headers)
# src = req.text

""" Зберігаємо данні з сторінки в html файлі """
# with open("index.html", "w") as file:
#     file.write(src)

""" Відкриваємо збережений html файл та надалі працюємо з ним """
# with open("index.html") as file:
#     src = file.read()

""" Передаємо усі данні з файлу бібліотеці BeautifulSoup, використовуючи бібліотеку lxml яка оброблює html """
# soup = BeautifulSoup(src, "lxml")
# # all_league_hrefs = soup.find_all("li")
# all_hrefs = soup.find_all("a")

""" Створюємо список країн таблиці яких нас цікавить, та по яким ми будемо шукати посилання """
# all_country = ["Україна", "Англія", "Німеччина", "Іспанія", "Італія",
#                "Нідерланди", "Португалія", "Туреччина", "Франція"]
#
""" Створюємо словник для зберігання необхідних нас посилань """
# all_country_dict = {}
#
""" Шукаємо необхідні нам країни, посилання на їх таблиці та додаємо данні до словника """
# for country in all_country:
#     for item in all_hrefs:
#         if (len(item.get("href")) < 40) and (len(item.get("href")) > 20) and item.text == country:
#             item_text = item.text
#             item_href = item.get("href")
#             item_href = item_href[:len(item_href) - len('.html')]+'/table.html'
#             all_country_dict[item_text] = item_href
#
""" Створюємо json файл в якій збережемо наш словник с країною та посиланням
(indent=2 - відступи від краю, ensure_ascii=False- щоб не було проблем з кирилицею) """
# with open("all_country_dict.json", 'w') as file:
#     json.dump(all_country_dict, file, indent=2, ensure_ascii=False)


""" Відкриваємо json файл та працюємо з ним """
with open("all_country_dict.json") as file:
    all_scores = json.load(file)


iteration_count = int(len(all_scores)) - 1
count = 0
print(f"Усього ліг: {iteration_count}")

""" За допомогою цикла пробігаємося по json файлу та збираємо потрібну нам інформацію з посилань json файлу """
for scores_name, scores_href in all_scores.items():

    req = requests.get(url=scores_href, headers=headers)
    src = req.text

    """ Створюємо html файли сторінок з посилань json файлу """
    # with open(f"data/{count + 1}_{scores_name}.html", "w") as file:
    #     file.write(src)

    """ Відкриваємо html файл та працюємо з ним """
    # with open(f"data/{count + 1}_{scores_name}.html") as file:
    #     src = file.read()

    """ Передаємо усі данні з файлу бібліотеці BeautifulSoup, використовуючи бібліотеку lxml яка оброблює html """
    soup = BeautifulSoup(src, "lxml")

    """ Знаходимо всі назви стовбців таблиці та зберігаємо їх в змінних """
    all_table = soup.find(class_="main-tournament-table").find_all("tr")
    all_table_title = all_table[0]
    place = all_table_title.find(class_='num').text
    date = ''
    for item in all_table_title.find(class_='date').text:
        if item.isdigit() or item.isalpha():
            date += item
    games = all_table_title.find(class_='games').text
    win = all_table_title.find(class_='win').text
    draw = all_table_title.find(class_='draw').text
    lose = all_table_title.find(class_='lose').text
    goal = all_table_title.find(class_='goal').text
    miss = all_table_title.find(class_='miss').text
    diff = all_table_title.find(class_='diff').text
    score = all_table_title.find(class_='score').text

    """ Збираємо усі стовбці у файл csv """
    with open(f"data/{count + 1}_{scores_name}.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                place,
                date,
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

    """ Знаходимо всі назви рядків таблиці та зберігаємо їх в змінних """
    all_table_body = all_table[1:]

    """ Створюємо список куди додамо ще один словник для запису даних з таблиці """
    table_info = []

    """ Ітеріруємо данні з таблиці """
    for item in all_table_body:
        all_tds = item.find_all_next('td')

        place = all_tds[0].text
        teem = all_tds[2].find('a').text
        games = all_tds[3].text
        win = all_tds[4].text
        draw = all_tds[5].text
        lose = all_tds[6].text
        goal = all_tds[7].text
        miss = all_tds[8].text
        diff = all_tds[9].text
        score = all_tds[10].text

        """ Дозаписуємо отриманні данні у вже існуючий csv файл """
        with open(f"data/{count + 1}_{scores_name}.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    place,
                    teem,
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

        """ Додаємо до списку словник для створення json файлу """
        table_info.append(
            {
                "Place": place,
                "Teem ": teem,
                "Games": games,
                "Win": win,
                "Draw": draw,
                "Lose": lose,
                "Goal": goal,
                "Miss": miss,
                "Diff": diff,
                "Score": score
            }
        )

    """ Записуємо список до json файлу """
    with open(f"data/{count + 1}_{scores_name}.json", "a") as file:
        json.dump(table_info, file, indent=2, ensure_ascii=False)

    """ Залишок коду """
    count += 1
    print(f"# Ітерація {count}. {scores_name} записан...")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Робота завершена")
        break
    print(f"Залишилось ліг: {iteration_count}")
    time.sleep(random.randrange(2, 4))
