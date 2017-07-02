# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 16:19:17 2016

@author: Nzix
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import pytz
import feedparser
import re
import datetime
import MySQLdb
import tools

print "start"
feed = feedparser.parse('http://blog.nogizaka46.com/atom.xml',agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
print "got"

conn=MySQLdb.connect(
    host='*???*',
    user='*???*',
    passwd='**???*',
    db='*???*',
    charset="utf8")

cur=conn.cursor()

preparedl = []

for i in xrange(len(feed.entries)-1,-1,-1):

    author = feed.entries[i].author#<type 'unicode'>
    link = feed.entries[i].link#<type 'unicode'>
    title = feed.entries[i].title#<type 'unicode'>
    
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
    
    utctime = datetime.datetime.strptime(feed.entries[i].published,"%Y-%m-%dT%H:%M:%SZ")
    utctime = utctime.replace(tzinfo=pytz.utc)
    #cntime=utctime.astimezone(pytz.timezone("Asia/Shanghai"))
    jptime = utctime.astimezone(pytz.timezone("Asia/Tokyo"))
    post = jptime.strftime("%Y/%m/%d %H:%M")

    # text <type 'unicode'>
    text = feed.entries[i].content[0].value
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
