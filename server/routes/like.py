import asyncio
import json
from aiohttp import web
from aiohttp_session import get_session

@asyncio.coroutine
def create(request):

    session = yield from get_session(request)
    query_string = request.rel_url.query

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    try:
        fid = int(query_string['fid'])
    except:
        return web.HTTPBadRequest()

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()

        try:
            yield from cursor.execute(
                'insert into favor values (%s, %s)',
                (uid, fid)
            )
        except Exception as error:
            print(error)
            yield from cursor.close()
            connect.close()
            if error.args[1].find('member') != -1:
                return web.HTTPBadRequest()
            elif error.args[1].find('feed') != -1:
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
def destroy(request):

    session = yield from get_session(request)
    query_string = request.rel_url.query

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    try:
        fid = int(query_string['fid'])
    except:
        return web.HTTPBadRequest()

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()

        deleted = yield from cursor.execute(
            'delete from favor where uid = %s and fid = %s',
            (uid, fid)
        )
        yield from connect.commit()
        yield from cursor.close()
        connect.close()

        if deleted:
            return web.HTTPOk()
        else:
            return web.HTTPBadRequest()