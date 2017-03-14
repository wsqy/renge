# coding:utf-8
import requests
from bs4 import BeautifulSoup

baseurl = "http://cl.gtta.pw/"


def down_load(tid=2294890):
    url = baseurl + "?tid=%s" % (tid, )
    print(url)
    r = requests.get(url)
    print(r.content)
    soup = BeautifulSoup(r.text).prettify()
    page = soup.find(attrs={'id': 'last'})
    print(page)

# print(r.content)
down_load()
