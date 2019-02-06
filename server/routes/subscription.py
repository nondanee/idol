import asyncio
from aiohttp import web
from aiohttp_session import get_session

@asyncio.coroutine
def prepare(request):

    session = yield from get_session(request)
    query_string = request.rel_url.query

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    try:
        end_point = query_string['end_point']
    except:
        return web.HTTPBadRequest()

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()
        updated = yield from cursor.execute(
            'update user set end_point = %s where id = %s',
            (end_point, uid)
        )
        yield from connect.commit()
        yield from cursor.close()
        connect.close()

        if updated:
            return web.HTTPOk()
        else:
            return web.HTTPOk()


@asyncio.coroutine
def confirm(request):

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
                'insert into subscription values (%s, %s)',
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
def cancel(request):

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

        cancelled = yield from cursor.execute(
            'delete from subscription where uid = %s and mid = %s',
            (uid, mid)
        )
        yield from connect.commit()
        yield from cursor.close()
        connect.close()

        if cancelled:
            return web.HTTPOk()
        else:
            return web.HTTPBadRequest()