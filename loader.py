import requests

user_id = 12345
url = 'https://www.zakon.kz/news'
r = requests.get(url)
with open('news.html', 'w') as output_file:
    output_file.write(r.text)
