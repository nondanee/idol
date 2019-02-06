import asyncio
from . import tool
from aiohttp import web
from aiohttp_session import get_session

@asyncio.coroutine
def all(request):

    session = yield from get_session(request)
    query_string = request.rel_url.query

    if 'uid' not in session:
        uid = 0
        # return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    page, size = tool.paging_parse(query_string)

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor() 

        yield from cursor.execute('''
            select
            cut.id,
            cut.post,
            cut.mid,
            cut.title,
            cut.snippet,
            cut.thumbnail,
            cut.favors,
            cut.romaji,
            cut.name,
            favor.uid
            from(
                select
                feed.id,
                feed.post,
                feed.mid,
                feed.title,
                feed.snippet,
                feed.thumbnail,
                feed.favors,
                member.romaji,
                member.name
                from feed, member
                where feed.mid = member.id
                order by feed.post desc, feed.mid desc
                limit %s, %s
            ) cut
            left join favor on favor.uid = %s and favor.fid = cut.id
        ''', ((page - 1) * size, size, uid))

        data = yield from cursor.fetchall()
        yield from cursor.close()
        connect.close()

        json_body = []

        for blog in data:

            json_body.append({
                'fid': str(blog[0]).zfill(7),
                'author': {
                    'mid': str(blog[2]).zfill(4),
                    'name': blog[8],
                    'romaji': blog[7],
                    'avatar': tool.avatar_locate(blog[2], blog[7]),
                    'affiliation': tool.member_affiliate(blog[2])
                },
                'post': tool.time_utc(blog[1]),
                'title': blog[3],
                'snippet': blog[4],
                'thumbnail': tool.thumb_locate(blog[0], blog[5]),
                'favored': True if blog[9] else False,
                'favors': blog[6]
            })

        return web.Response(
            text = tool.jsonify(json_body),
            content_type = 'application/json',
            charset = 'utf-8'
        )


@asyncio.coroutine
def follow(request):

    session = yield from get_session(request)
    query_string = request.rel_url.query

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    page, size = tool.paging_parse(query_string)

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor() 

        yield from cursor.execute('''
            select
            cut.id,
            cut.post,
            cut.mid,
            cut.title,
            cut.snippet,
            cut.thumbnail,
            cut.favors,
            cut.romaji,
            cut.name,
            favor.uid
            from(
                select
                feed.id,
                feed.post,
                feed.mid,
                feed.title,
                feed.snippet,
                feed.thumbnail,
                feed.favors,
                member.romaji,
                member.name
                from feed, member
                where feed.mid in (
                    select 
                    mid
                    from follow
                    where uid = %s
                )
                and feed.mid = member.id
                order by feed.post desc, feed.mid desc
                limit %s, %s
            ) cut
            left join favor on favor.uid = %s and favor.fid = cut.id
        ''', (uid, (page - 1) * size, size, uid))

        data = yield from cursor.fetchall()
        yield from cursor.close()
        connect.close()

        json_body = []

        for blog in data:

            json_body.append({
                'fid': str(blog[0]).zfill(7),
                'author': {
                    'mid': str(blog[2]).zfill(4),
                    'name': blog[8],
                    'romaji': blog[7],
                    'avatar': tool.avatar_locate(blog[2], blog[7]),
                    'affiliation': tool.member_affiliate(blog[2])
                },
                'post': tool.time_utc(blog[1]),
                'title': blog[3],
                'snippet': blog[4],
                'thumbnail': tool.thumb_locate(blog[0], blog[5]),
                'favored': True if blog[9] else False,
                'favors': blog[6]
            })

        return web.Response(
            text = tool.jsonify(json_body),
            content_type = 'application/json',
            charset = 'utf-8'
        )

@asyncio.coroutine
def favor(request):

    session = yield from get_session(request)
    query_string = request.rel_url.query

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    page, size = tool.paging_parse(query_string)

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor() 

        yield from cursor.execute('''
            select
            cut.id,
            cut.post,
            cut.mid,
            cut.title,
            cut.snippet,
            cut.thumbnail,
            cut.favors,
            cut.romaji,
            cut.name,
            favor.uid
            from(
                select
                feed.id,
                feed.post,
                feed.mid,
                feed.title,
                feed.snippet,
                feed.thumbnail,
                feed.favors,
                member.romaji,
                member.name
                from feed, member
                where feed.id in (
                    select 
                    fid
                    from favor
                    where uid = %s
                ) 
                and feed.mid = member.id
                order by feed.post desc, feed.mid desc
                limit %s, %s
            ) cut
            left join favor on favor.uid = %s and favor.fid = cut.id
        ''', (uid, (page - 1) * size, size, uid))

        data = yield from cursor.fetchall()
        yield from cursor.close()
        connect.close()

        json_body = []

        for blog in data:

            json_body.append({
                'fid': str(blog[0]).zfill(7),
                'author': {
                    'mid': str(blog[2]).zfill(4),
                    'name': blog[8],
                    'romaji': blog[7],
                    'avatar': tool.avatar_locate(blog[2], blog[7]),
                    'affiliation': tool.member_affiliate(blog[2])
                },
                'post': tool.time_utc(blog[1]),
                'title': blog[3],
                'snippet': blog[4],
                'thumbnail': tool.thumb_locate(blog[0], blog[5]),
                'favored': True if blog[9] else False,
                'favors': blog[6]
            })

        return web.Response(
            text = tool.jsonify(json_body),
            content_type = 'application/json',
            charset = 'utf-8'
        )

@asyncio.coroutine
def member(request):

    session = yield from get_session(request)
    query_string = request.rel_url.query
    mid = request.match_info['mid']

    if 'uid' not in session:
        uid = 0
        # return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    try:
        mid = int(mid)
    except:
        return web.HTTPBadRequest()

    page, size = tool.paging_parse(query_string)

    with (yield from request.app['pool']) as connect:

        cursor = yield from connect.cursor() 

        yield from cursor.execute('''
            select
            cut.id,
            cut.post,
            cut.mid,
            cut.title,
            cut.snippet,
            cut.thumbnail,
            cut.favors,
            cut.romaji,
            cut.name,
            favor.uid
            from(
                select
                feed.id,
                feed.post,
                feed.mid,
                feed.title,
                feed.snippet,
                feed.thumbnail,
                feed.favors,
                member.romaji,
                member.name
                from feed, member
                where feed.mid = %s
                and feed.mid = member.id
                order by feed.post desc, feed.mid desc
                limit %s, %s
            ) cut
            left join favor on favor.uid = %s and favor.fid = cut.id
        ''', (mid, (page - 1) * size, size, uid))

        data = yield from cursor.fetchall()
        yield from cursor.close()
        connect.close()

        json_body = []

        for blog in data:

            json_body.append({
                'fid': str(blog[0]).zfill(7),
                'author': {
                    'mid': str(blog[2]).zfill(4),
                    'name': blog[8],
                    'romaji': blog[7],
                    'avatar': tool.avatar_locate(blog[2], blog[7]),
                    'affiliation': tool.member_affiliate(blog[2])
                },
                'post': tool.time_utc(blog[1]),
                'title': blog[3],
                'snippet': blog[4],
                'thumbnail': tool.thumb_locate(blog[0], blog[5]),
                'favored': True if blog[9] else False,
                'favors': blog[6]
            })

        return web.Response(
            text = tool.jsonify(json_body),
            content_type = 'application/json',
            charset = 'utf-8'
        )