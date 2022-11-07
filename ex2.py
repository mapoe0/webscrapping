from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from time import sleep
from selenium.webdriver.common.by import By
import csv

url = "https://www.youtube.com/"
path_result = "result/exo2/"

browser = Chrome()
browser.get(url)

# accept the cookies
sleep(3)
buttons = browser.find_element(By.CSS_SELECTOR, '.yt-spec-button-shape-next.yt-spec-button-shape-next--filled.yt-spec'
                                                '-button-shape-next--call-to-action.yt-spec-button-shape-next--size-m')
sleep(1)
buttons.click()
# click on the menu btn to acces at the link for qq 3
sleep(1)
menu_button = browser.find_element(By.ID, 'guide-button')
sleep(1)
menu_button.click()

# get the html of the home page
soup = BeautifulSoup(browser.page_source, "html.parser")

###
# QUESTION 1
# Scrape the text from each span tag
###

spans = soup.find_all('span')
spansTxt = []
for span in spans:
    spansTxt.append(span.text)

# console display
print(f"Span Text\n{spansTxt}")

# save in a file.txt
fileName = path_result + 'span.txt'
with open(fileName, 'w', encoding="utf-8") as f:
    for txt in spansTxt:
        f.write(f"{txt}\n")

###
# QUESTION 2
# How many images are on YouTube'e homepage?
###
images = soup.find_all('img')
# display the lengh
print(f"\nNb d'image dans la page d'acceuil:\n{len(images)}")

###
# QUESTION 3
# Can you find the URL of the link with title = "Movies"? Music? Sports?
###
titles = ['Musique', 'Sport', 'Films et TV']
links = []
yt = "https://www.youtube.com"
for title in titles:
    relative_link = soup.find('a', attrs={"title": title})['href']
    links.append({
        "title": title,
        "lien": yt + relative_link
    })
# console print
print(f"Liens:\n{links}")

# save in links.csv
fileName = path_result + "links.csv"
with open(fileName, 'w', newline='', encoding="utf-8") as f:
    w = csv.DictWriter(f, ['title', 'lien'])
    w.writeheader()
    for link in links:
        w.writerow(link)
###
# QUESTION 4
# Now, try connecting to and scraping
# https://www.youtube.com/results?search_query=stairway+to+heaven
###
url = "https://www.youtube.com/results?search_query=stairway+to+heaven"
browser.get(url)
sleep(2)
soup = BeautifulSoup(browser.page_source, "html.parser")

###
# QUESTION 4a
#  Can you get the names of the first few videos in the search results?
###
link_titles = soup.find_all('a', attrs={'id': 'video-title'})
titles = []
for link in link_titles:
    titles.append(link['title'])
# console display
print(f"Video title of result for search: {url}\n{titles}")
# save into titles.txt
fileName = path_result + 'titles.txt'
with open(fileName, 'w', encoding="utf-8") as f:
    f.write(f"Video title of result for search: {url}\n")
    for title in titles:
        f.write(f"{title}\n")
###
# QUESTION 4b
#  Next, connect to one of the search result videos -
# https://www.youtube.com/watch?v=qHFxncb1gRY
###
url = "https://www.youtube.com/watch?v=qHFxncb1gRY"
browser.get(url)
sleep(2)
soup = BeautifulSoup(browser.page_source, "html.parser")

###
# QUESTION 4c
#  Can you find the "related" videos? What are their titles? Durations? URLs? Number of views?
#
###
related_video_container = soup.find('div', attrs={'id': 'related'})
related_video_lst = related_video_container.find_all("div", attrs={'id': 'dismissible'})
related = []

for related_video in related_video_lst:
    # if the related is a playlist its gonna throw an AttributeError exeption
    try:
        title = related_video.find('span', attrs={'id': 'video-title'}).text.strip()
        duration = related_video.find('span', attrs={'id': 'text'}).text.strip()
        views = related_video.find('span',
                                   attrs={
                                       'class': 'inline-metadata-item style-scope ytd-video-meta-block'}).text.rstrip()
        url = yt + related_video.find('a', attrs={'id': 'thumbnail'})['href']

        related.append({
            'title': title,
            'duration': duration,
            'url': url,
            'views': views
        })
    except AttributeError:
        pass
# console print
print(f"Related video for url: {url}\n{related}")

# save into related.csv
fileName = path_result + "related.csv"
with open(fileName, 'w', newline='', encoding="utf-8") as f:
    w = csv.DictWriter(f, ['title', 'duration', 'url', 'views'])
    w.writeheader()
    for video in related:
        w.writerow(video)

###
# QUESTION 4d
# Try finding (and scraping) the description of the video
###
description = soup.find('span', attrs={'id': 'plain-snippet-text'}).text
print(f"Description de la video:\n{description}")
browser.close()
