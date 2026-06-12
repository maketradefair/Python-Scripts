

import requests
import logging
import bs4
from urllib.parse import urlencode

logging.basicConfig(level=logging.DEBUG)

filename = "Static-Search-Lists.xml"
soup = bs4.BeautifulSoup(open(filename).read(), 'lxml-xml')

creds = ('aanzAst1','uAUT9qW+')
requested_with = {"X-Requested-With" : "Python"}

for search_list in soup.find_all('STATIC_LIST'):
    api_url = 'https://qualysapi.qg1.apps.qualysksa.com/api/2.0/fo/qid/search_list/static/?action=create'
    
    title=search_list.find('TITLE').text
    #title = title.replace(' ', '+')
    api_url+='&title=' + title
    
    qids = search_list.find_all('QIDS')
    if qids is not None:
        for q in qids:
            qid = ",".join(item.text for item in q.find_all('QID'))
    #print(qid)
    api_url+='&qids=' + qid

    #print(api_url)
    response = requests.post(api_url, auth=creds, headers=requested_with)
    print(response.text)