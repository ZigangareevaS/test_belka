import joblib
import numpy as np
import requests
from bs4 import BeautifulSoup

# Собираем ссылки на объявления
def get_href_value(url):
    href_values = []
    res = requests.get(url)
    content = res.content
    soup = BeautifulSoup(content, "html.parser")
    a_tag = soup.find_all("a", class_="adv-list-image__link")
    for el in a_tag:
        href_value = el.get('href')
        href_values.append(href_value)
    return href_values

# Достаем инфо из объявления
def get_info(urls):
    ads = {}
    for line in urls:
        url = f'http://citystar.ru/{line}'
        res = requests.get(url)
        content = res.content
        soup = BeautifulSoup(content, "html.parser")
        fonts = [el.text for el in soup.find_all('font', class_='fin')]
        ads[url] = [fonts[1], fonts[3], fonts[5], fonts[7], fonts[9], fonts[11], fonts[13], fonts[15], fonts[17], fonts[19],
            fonts[21], fonts[23], fonts[25], fonts[-1]]
    return ads

links = []
for end in ['', '&pN=2', '&pN=3', '&pN=4']:
    url = f'http://citystar.ru/detal.htm?d=43&nm=%CE%E1%FA%FF%E2%EB%E5%ED%E8%FF%20-%20%CF%F0%EE%E4%E0%EC%20%EA%E2%E0%F0%F2%E8%F0%F3%20%E2%20%E3.%20%CC%E0%E3%ED%E8%F2%EE%E3%EE%F0%F1%EA%E5{end}'
    links.append(get_href_value(url))
    joblib.dump(links, 'links.pkl')

urls = np.array(links).flatten()
result = get_info(urls)
joblib.dump(result, 'result.pkl')
