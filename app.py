from bs4 import BeautifulSoup
import requests

url = "https://football.ua/"

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

}

req = requests.get(url, headers=headers)
src = req.text

# with open("index.html", "w") as file:
#     file.write(src)

# with open("index.html") as file:
#     src = file.read()

soup = BeautifulSoup(src, "lxml")
# all_league_hrefs = soup.find_all("li")
all_hrefs = soup.find_all("a")


all_country = ["Україна", "Англія", "Німеччина", "Іспанія", "Італія",
               "Нідерланди", "Португалія", "Туреччина", "Франція"]

for country in all_country:
    for item in all_hrefs:
        if (len(item.get("href")) < 40) and (len(item.get("href")) > 20) and item.text == country:
            item_text = item.text
            item_href = item.get("href")
            print(f"{item_text}: {item_href}")
