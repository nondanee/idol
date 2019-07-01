import asyncio
import json, datetime
from aiohttp import web

@asyncio.coroutine
def route(request):

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor()

        yield from cursor.execute('''
            select
            member.id,
            member.romaji,
            member.name,
            history.last_update
            from member
            left join (
                select
                mid,
                max(post) as last_update
                from feed
                group by mid
            ) history
            on member.id = history.mid
        ''')
        data = yield from cursor.fetchall()

        yield from cursor.close()
        connect.close()

        return web.Response(text = str(data))
