#coding=utf-8
import  urllib2
from BeautifulSoup import BeautifulSoup
import couchdb

bdurl = u"http://tieba.baidu.com/f/like/furank?kw="
appurl = u"&pn="

server = couchdb.Server(r'http://localhost:5984')
DB = u"tieba_name"
HDDB = u"tieba_have_down"
URDB = u"user_name"
db = server[DB]
hddb = server[HDDB]
urdb = server[URDB]

tieba_name = list()
tiebaHaveDown = list()
user_name = list()

for i in db["TiebaName"]['TiebaName']:
    tieba_name.append(i)

for i in hddb:
    tiebaHaveDown.append(hddb[i]["tiebaname"] + "$$" + hddb[i]["page"])

for i in urdb:
    user_name.append(urdb[i]["_id"])

for i in tieba_name:
    for j in xrange(1,6):
        print type(i)
        stem = i + u"$$" + repr(j)
        if not stem in tiebaHaveDown:
            url = bdurl + i + appurl + repr(j)
            print url
            try:
                urlopen = urllib2.urlopen(url.encode("gb18030"))
                content = urlopen.read().decode('gb18030').encode('utf-8')
                urlopen.close()
            except:
                print "err " + i + str(j)
            else:
                tiebaHaveDown.append(stem)
                soup = BeautifulSoup(content)
                a = soup.findAll("td",{"class":"drl_item_name"})
                for k in a:
                    kk = k.text
                    if not kk in user_name:
                        user_name.append(kk)

userNameUpdata = list()
tiebaHadUpdata = list()

for i in user_name:
    tem = dict()
    tem["_id"] = "baidu " + i
    tem["username"] = i
    userNameUpdata.append(tem)

for i in tiebaHaveDown:
    stem = i.split("$$")
    tem = dict()
    tem["tiebaname"] = stem[0]
    tem["page"] = stem[1]
    tiebaHadUpdata.append(tem)

hddb.update(tiebaHadUpdata)
urdb.update(userNameUpdata)

print len(userNameUpdata)




