# -*- coding: utf-8 -*-
__metaclass__=type

import  urllib2, threading, Queue, socket
from BeautifulSoup import BeautifulSoup
import couchdb

socket.setdefaulttimeout(100)

server = couchdb.Server(r'http://localhost:5984')
bdurl = u"http://www.baidu.com/p/"
appurl = u"?from=tieba"

usernameList = list()
userInfoHadDown = list()
someOneHadDoneListtem = list()
temredata = list()

DB = u"user_name"
InfoDB = u"userinfo"
HadDownInfo =u"user_have_down"

db = server[DB]
infodb = server[InfoDB]
haddb = server[HadDownInfo]
for i in db:
    usernameList.append(db[i]["username"])
for i in haddb:
    userInfoHadDown.append(haddb[i]["username"])



class Worker(threading.Thread):
    def __init__(self,work_queue,func):
        super(Worker, self).__init__()
        self.work_queue=work_queue
        self.func=func

    def run(self):
        while True:
            try:
                elemt=self.work_queue.get()
                self.func(elemt)
            finally:
                self.work_queue.task_done()

def DateMining(name):
    if not name in userInfoHadDown:
        url = bdurl + name + appurl
        try:
            print name
            urlopen = urllib2.urlopen(url.encode("gbk"))
            content = urlopen.read()
            urlopen.close()
        except:
            print "err"
        else:
            soup = BeautifulSoup(content)
            try:
                a = soup.findAll("script")
                ss = a[8].text.split('":"')
                temm = ss[2].replace('\/','/')
            except:
                print "err"
            else:
                someOneHadDoneListtem.append(name)
                yy=BeautifulSoup(temm.replace('"});',''))
                redata = yy.findAll("div",{"class":"tieba-name"})
                level = yy.findAll("span",{"class":"level"})
                sptem = list()

                for i in xrange(len(redata)):
                    try:
                        ss = [redata[i].text,level[i].text[:-1]]
                    except:
                        ss = [redata[i].text,sptem[i-1][1]]
                        sptem.append(ss)
                    else:
                        sptem.append(ss)
                temredata.append([name,sptem])
                print u"succe"

def main(func):
    work_queue = Queue.Queue()
    for i in xrange(2):
        worker=Worker(work_queue,func)
        worker.setDaemon(True)
        worker.start()
    for i in usernameList:
        work_queue.put(i)
    work_queue.join()

if __name__ == "__main__":
    main(DateMining)
    print len(someOneHadDoneListtem)
    HadDoneUpdata = list()
    userInfoUpdata = list()

    for i in someOneHadDoneListtem:
        stem = dict()
        stem["_id"] = u"baidu" + i
        stem["username"] = i
        HadDoneUpdata.append(stem)

    for i in temredata:
        stem = dict()
        stem["_id"] = u"baidu" + i[0]
        stem["username"] = i[0]
        stem["data"] = i[1]
        userInfoUpdata.append(stem)

    haddb.update(HadDoneUpdata)
    infodb.update(userInfoUpdata)



