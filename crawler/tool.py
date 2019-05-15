# -*- coding: utf-8 -*-

import re, html.parser

def truncate_url(url):

    return re.sub(r'\?.*$', '', url)

def get_feed_id(url):

    if url.find('nogizaka46') != -1:
        fid = '0' + re.search(r'\d{4}/\d{2}/(\d{6})', url).group(1).zfill(6)
    elif url.find('keyakizaka46') != -1 or url.find('hinatazaka46') != -1:
        fid = '1' + re.search(r'diary/detail/(\d+)', url).group(1).zfill(6)
    return fid

def purify_text(text):

    text = text.replace('\u3000', '\xa0')
    text = text.replace('&nbsp;', '\xa0')

#     text = re.sub(r'\r|\n', '', text)
    text = re.sub(r'\s+', ' ', text)

    text = re.sub(r'<p[^>]*>[\s|\xa0]+</p>', '\n', text)
    text = re.sub(r'<div[^>]*>[\s|\xa0]+</div>', '\n', text)
    text = re.sub(r'<div[^>]*><span[^>]*>[\s|\xa0]*<br[^>]*>[\s|\xa0]*</span></div>', '\n', text)
    text = re.sub(r'<p[^>]*><span[^>]*>[\s|\xa0]*<br[^>]*>[\s|\xa0]*</span></p>', '\n', text)
    text = re.sub(r'<div[^>]*>[\s|\xa0]*<br[^>]*>[\s|\xa0]*</div>', '\n', text)

    text = re.sub(r'<p[^>]*>\s*</p>', '', text)
    text = re.sub(r'<div[^>]*>\s*</div>', '', text)

    text = re.sub(r'<p[^>]*>([\s\S]+?)</p>', '\g<1>\n', text)
    text = re.sub(r'<div[^>]*>([\s\S]+?)</div>', '\g<1>\n', text)

    regexp_awalker = re.compile(r'<a href="(http://dcimg.awalker.jp/[^"]+)"[^>]*><img\s[^>]*src="([^"]+)"[^>]*></a>')

    while regexp_awalker.search(text) != None: text = regexp_awalker.sub('![](\g<1>)', text)

    text = re.sub(r'<a href="http://blog.nogizaka46.com/staff/img/([^"]+)"[^>]*>[^<]*<img[^>]+>', '![](http://img.nogizaka46.com/blog/staff/img/\g<1>)', text)
    text = re.sub(r'<a href="http://img.nogizaka46.com/([^"]+)"[^>]*>[^<]*<img[^>]+>', '![](http://img.nogizaka46.com/\g<1>)', text)

    # text = re.sub(r'<(?!(br|img))[\s\S]+?>', "", text)
    # text = re.sub(r'<(?!(br|img))[^<>]+?>', "", text) # very important

    text = re.sub(r'<br[^>]*>', '\n', text)
    text = re.sub(r'<img\s[^>]*src=""[^>]*>', '', text)
    text = re.sub(r'<img\s[^>]*src="([^"]+)"[^>]*>', '![](\g<1>)', text)
    text = re.sub(r'<img\s[^>]*src="(/files/[^"]+)"[^>]*>', '![](http://www.keyakizaka46.com\g<1>)', text)
    text = re.sub(r'<[^<>]+?>', '', text)

    text = re.sub(r'[\s|\xa0]*?\n[\s|\xa0]*?', '\n', text)
    text = re.sub(r'^[\s|\xa0]*\n*', '', text)
    text = re.sub(r'\n*[\s|\xa0]*$', '', text)

    text = '\n'.join(map(str.strip, text.split('\n')))

    return html.parser.HTMLParser().unescape(text)

def clip_text(text):

    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\!\[[^\]]*\]\([^\)]+\)', ' ', text)
    text = re.sub(r'http://', '', text)
    text = re.sub(r'https://', '', text)
    text = re.sub(r'\s|\xa0', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^\s+', '', text)

    snippet = text[0:60]
    snippet = re.sub(r'\s$', '', snippet)

    return snippet
