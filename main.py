import csv

from bs4 import BeautifulSoup

from common import get_news_full_text, get_session

BASE_URL = 'https://www.zakon.kz'
fieldnames = ['title', 'full_text', 'datetime', 'comm_num']

session = get_session()
response = session.get(BASE_URL + '/news')

soup = BeautifulSoup(response.text, 'html.parser')
tags = soup.findAll(name='div', attrs="cat_news_item")
date_str = tags[0].find(None, {'date'}).string

with open('today_news.csv', 'w') as f:
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    for tag in tags[1:]:
        news = dict()
        news['title'] = tag.find('a').string
        news['full_text'] = get_news_full_text(
            BASE_URL + tag.find('a')['href'],
            session
        )
        news['datetime'] = date_str + ' ' + tag.find('span').string
        comm_num = tag.find('span', 'comm_num')
        if comm_num:
            news['comm_num'] = int(comm_num.string)
        else:
            news['comm_num'] = 0
        csv_writer.writerow(news)

