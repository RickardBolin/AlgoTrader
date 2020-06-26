import requests
from bs4 import BeautifulSoup
from wayback import WaybackClient
import datetime

client = WaybackClient()

def reps(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.tbody
    rows = rows.find_all('tr')
    reports = []
    
    for r in rows:
        company = r.a.get('href')
        tds = r.find_all('td')
        typ = tds[1].get_text()
        date = tds[2].get_text()
        reports.append((company, typ, date))

    return reports    

def get_closest_result(url, date):
    format_str = "%Y-%m-%d"
    date = datetime.datetime.strptime(date, format_str)
    results = list(client.search(url))
    i = 0
    while(results[i].timestamp < date):
        i += 1 

    return results[i]

URL = 'https://www.privataaffarer.se/borsguiden/kalendarium-och-dagens-agenda/borskalender'

page = requests.get(URL)
reports = reps(page)


results = list(client.search(URL))
results.reverse()

print(results[10].raw_url)

record = results[10]

response = client.get_memento(record.raw_url)

reports = reps(response)
res = get_closest_result(reports[0][0],reports[0][2])
print(reports[0])
print(res)
print(res.raw_url)
