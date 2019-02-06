import asyncio
from . import tool
from aiohttp import web
from aiohttp_session import get_session

@asyncio.coroutine
def manifest(request):

    session = yield from get_session(request)

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()

        yield from cursor.execute('''
            select
            member.id,
            member.romaji,
            member.name,
            member.follows,
            member.subscribes,
            follow.uid,
            subscription.uid
            from member
            left join follow on follow.uid = %s and follow.mid = member.id
            left join subscription on subscription.uid = %s and subscription.mid = member.id
        ''', (uid, uid))

        data = yield from cursor.fetchall()
        yield from cursor.close()
        connect.close()

        if not data:
            return web.HTTPNotFound()

        json_body = []

        for member in data:

            json_body.append({
                'mid': str(member[0]).zfill(4),
                'name': member[2],
                'romaji': member[1],
                'avatar': tool.avatar_locate(member[0], member[1]),
                'affiliation': tool.member_affiliate(member[0]),
                'followed': True if member[5] else False,
                'subscribed': True if member[6] else False,
                'follows': member[3],
                'subscribes': member[4]
            })

        return web.Response(
            text = tool.jsonify(json_body),
            content_type = 'application/json',
            charset = 'utf-8'
        )

@asyncio.coroutine
def add(request):

    session = yield from get_session(request)
    query_string = request.rel_url.query

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    try:
        mid = int(query_string['mid'])
    except:
        return web.HTTPBadRequest()

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()

        try:
            yield from cursor.execute(
                'insert into follow values (%s, %s)',
                (uid, mid)
            )
        except Exception as error:
            print(error)
            yield from cursor.close()
            connect.close()
            if error.args[1].find('member') != -1:
                return web.HTTPBadRequest()
            elif error.args[1].find('user') != -1:
                session.clear()
                return web.HTTPBadRequest()
            elif error.args[1].find('Duplicate') != -1:
                return web.HTTPOk()
        else:
            yield from connect.commit()
            yield from cursor.close()
            connect.close()

            return web.HTTPOk()


@asyncio.coroutine
def remove(request):

    session = yield from get_session(request)
    query_string = request.rel_url.query

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    try:
        mid = int(query_string['mid'])
    except:
        return web.HTTPBadRequest()

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()

        deleted = yield from cursor.execute(
            'delete from follow where uid = %s and mid = %s',
            (uid, mid)
        )
        yield from connect.commit()
        yield from cursor.close()
        connect.close()

        if deleted:
            return web.HTTPOk()
        else:
            return web.HTTPBadRequest()