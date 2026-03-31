from bs4 import BeautifulSoup
import requests
import json


with open('licenses_link.json') as f:
    prev = json.load(f)

r         = requests.get('https://sites.google.com/view/agilitycpcportugal/p%C3%A1gina-inicial')
soup      = BeautifulSoup(r.text,features="lxml")
curr_link = soup.find_all(attrs={'aria-label':'Licenças'})[1]['href']

if prev['link'] != curr_link:
    print("AVISO: Novo ficheiro de licencas!!")
    print()
    print(curr_link)

