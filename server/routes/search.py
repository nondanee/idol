import asyncio
import base64
from aiohttp import web

@asyncio.coroutine
def route(request):

    query_string = request.rel_url.query

    try:
        url = base64.urlsafe_b64decode(query_string['url'])
    except:
        return web.HTTPBadRequest()


    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()

        yield from cursor.execute(
            'select server, location from proxy where url = %s',
            (url,)
        )

        data = yield from cursor.fetchone()
        yield from cursor.close()
        connect.close()

        if not data:
            return web.HTTPNotFound()

        redirect = 'http://' + [
            '45.32.60.5:3000/dev/',
            '45.32.60.5:3000/lts/',
            '198.13.49.113:3000/legacy/'
        ][data[0]] + data[1]

        return web.HTTPFound(redirect)