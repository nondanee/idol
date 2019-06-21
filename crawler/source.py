# -*- coding: utf-8 -*-

import datetime, re, xml.dom.minidom
import requests
# proxies = {'http': 'http://139.180.134.223:8080', 'https': 'http://139.180.134.223:8080'}

def fetch(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3509.0 Safari/537.36'}
    retry = 0
    while True:
        try:
            response = requests.get(url, headers = headers, timeout = 5, proxies = None)
            return response.content
        except Exception as e:
            retry += 1
            if retry > 5: raise
            print(e)

def from_keyakizaka_pc_site(page = 1):
    html = fetch('http://www.keyakizaka46.com/s/k46o/diary/member/list?site=k46o&ima=0000&page={}'.format(page - 1)).decode('utf-8')
    regexp = re.compile(r'<article>[\s\S]*?<h3>\s*<a href="(.*?)">(.*?)</a>[\s\S]*?<p class="name">\s*([\s\S]*?)\s*</p>[\s\S]*?<div class="box-article">([\s\S]*?)</div>\s+?<div class="box-bottom">[\s\S]*?<li>\s*([\s\S]*?)\s*</li>[\s\S]*?</article>', re.M|re.I)
    entries = regexp.findall(html)
    assert len(entries) == 20
    result = []
    for entry in entries:
        author = entry[2].replace(' ', '')
        post = datetime.datetime.strptime(entry[4], '%Y/%m/%d %H:%M').strftime('%Y/%m/%d %H:%M')
        link = 'http://www.keyakizaka46.com{}'.format(entry[0])
        title = entry[1]
        text = entry[3]
        result.append([post, author, title, text, link])
    return result

def from_hinatazaka_pc_site(page = 1):
    html = fetch('https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&page={}'.format(page - 1)).decode('utf-8')
    regexp = re.compile(r'<div class="p-blog-article">[\s|\S]+?<div class="c-blog-article__title">\s*([\s|\S]*?)\s*</div>[\s|\S]+?<div class="c-blog-article__date">\s*([\s|\S]+?)\s*</div>\s*<div class="c-blog-article__name">\s*([\s|\S]+?)\s*</div>[\s|\S]+?<div class="c-blog-article__text">\s*([\s|\S]+?)\s*</div>\s*<div class="p-button__blog_detail">\s*?<a class="c-button-blog-detail" href="([^"]+)"', re.M|re.I)
    entries = regexp.findall(html)
    assert len(entries) == 20
    result = []
    for entry in entries:
        author = entry[2].replace(' ', '')
        link = 'http://www.hinatazaka46.com{}'.format(entry[4])
        post = datetime.datetime.strptime(entry[1], '%Y.%m.%d %H:%M').strftime('%Y/%m/%d %H:%M')
        title = entry[0]
        text = entry[3]
        result.append([post, author, title, text, link])
    return result

def from_nogizaka_pc_site(page = 1):
    html = fetch('http://blog.nogizaka46.com/?p={}'.format(page)).decode('utf-8')
    regexp = re.compile(r'<h1 class="clearfix">[\s\S]+?<span class="author">([\s\S]+?)</span>\s*<span class="entrytitle">\s*<a href="([\s\S]+?)" rel="bookmark">([\s\S]*?)</a>[\s\S]+?<div class="entrybody">([\s\S]+?)</div>\s*?<div class="entrybottom">[^\d]*([\s\S]+?)[^\d]*<a href="([^"]+?)">', re.M|re.I|re.S)
    entries = regexp.findall(html)
    assert len(entries) == 5
    result = []
    for entry in entries:
        author = entry[0]
        link = entry[1]
        assert entry[1] == entry[5]
        post = datetime.datetime.strptime(entry[4], '%Y/%m/%d %H:%M').strftime('%Y/%m/%d %H:%M')
        title = entry[2]
        text = entry[3]
        result.append([post, author, title, text, link])
    return result

def from_nogizaka_rss():
    html = fetch('http://blog.nogizaka46.com/atom.xml')
    dom_tree = xml.dom.minidom.parseString(html)
    entries = dom_tree.documentElement.getElementsByTagName('entry')
    #assert len(entries) == 15
    result = []
    for entry in entries:
        title = entry.getElementsByTagName('title')[0].firstChild.data
        link = entry.getElementsByTagName('link')[0].getAttribute('href')
        author = entry.getElementsByTagName('author')[0].getElementsByTagName('name')[0].firstChild.data
        utc = datetime.datetime.strptime(entry.getElementsByTagName('published')[0].firstChild.data, '%Y-%m-%dT%H:%M:%SZ')
        post = (utc + datetime.timedelta(hours = 9)).strftime('%Y/%m/%d %H:%M')
        text = entry.getElementsByTagName('content')[0].childNodes[1].data
        result.append([post, author, title, text, link])
    return result

def from_keyakizaka_pc_site_single(url):
    html = fetch(url).decode('utf-8')
    regexp = re.compile(r'<article>[\s\S]*?<h3>\s*([\s\S]*?)\s*</h3>\s*<p class="name">\s*<a[^>]+>([\s\S]*?)</a>\s*</p>[\s\S]*?<div class="box-article">([\s\S]*?)</div>\s+?<div class="box-bottom">[\s\S]*?<li>\s*([\s\S]*?)\s*</li>[\s\S]*?</article>', re.M|re.I)
    entries = regexp.findall(html)
    assert len(entries) == 1
    result = []
    for entry in entries:
        author = entry[1].replace(' ', '')
        post = datetime.datetime.strptime(entry[3], '%Y/%m/%d %H:%M').strftime('%Y/%m/%d %H:%M')
        link = url
        title = entry[0]
        text = entry[2]
        result.append([post, author, title, text, link])
    return result

def from_nogizaka_pc_site_single(url):
    html = fetch(url).decode('utf-8')
    regexp = re.compile(r'<h1 class="clearfix">[\s\S]+?<span class="author">([\s\S]+?)</span>\s*<span class="entrytitle">\s*([\s\S]*?)\s*</span>[\s\S]*?<div class="entrybody">([\s\S]+?)</div>\s*?<div class="entrybottom">[^\d]*([\s\S]+?)[^\d]*</div>', re.M|re.I|re.S)
    entries = regexp.findall(html)
    assert len(entries) == 1
    result = []
    for entry in entries:
        author = entry[0]
        post = datetime.datetime.strptime(entry[3], '%Y/%m/%d %H:%M').strftime('%Y/%m/%d %H:%M')
        link = url
        title = entry[1]
        text = entry[2]
        result.append([post, author, title, text, link])
    return result
