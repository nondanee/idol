import asyncio
from . import tool
from aiohttp import web
from aiohttp_session import get_session

@asyncio.coroutine
def route(request):

    session = yield from get_session(request)
    query_string = request.rel_url.query

    if 'uid' not in session:
        uid = 0
#         return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    try:
        mid = int(query_string['mid'])
    except:
        return web.HTTPBadRequest()

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()

        yield from cursor.execute('''
            select
            overview.id,
            overview.romaji,
            overview.name,
            overview.introduction,
            overview.follows,
            overview.subscribes,
            follow.uid,
            subscription.uid
            from (
                select
                member.id,
                member.romaji,
                member.name,
                member.introduction,
                member.follows,
                member.subscribes
                from member
                where member.id = %s
            ) overview
            left join follow on follow.uid = %s and follow.mid = overview.id
            left join subscription on subscription.uid = %s and subscription.mid = overview.id
        ''', (mid, uid, uid))

        data = yield from cursor.fetchone()
        yield from cursor.close()
        connect.close()

        if not data:
            return web.HTTPNotFound()

        json_body = {
            'mid': str(data[0]).zfill(4),
            'avatar': tool.avatar_locate(data[0], data[1]),
            'name': data[2],
            'romaji': data[1],
            'affiliation': tool.member_affiliate(data[0]),
            'introduction': data[3],
            'follows': data[4],
            'subscribes': data[5],
            'followed': True if data[6] else False,
            'subscribed': True if data[7] else False
        }

        return web.Response(
            text = tool.jsonify(json_body),
            content_type = 'application/json',
            charset = 'utf-8'
        )