import asyncio
import re, time
from . import tool
from aiohttp import web

@asyncio.coroutine
def route(request):

    query_string = request.rel_url.query
    page, size = tool.paging_parse(query_string)
    condition = ''
    
    if 'member' in query_string:
        if re.search(r'^[a-z|-]+$', query_string['member']):
            condition = 'and member.romaji = "{}"'.format(query_string['member'])
        else:
            return web.HTTPBadRequest()

    if 'group' in query_string:
        if query_string['group'] == 'nogizaka':
            condition = 'and feed.id < 1000000'
        elif query_string['group'] == 'keyakizaka':
            condition = 'and feed.id > 1000000'

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor() 

        yield from cursor.execute('''
            select
            feed.id,
            feed.post,
            feed.title,
            feed.snippet,
            member.name
            from feed, member
            where feed.mid = member.id
            {}
            order by feed.post desc, feed.mid desc
            limit %s, %s
        '''.format(condition), ((page - 1) * size, size))

        data = yield from cursor.fetchall()
        yield from cursor.close()
        connect.close()

        json_body = []

        for blog in data:

            json_body.append({
                'summary': blog[3],
                'url': 'https://aidoru.tk/blog/{}'.format(str(blog[0]).zfill(7)),
                'post': int(time.mktime(blog[1].timetuple())) - 9 * 3600,
                'author': blog[4],
                'title': blog[2]
            })

        return web.Response(
            text = tool.jsonify(json_body),
            content_type = 'application/json',
            charset = 'utf-8'
        )
