# -*- coding: utf-8 -*-

import re, operator
import member, source, tool, photo, translate, push

def indicator(*args):
    pass
    print(' '.join(map(str, args)))

def nogizaka_only(page = 1):
    blogs = source.from_nogizaka_pc_site(page)
    blogs.sort(key = operator.itemgetter(0), reverse = False)
    return blogs
    
def keyakizaka_only(page = 1):
    blogs = source.from_keyakizaka_pc_site(page)
    blogs.sort(key = operator.itemgetter(0), reverse = False)
    return blogs

def hinatazaka_only(page = 1):
    blogs = source.from_hinatazaka_pc_site(page)
    blogs.sort(key = operator.itemgetter(0), reverse = False)
    return blogs

def all():
    blogs = source.from_keyakizaka_pc_site()
    blogs += source.from_nogizaka_rss()
    blogs += source.from_hinatazaka_pc_site()
    blogs.sort(key = operator.itemgetter(0), reverse = False)
    return blogs

def deal(connect, blogs):
    fresh = []
    cursor = connect.cursor()
    for blog in blogs:
    
        post = blog[0]
        author = blog[1]
        title = blog[2]
        html = blog[3]
        url = blog[4]
    
        feed_id = tool.get_feed_id(url)
        if cursor.execute('select * from feed where id = %s', (feed_id,)) != 0: continue

        url = tool.truncate_url(url)
        text = tool.purify_text(html)
        title = tool.purify_text(title)
        snippet = tool.clip_text(text)

        author = member.bind(author, feed_id)
        author, title = member.identify(author, title)

        member_id = member.get_id(author)
        romaji = member.get_romaji(author)

        indicator('{} {}'.format(author, title))
    
        try:
            cursor.execute('insert into feed values(%s, %s, %s, %s, %s, %s, %s, %s)', (feed_id, post, member_id, url, title, snippet, False, 0))
        except Exception as e:
            indicator('feed insert', e)
        else:
            connect.commit()
            indicator('list save')
    
        (text, thumbnail, images) = photo.process({'feed_id': feed_id, 'romaji': romaji,'post': post}, text)

        try:
            cursor.executemany('insert into photo values({}, %s, %s, %s, %s, %s, %s)'.format(feed_id), images)
        except Exception as e:
            indicator('photo insert', e)
        else:
            connect.commit()
            indicator('photo save')
    
        try:
            cursor.execute('update feed set thumbnail = %s where id = %s', (thumbnail, feed_id))
        except Exception as e:
            indicator('feed update', e)
        else:
            connect.commit()
            indicator('cover update')
        
        title_translated = translate.translate(title)
        text_translated = translate.translate(text)
    
        try:
            cursor.execute('insert into blog values(%s, %s, %s, %s, %s)', (feed_id, text, title_translated, text_translated, html))
        except Exception as e:
            indicator('blog insert', e)
        else:
            connect.commit()
            indicator('blog save')

        fresh.append(feed_id)
    
    cursor.close()
    
    # push.firebase(connect, fresh)
