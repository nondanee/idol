import asyncio
import datetime
from aiohttp import web
from aiohttp_session import get_session

@asyncio.coroutine
def route(request):

    session = yield from get_session(request)

    user_agent = request.headers['User-Agent']
    ip_address = request.headers['Remote-Host'] if 'Remote-Host' in request.headers else request.remote

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()

        if 'uid' not in session:

            try:
                yield from cursor.execute(
                    'insert into user values(null, now(), %s, %s, "")',
                    (ip_address, user_agent)
                )
                yield from cursor.execute('select last_insert_id()')
                (uid,) = yield from cursor.fetchone()
                session['uid'] = uid
            except Exception as error:
                print(error)
                return web.HTTPInternalServerError()

        else:

            uid = session['uid']
            try:
                updated = yield from cursor.execute(
                    'update user set last_active = now(), ip_address = %s, user_agent = %s where id = %s',
                    (ip_address, user_agent, uid)
                )
            except Exception as error:
                print(error)
                return web.HTTPInternalServerError()

            if updated:
                session['uid'] = uid
            else:
                session.clear()

        yield from connect.commit()
        yield from cursor.close()
        connect.close()

        return web.HTTPNoContent()