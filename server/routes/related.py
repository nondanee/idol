import asyncio
from . import tool
from aiohttp import web
from aiohttp_session import get_session

@asyncio.coroutine
def route(request):

    fid = request.match_info['fid']

    session = yield from get_session(request)

    if 'uid' not in session:
        uid = -1
    else:
        uid = session['uid']

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()

        yield from cursor.execute('''
            select
            cut.id,
            cut.post,
            cut.mid,
            cut.title,
            cut.thumbnail,
            cut.favors,
            cut.name,
            cut.romaji,
            favor.uid
            from(
                select 
                feed.id,
                feed.post,
                feed.mid,
                feed.title,
                feed.thumbnail,
                feed.favors,
                member.name,
                member.romaji
                from feed, member
                where feed.mid = (
                    select 
                    feed.mid 
                    from feed
                    where feed.id = %s
                )
                and feed.mid = member.id
                and feed.id < %s
                order by feed.post desc
                limit 0, 10
            ) cut
            left join favor on favor.uid = %s and favor.fid = cut.id
        ''', (fid, fid, uid))

        data = yield from cursor.fetchall()
        yield from cursor.close()
        connect.close()

        if not data:
            return web.HTTPNotFound()

        json_body = []

        for blog in data:

            json_body.append({
                'fid': str(blog[0]).zfill(7),
                'author':{
                    'mid': str(blog[2]).zfill(4),
                    'name': blog[6],
                    'romaji': blog[7],
                    'avatar': tool.avatar_locate(blog[2], blog[7])
                },
                'post': tool.time_utc(blog[1]),
                'title': blog[3],
                'thumbnail': tool.thumb_locate(blog[0], blog[4]),
                'favored': True if blog[8] else False,
                'favors': blog[5]
            })

        return web.Response(
            text = tool.jsonify(json_body),
            content_type = 'application/json',
            charset = 'utf-8'
        )