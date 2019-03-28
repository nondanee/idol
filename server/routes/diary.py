import asyncio
from . import tool
from aiohttp import web
from aiohttp_session import get_session

@asyncio.coroutine
def route(request):

    fid = request.match_info['fid']

    session = yield from get_session(request)

    if 'uid' not in session:
        uid = 0
    else:
        uid = session['uid']

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()

        yield from cursor.execute('''
            select
            target.id,
            target.post,
            target.mid,
            member.name,
            member.romaji,
            target.link,
            target.title,
            target.favors,
            blog.text_original,
            favor.uid
            from (
                select
                feed.id,
                feed.post,
                feed.mid,
                feed.link,
                feed.title,
                feed.favors
                from feed
                where feed.id = %s
            ) target
            inner join blog on blog.id = target.id
            inner join member on member.id = target.mid
            left join favor on favor.uid = %s and favor.fid = target.id
        ''', (fid, uid))

        data = yield from cursor.fetchone()
        yield from cursor.close()
        connect.close()

        if not data:
            return web.HTTPNotFound()

        json_body = {
            'fid': str(data[0]).zfill(7),
            'post': tool.time_utc(data[1]),
            'author': {
                'mid': str(data[2]).zfill(4),
                'name': data[3],
                'romaji': data[4],
                'affiliation': tool.member_affiliate(data[2]),
                'avatar': tool.avatar_locate(data[2], data[4])
            },
            'title': data[6],
            'link': data[5],
            'favored': True if data[9] else False,
            'favors': data[7],
            'text': tool.photo_locate(data[4], data[1], data[0], data[8])
        }

        return web.Response(
            text = tool.jsonify(json_body),
            content_type = 'application/json',
            charset = 'utf-8'
        )


@asyncio.coroutine
def legacy(request):

    fid = request.match_info['fid']

    session = yield from get_session(request)

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()

        yield from cursor.execute('''
            select
            target.post,
            target.mid,
            member.name,
            member.romaji,
            target.link,
            target.title,
            blog.text_original,
            blog.title_translated,
            blog.text_translated
            from (
                select
                feed.id,
                feed.post,
                feed.mid,
                feed.link,
                feed.title
                from feed
                where feed.id = %s
            ) target
            inner join blog on blog.id = target.id
            inner join member on member.id = target.mid
        ''', (fid,))

        data = yield from cursor.fetchone()
        yield from cursor.close()
        connect.close()

        if not data:
            return web.HTTPNotFound()

        json_body = {
            'fid': fid,
            'post': tool.time_utc(data[0]),
            'author': {
                'mid': str(data[1]).zfill(4),
                'name': data[2],
                'avatar': tool.avatar_locate(data[1], data[3])
            },
            'title': [data[5], data[7]],
            'article': [
                tool.photo_locate(data[3], data[0], fid, data[6]), 
                tool.photo_locate(data[3], data[0], fid, data[8])
            ],
            'link': data[4]
        }

        return web.Response(
            text = template.format(data[5], data[2], tool.jsonify(json_body)),
            content_type = 'text/html',
            charset = 'utf-8'
        )

template = '''
<!DOCTYPE html>
<html>
<head>
    <title>{} | {} | idol</title>
    <meta charset="UTF-8">
    <meta name="theme-color" content="#ffffff">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link rel="manifest" href="/manifest.json">
    <link rel="shortcut icon" sizes="144x144" href="/static/logo/144.png">
    <link rel="stylesheet" type="text/css" href="/static/css/pwa-view.css">
</head>
<body>
    <div id="topbar">
        <button id="back"></button>
        <div class="fill"></div>
        <button id="translate"></button>
        <button id="link"></button>
    </div>
</body>
<script>const shareData = {}</script>
<script type="text/javascript" src="/static/js/view.js"></script>
</html>
'''