# -*- coding: utf-8 -*-
"""
Created on Tue Nov 06 22:39:14 2012

@author: han
"""
__metaclass__=type
import  urllib2, time
from BeautifulSoup import BeautifulSoup
import jsonlib2 as json
import couchdb

url = r"http://tieba.baidu.com/f/fdir?fd=%C8%CB%CE%C4%D7%D4%C8%BB&sd=%C0%FA%CA%B7"

server = couchdb.Server(r'http://localhost:5984')
DB = u"tieba_name"
db = server.create(DB)
#db = server[DB]
urlopen = urllib2.urlopen(url)
content = urlopen.read().decode('gb18030').encode('utf-8')
urlopen.close()
soup = BeautifulSoup(content)

a = soup.findAll(width="20%")

b = []
a = a[:20]

for i in a:
    b.append(i.text)

b.append(u"汉服")
b.append(u"汉服水吧")

dicta = dict()
dicta[u"TiebaName"] = b
dicta[u"_id"]=u"TiebaName"
dicta[u"created_at"] = time.ctime()
cc = [dicta]

db.update(cc)

for i in b:
    print i
