# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 16:19:17 2016

@author: Nzix
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import urllib2
import re
import datetime
import MySQLdb
import tools
import socket

page = 1

if len(sys.argv) > 1:
    if re.search(r'^\d+$',sys.argv[1]) !=None:
        page = int(sys.argv[1])
        if page < 1:
            print "illegal argument"
            exit()


headers = {
    "Host": "www.keyakizaka46.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
}

request = urllib2.Request(url = 'http://www.keyakizaka46.com/s/k46o/diary/member/list?ima=0000&page=%s&cd=member' % (page - 1), headers = headers)

print "start"

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
result = re.findall(r'<article>[\s\S]*?<h3>\s*<a href="(.*?)">(.*?)</a>[\s\S]*?<p class="name">\s*([\s\S]*?)\s*</p>[\s\S]*?<div class="box-article">([\s\S]*?)</div>\s+?<div class="box-bottom">[\s\S]*?<li>\s*([\s\S]*?)\s*</li>[\s\S]*?</article>',data,re.M|re.I)


conn=MySQLdb.connect(
    host='*???*',
    user='*???*',
    passwd='*???*',
    db='*???*',
    charset="utf8")

cur=conn.cursor()

preparedl = []

for i in xrange(len(result)-1,-1,-1):

    #author <type 'unicode'>    
    author = result[i][2].replace(' ','')
    rome = tools.members[author][1]
    kana = tools.members[author][0]
    jptime = datetime.datetime.strptime(result[i][4],"%Y/%m/%d %H:%M")
    post = jptime.strftime("%Y/%m/%d %H:%M")
    link = 'http://www.keyakizaka46.com' + result[i][0]

    postid = tools.findid(link)
    if cur.execute("SELECT * FROM raw WHERE id = %s AND team = 1",(postid,)) != 0:
        continue
    
    #title <type 'unicode'>
    title = result[i][1]
    
    while re.search(r'&\w+?;',title)!=None:
        title = re.sub(r'(?P<mark>&[\w]+?;)',tools.convertmark,title)
    if re.search(u"^[\s|\u3000|\xa0]*$",title)!=None:
        title = '(無題)'

    print author,title


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
        cur.execute("INSERT INTO raw VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(postid,1,author,post,link,title,text,datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
    except BaseException as e:
        print e
    else:
        conn.commit()
        print "raw save"

    # brief <type 'unicode'>
    brief = tools.summary(text)
        
    try:
        cur.execute("INSERT INTO list VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(postid,1,post,kana,rome,author,link,title,brief))
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
        cur.execute("INSERT INTO blog VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(postid,1,post,rome,author,link,title,title_translation,text_original,text_translation))
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
