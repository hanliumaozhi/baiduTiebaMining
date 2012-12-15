# -*- coding: utf-8 -*-
import time, urllib2
from BeautifulSoup import BeautifulSoup

url=u"http://www.baidu.com/p/Dragon丶Eva?from=tieba"

urlopen = urllib2.urlopen(url.encode("gbk"))
content = urlopen.read()
urlopen.close()
print content
soup = BeautifulSoup(content)
a = soup.findAll("script")
print len(a)

print a[0]
ss = a[8].text.split('":"')
temm = ss[2].replace('\/','/')
yy=BeautifulSoup(temm.replace('"});',''))
redata = yy.findAll("div",{"class":"tieba-name"})
level = yy.findAll("span",{"class":"level"})

print len(redata)
print len(level)

for i in redata:
    print i.text

for i in level:
    print i
    print i.text[:-1]
