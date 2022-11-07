import time
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import csv

url = "https://store.steampowered.com/tags/en/Action/"
# folder wich contain the result
path_result = "result/exo1/"

browser = Chrome()
browser.get(url)
time.sleep(2)

soup = BeautifulSoup(browser.page_source, "lxml")
###
# QUESTION 1 & 2
###
# all the top games are stored inside a container div
container = soup.find('div', {'id': 'SaleSection_93094'})
# the top games data content is stored inside a 'a' link
allGamesData = container.find_all('a')
games = []
for gameData in allGamesData:
    game = {}
    # the game title is stored insade the alt of the img
    img = gameData.find('img', alt=True)
    game['title'] = img['alt']
    # price is inside a div with unique class name
    price = gameData.find('div', {'class': 'salepreviewwidgets_StoreSalePriceBox_Wh0L8'}).text
    game['price'] = price
    games.append(game)
# console display
print(f"Top games \n{games}")
# save in games_info.csv
fileName = path_result + "games_info.csv"
with open(fileName, 'w', newline='', encoding="utf-8") as f:
    w = csv.DictWriter(f, ['title', 'price'])
    w.writeheader()
    for game in games:
        w.writerow(game)
###
# QUESTION 3
###
head = soup.find('head')

tags = []
for tag in head.children:
    if tag != '\n':
        tags.append(tag)
    next(head.children)
print(f"Header _n{tags}")
# save as header_tags.html
fileName = path_result + "header_tags.html"
with open(fileName, 'w', encoding="utf-8") as f:
    for tag in tags:
        f.write(f"{tag}\n")
###
# QUESTION 5
###
itemsContainers = soup.find_all('div', attrs={'class': 'popup_genre_expand_content responsive_hidden'})
narrow_by_tag = []
for div in itemsContainers:
    items = div.find_all('a', attrs={'class': 'popup_menu_item'})
    for item in items:
        narrow_by_tag.append(item.text)
# console display
print(f"Narrow By tag \n{narrow_by_tag}")
# save into narrow_by_tag.txt
fileName = path_result + "narrow_by_tag.txt"
with open(fileName, 'w', encoding="utf-8") as f:
    for cat in narrow_by_tag:
        f.write(f"{cat}\n")
    exit()
# we need to close the brower
browser.close()
