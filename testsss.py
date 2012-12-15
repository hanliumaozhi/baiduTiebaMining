# -*- coding: utf-8 -*-
"""
Created on Sun Nov 06 18:39:52 2011
@author: hanliumaozhi
"""

import urllib, urllib2, cookielib
body={'mem_pass': 'on','username':'apiis','password':'jpwoniuapiis'}
x=urllib2.urlopen("http://www.baidu.com")
print x.read().decode('gb2312').encode('utf-8')
cj = cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
urllib2.install_opener(opener)
req=urllib2.Request("https://passport.baidu.com/?login",urllib.urlencode(body))
urllib2.urlopen(req)
x=urllib2.urlopen("http://www.baidu.com")
print x.read()