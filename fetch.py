from bs4 import BeautifulSoup
import requests


url = 'http://www.esporteclubebahia.com.br/agenda/'
resp = requests.get(url)
soup = BeautifulSoup(resp.content, 'html.parser')
lis = soup.findAll('li')
_as = []
for li in lis:
    _as.append(li.find('a'))
for a in _as:
    if '/agenda/' in a.get('href', ''):
        if not a.find('div', {'class': 'times'}):
            continue
        print(a.find('div', {'class': 'times'}).findAll('span')[0].text)
        print(a.find('div', {'class': 'times'}).findAll('span')[1].text)
        print(a.find('div', {'class': 'data'}).find('span').text.split('•'))
