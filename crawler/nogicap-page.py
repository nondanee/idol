# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 16:19:17 2016

@author: Nzix
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import datetime
import MySQLdb
import tools
import urllib2
import socket

page = 1

if len(sys.argv) > 1:
    if re.search(r'^\d+$',sys.argv[1]) !=None:
        page = int(sys.argv[1])
        if page < 1 or page > 15:
            print "illegal argument"
            exit()

print "start"

headers = {
    "Host": "blog.nogizaka46.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
}

request = urllib2.Request(url = 'http://blog.nogizaka46.com/?p=%s' % page, headers = headers)

reconnect = 0
while 1:
    try:
        response = urllib2.urlopen(request,timeout = 5)
    except socket.timeout:
        reconnect = reconnect + 1
        if reconnect < 3:
            continue
        else:
            exit()
    else:
        break
    
data = response.read().decode('utf-8')

print "got"

result = re.findall(r'<h1 class="clearfix">[\s\S]+?<span class="author">([\s\S]+?)</span>\s*<span class="entrytitle">\s*<a href="([\s\S]+?)" rel="bookmark">([\s\S]*?)</a>[\s\S]+?<div class="entrybody">([\s\S]+?)</div>\s*?<div class="entrybottom">([\s\S]+?)<a href="([^"]+?)">',data,re.M|re.I|re.S)
assert len(result) == 5


conn=MySQLdb.connect(
    host='*???*',
    user='*???*',
    passwd='*???*',
    db='*???*',
    charset="utf8")

cur=conn.cursor()

preparedl = []

for i in xrange(len(result)-1,-1,-1):

    # <type 'unicode'>
    author = result[i][0]
    # <type 'unicode'>
    link = result[i][1]
    assert result[i][1] == result[i][5]
    # <type 'unicode'>
    title = result[i][2]
    
    postid = tools.findid(link)
    
    if cur.execute("SELECT * FROM raw WHERE id = %s AND team = 0",(postid,)) != 0:
        continue
    
    while re.search(r'&\w+?;',title)!=None:
        title = re.sub(r'(?P<mark>&[\w]+?;)',tools.convertmark,title)
    if re.search(u"^[\s|\u3000|\xa0]*$",title)!=None:
        title = '(無題)'

    if author == "３期生":
        (author,title) = tools.identifysankisei(title)
        if author == "３期生":
            print "identify error"

    print author,title
        
    rome = tools.members[author][1]
    kana = tools.members[author][0]

    post = re.search(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}',result[i][4]).group(0)
    jptime = datetime.datetime.strptime(post,"%Y/%m/%d %H:%M")

    # text <type 'unicode'>
    text = result[i][3]
    text = tools.sortout(text)
    
    
    allimg = re.findall(r'<img[^>]+?src="([\s\S]+?)"[^>]*?>',text)

    for p in xrange(0,len(allimg)):

        imgurl = allimg[p]

        if re.search(r'.jpg$',imgurl)!=None or re.search(r'.jpeg$',imgurl)!=None:
            suffix = "jpg"
        elif re.search(r'.png$',imgurl)!=None:
            suffix = "png"
        elif re.search(r'.gif$',imgurl)!=None:
            suffix = "gif"
        elif re.search(r'awalker',imgurl)!=None:
            suffix = "jpg"
        else:
            print "unknown type"
            suffix = "file"

        filename = '%s-%s.%s'%(jptime.strftime("%Y-%m-%d-%H-%M"),str(p+1).zfill(2),suffix)
        newurl = 'hostpath/%s/%s'%(rome,filename)

        text = re.sub(re.escape(imgurl).decode("utf-8"),newurl,text)

        if re.search(re.escape(imgurl),text) != None:
            print "img dealing error"
            
        try:
            cur.execute("INSERT INTO photo VALUES(%s,%s,%s,%s,%s)",(rome,filename,author,imgurl,0))
        except BaseException as e: 
            print e
        else:
            preparedl.append([rome,filename,imgurl])
            
    conn.commit()
    
        
    try:
        cur.execute("INSERT INTO raw VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(postid,0,author,post,link,title,text,datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
    except BaseException as e:
        print e
    else:
        conn.commit()
        print "raw save"

    # brief <type 'unicode'>
    brief = tools.summary(text)
        
    try:
        cur.execute("INSERT INTO list VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(postid,0,post,kana,rome,author,link,title,brief))
    except BaseException as e:
        print e
    else:
        conn.commit()
        print "list save"
        
    
    if title == '(無題)':
        title_translation = '(无题)'
    else:
        title_translation = tools.translate(title)
        
    text_translation = tools.translate(text)

    text_original = tools.indent(text)
    text_translation = tools.indent(text_translation)  
    
    
    try:
        cur.execute("INSERT INTO blog VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(postid,0,post,rome,author,link,title,title_translation,text_original,text_translation))
    except BaseException as e:
        print e
    else:
        conn.commit()
        print "blog save"
        

for imginfo in preparedl:
    status = tools.downloadphoto(imginfo[0],imginfo[1],imginfo[2])
    cur.execute('UPDATE photo set status = %s where rome = "%s" and filename = "%s";'%(status,imginfo[0],imginfo[1]))
    conn.commit()
    print imginfo[0],imginfo[1],status

conn.close()
print "done"
