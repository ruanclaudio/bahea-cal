import arrow
import os
import requests
import tempfile
from bs4 import BeautifulSoup

from io import StringIO
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

SCOPES = 'https://www.googleapis.com/auth/calendar'

token_name = os.environ.get('TOKEN_NAME')
store = file.Storage(token_name)
creds = store.get()
if not creds or creds.invalid:
    with open(token_name, 'w+') as token_file:
        token_file.write(os.environ.get('TOKEN_JSON'))
        with tempfile.NamedTemporaryFile('w+', delete=False) as creds_file:
            flow = client.flow_from_clientsecrets(
                os.environ.get('CREDENTIALS_JSON'), SCOPES)
    creds = tools.run_flow(flow, store)
    store.put(creds)
service = build('calendar', 'v3', http=creds.authorize(Http()))

now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

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
        possible_existing = service.events().list(
            calendarId='primary', timeMin=when, maxResults=20,
            singleEvents=True, orderBy='startTime',
            timeMax=when.shift(minutes=+140)).execute()

        existent = False
        for possible in possible_existing.get('items', []):
            if possible['summary'] == event['summary']:
                existent = True
                break

        if not existent:
            eventc = service.events().insert(
                calendarId='primary', body=event).execute()
            print('Event created: {} x {} {} {}'.format(
                team1, team2, when,
                eventc.get('htmlLink')))
        else:
            print('Event already in calendar: {} x {} {} {}'.format(
                team1, team2, when,
                possible.get('htmlLink')))
