from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urlsplit,urlunsplit
import datetime


def download(url, file):
    with open(file, 'wb') as f:
        r = requests.get(url)
        f.write( r.content )

def convert(url):
    u = urlsplit(url)
    u = u._replace(query='format=csv')._replace(path=u.path.replace('/edit','/export'))
    return urlunsplit(u)


with open('licenses_link.json') as f:
    prev = json.load(f)

r         = requests.get('https://sites.google.com/view/agilitycpcportugal/p%C3%A1gina-inicial')
soup      = BeautifulSoup(r.text,features="lxml")
curr_link = soup.find_all(attrs={'aria-label':'Licenças'})[1]['href']

if prev['link'] != curr_link:
    print("AVISO: Novo ficheiro de licencas!!")
    print()
    print(curr_link)
    
    download(convert(curr_link), f'licenses-{datetime.date.today()}.csv')
    with open('licenses_link.json','w') as f:
        prev['link'] = curr_link
        json.dump(prev, f, indent=2)



