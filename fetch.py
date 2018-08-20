import arrow
import requests
from bs4 import BeautifulSoup


from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))


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
        team1 = a.find('div', {'class': 'times'}).findAll('span')[0].text
        team2 = a.find('div', {'class': 'times'}).findAll('span')[1].text
        spplited = a.find(
            'div', {'class': 'data'}).find('span').text.split('•')
        date = spplited[0].strip()
        time = spplited[1].strip()
        when = arrow.get(
            date + ' ' + time + ' America/Bahia', 'DD/MM HH:mm ZZZ')
        when = when.replace(year=arrow.utcnow().year)
        event = {
            'summary': '{} x {}'.format(team1, team2),
            'location': '',
            'description': '{} x {}'.format(team1, team2),
            'start': {
                'dateTime': when.isoformat(),
                'timeZone': 'America/Bahia',
            },
            'end': {
                'dateTime': when.replace(minutes=+110).isoformat(),
                'timeZone': 'America/Bahia',
            },
        }
        eventc = service.events().insert(
            calendarId='primary', body=event).execute()
        print('Event created: {} x {} {} {}'.format(
            team1, team2, when,
            eventc.get('htmlLink')))
