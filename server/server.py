import asyncio
import aiohttp
import aiomysql
import re
import json
import datetime
from aiohttp import web


def timefriendly(timeset):

    cntime = timeset - datetime.timedelta(hours = 1)
    visit = datetime.datetime.now() - datetime.timedelta(hours = 1) #GMT + 8

    if cntime.date() == visit.date():
    # if (visit - cntime).days==0:
        subtime = (visit - cntime).seconds
        if subtime//60 == 0:
            if subtime == 0:
                timeinfo = "just now"
            else:
                timeinfo = "%s secs ago"%(subtime)
        elif subtime//60 <= 59:
            timeinfo = "%s mins ago"%(subtime//60)
        # elif subtime//3600<=12:
        else:
            timeinfo = "%s hours ago"%(subtime//3600)
        # else:
        #     timeinfo=cntime.strftime('%m.%d %H:%M')
    else:
        timeinfo = cntime.strftime('%Y/%m/%d %H:%M')

    if re.search(r'^1 ',timeinfo)!=None:
        timeinfo = re.sub(r'secs','sec',timeinfo)
        timeinfo = re.sub(r'mins','min',timeinfo)
        timeinfo = re.sub(r'hours','hour',timeinfo)

    if re.search(":",timeinfo)!=None:
        # timeinfo=re.sub(r'(?<!\d)0','',timeinfo)
        timeinfo = re.sub(r'(?<!\d)0+([123456789])(?!$)','\g<1>',timeinfo)

    return timeinfo

def timeutc(timeset):
    
    # jptime = timeset.replace(tzinfo=pytz.timezone("Asia/Tokyo"))
    jptime = pytz.timezone('Asia/Tokyo').localize(timeset)
    utctime = jptime.astimezone(pytz.utc)
    timeinfo = utctime.strftime("%Y-%m-%dT%H:%M:%SZ")

    return timeinfo


@asyncio.coroutine
def create_pool():
    global pool
    pool = yield from aiomysql.create_pool(host='127.0.0.1', port=3306,
                                           user='*???*', password='*???*',
                                           db='*???*', loop=loop,
                                           charset='utf8')

@asyncio.coroutine
def index(request):

    query_parameter=request.rel_url.query

    if "page" in query_parameter:
        if re.search(r'^\d+$',query_parameter["page"])!=None:
            page = int(query_parameter["page"])
            if page < 2:
                return web.HTTPBadRequest()
        else:
            return web.HTTPBadRequest()
    else:
        page = 1

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        judge = yield from cur.execute('SELECT post,rome,author,title,brief FROM list ORDER BY post DESC,kana DESC LIMIT %s,20'%((page - 1) * 20))
        
        if judge == 0:
            yield from cur.close()
            conn.close()
            jsonback = {"content":"","more":0}
            return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')
        else:
            out = yield from cur.fetchall()
            yield from cur.close()
            conn.close()

    more = 1 if len(out) == 20 else 0
    content = ""

    for onepost in out:

        link = '/' + onepost[1] + '/' + onepost[0].strftime('%Y%m%d%H%M')
        # timeinfo = timefriendly(onepost[0])
        timedata = timeutc(onepost[0])
        
        card='''
        <div class="card" onclick="window.location.href='{link}'">
            <div class="line">
                <div class="avatar" style="background-image:url(/avatar/{rome}.jpg)"></div>
                <span class="info">
                    <span class="author">{author}</span> · 
                    <span class="post" data-post="{timedata}"></span>
                </span>
            </div>
            <div class="title">{title}</div>
            <div class="brief">{brief}</div>
        </div> '''.format(link = link,rome = onepost[1],author = onepost[2],timedata = timedata,title = onepost[3],brief = onepost[4])

        content = content + card


    html='''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>idol</title>
<meta name="theme-color" content="#eeeeee">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<link rel="manifest" href="/manifest.json">
<link rel="icon" sizes="144x144" href="/static/logo/144.png">
<link rel="apple-touch-icon-precomposed" href="/static/apple_launcher.png">
<link rel="stylesheet" type="text/css" href="/static/css/pwa-main.css" />
</head>
<body>
<div id="topbar" onclick="pagescroll()">
	<div id="logo"></div>
	<div id="app">idol</div>
	<div id="about" onclick="event.cancelBubble=true;window.location.href='/about'"></div>
	<div id="member" onclick="event.cancelBubble=true;window.location.href='/group'"></div>
</div>
<div id="content">%s
</div>
<div id="loading"></div>
</body>
<script src="https://cdn.bootcss.com/moment.js/2.18.1/moment.min.js"></script>
<script src="/static/js/main.js"></script>
</html>
'''


    if page == 1:
        return web.Response(text=html%content,content_type='text/html',charset='utf-8')
    else:
        jsonback = {"content":content,"more":more}
        return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')


    

@asyncio.coroutine
def view(request):
    
    rome = request.match_info["name"]
    if rome not in {"iguchi-mao":"","ushio-sarina":"","kakizaki-memi":"","kageyama-yuuka":"","katou-shiho":"","saitou-kyouko":"","sasaki-kumi":"","sasaki-mirei":"","takase-mana":"","takamoto-ayaka":"","nagahama-neru":"","higashimura-mei":"","ishimori-nijika":"","imaizumi-yui":"","uemura-rina":"","ozeki-rika":"","oda-nana":"","koike-minami":"","kobayashi-yui":"","saitou-fuyuka":"","satou-shiori":"","shida-manaka":"","sugai-yuuka":"","suzumoto-miyu":"","nagasawa-nanako":"","habu-mizuho":"","harada-aoi":"","hirate-yurina":"","moriya-akane":"","yonetani-nanami":"","watanabe-rika":"","watanabe-risa":"","akimoto-manatsu":"","ikuta-erika":"","ikoma-rina":"","itou-marika":"","inoue-sayuri":"","etou-misa":"","kawago-hina":"","kawamura-mahiro":"","saitou-asuka":"","saitou-chiharu":"","saitou-yuuri":"","sakurai-reika":"","shiraishi-mai":"","takayama-kazumi":"","nakada-kana":"","nakamoto-himeka":"","nishino-nanase":"","noujou-ami":"","hashimoto-nanami":"","higuchi-hina":"","hoshino-minami":"","matsumura-sayuri":"","wakatsuki-yumi":"","wada-maaya":"","itou-karin":"","itou-junna":"","kitano-hinako":"","sagara-iori":"","sasaki-kotoko":"","shinuchi-mai":"","suzuki-ayane":"","terada-ranze":"","hori-miona":"","yamazaki-rena":"","watanabe-miria":"","itou-riria":"","iwamoto-renka":"","umezawa-minami":"","oozono-momoko":"","kubo-shiori":"","sakaguchi-tamami":"","satou-kaede":"","nakamura-reno":"","mukai-hazuki":"","yamashita-mizuki":"","yoshida-ayano-christie":"","yoda-yuuki":"","unei-sutaffu":""}:
        return web.HTTPNotFound()

    time = request.match_info["time"]
    post = time[0:4]+"/"+time[4:6]+"/"+time[6:8]+" "+time[8:10]+":"+time[10:12]

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        judge = yield from cur.execute('SELECT team,post,rome,author,link,title_original,title_translation,text_original,text_translation FROM blog WHERE post = "%s" AND rome = "%s";'%(post,rome))
        
        if judge == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPNotFound()
        else:
            out = yield from cur.fetchall()
            yield from cur.close()
            conn.close()

    today = datetime.date.today() - datetime.timedelta(hours = 1) #GMT + 8
    yesterday = today - datetime.timedelta(1)

    displaytime = out[0][1] - datetime.timedelta(hours=1)

    if displaytime.date() == today:
        jptimeinfo = '今日' + displaytime.strftime(' %H:%M')
        cntimeinfo = '今天' + displaytime.strftime(' %H:%M')
    elif displaytime.date() == yesterday:
        jptimeinfo = '昨日' + displaytime.strftime(' %H:%M')
        cntimeinfo = '昨天' + displaytime.strftime(' %H:%M')
    else:
        jptimeinfo = displaytime.strftime('%m/%d %H:%M')
        cntimeinfo = displaytime.strftime('%m/%d %H:%M')

    jptext = out[0][7]
    cntext = out[0][8]

    while re.search("hostpath",jptext) != None:
        jptext = re.sub('hostpath',"/photo",jptext)

    while re.search("hostpath",cntext) != None:
        cntext = re.sub('hostpath',"/photo",cntext)
    
    if out[0][0] == 0:
        groupname = 'NOGI'
    elif out[0][0] == 1: 
        groupname = 'KEYAKI'
    
    html='''<!DOCTYPE html>
<html>
<head>
<title>%s</title>
<meta charset="UTF-8" />
<meta name="theme-color" content="#ffffff">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
<meta name="mobile-web-app-capable" content="yes">
<link rel="manifest" href="/manifest.json">
<link rel="stylesheet" type="text/css" href="/static/css/pwa-view.css" />
<script type="text/javascript" src="/static/js/view.js"></script>
</head>
<body>
    <div id="topbar" onclick="pageScroll();"><div id="back" onclick="event.cancelBubble=true;javascript:history.back(-1);"></div><div id="link" onclick="event.cancelBubble=true;window.location.href='%s'"></div><div id="translate" onclick="event.cancelBubble=true;viewSwitch()"></div></div>
    %s
    %s
</body>
</html>'''


    article='''
    <div class ="text %s" id="%s">
        <div class="head"><div class="avatar" style="background-image:url(/avatar/%s.jpg)"></div></div>
        <div class="title">%s</div>
        <div class="infor">%s · %s · %s</div>
        <div class="depart">————&nbsp;&nbsp;&nbsp;&nbsp;~&nbsp;&nbsp;&nbsp;&nbsp;————</div>
        <div class="article">%s</div>
	<div class="footer"></div>
    </div>'''

    article_original = article%("focus","ja-jp",out[0][2],out[0][5],out[0][3],groupname,jptimeinfo,jptext)
    article_translation = article%("unfocus","zh-cn",out[0][2],out[0][6],out[0][3],groupname,cntimeinfo,cntext)
    html = html%(out[0][5],out[0][4],article_original,article_translation)

    return web.Response(text=html,content_type='text/html',charset='utf-8')

@asyncio.coroutine
def member(request):

    rome = request.match_info["name"]
    if rome not in {"iguchi-mao":"","ushio-sarina":"","kakizaki-memi":"","kageyama-yuuka":"","katou-shiho":"","saitou-kyouko":"","sasaki-kumi":"","sasaki-mirei":"","takase-mana":"","takamoto-ayaka":"","nagahama-neru":"","higashimura-mei":"","ishimori-nijika":"","imaizumi-yui":"","uemura-rina":"","ozeki-rika":"","oda-nana":"","koike-minami":"","kobayashi-yui":"","saitou-fuyuka":"","satou-shiori":"","shida-manaka":"","sugai-yuuka":"","suzumoto-miyu":"","nagasawa-nanako":"","habu-mizuho":"","harada-aoi":"","hirate-yurina":"","moriya-akane":"","yonetani-nanami":"","watanabe-rika":"","watanabe-risa":"","akimoto-manatsu":"","ikuta-erika":"","ikoma-rina":"","itou-marika":"","inoue-sayuri":"","etou-misa":"","kawago-hina":"","kawamura-mahiro":"","saitou-asuka":"","saitou-chiharu":"","saitou-yuuri":"","sakurai-reika":"","shiraishi-mai":"","takayama-kazumi":"","nakada-kana":"","nakamoto-himeka":"","nishino-nanase":"","noujou-ami":"","hashimoto-nanami":"","higuchi-hina":"","hoshino-minami":"","matsumura-sayuri":"","wakatsuki-yumi":"","wada-maaya":"","itou-karin":"","itou-junna":"","kitano-hinako":"","sagara-iori":"","sasaki-kotoko":"","shinuchi-mai":"","suzuki-ayane":"","terada-ranze":"","hori-miona":"","yamazaki-rena":"","watanabe-miria":"","itou-riria":"","iwamoto-renka":"","umezawa-minami":"","oozono-momoko":"","kubo-shiori":"","sakaguchi-tamami":"","satou-kaede":"","nakamura-reno":"","mukai-hazuki":"","yamashita-mizuki":"","yoshida-ayano-christie":"","yoda-yuuki":"","unei-sutaffu":""}:
        return web.HTTPNotFound()

    query_parameter=request.rel_url.query
    if "page" in query_parameter:
        if re.search(r'^\d+$',query_parameter["page"])!=None:
            page = int(query_parameter["id"])
            if page < 2:
                return web.HTTPBadRequest()
        else:
            return web.HTTPBadRequest()
    else:
        page = 1

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        judge = yield from cur.execute('SELECT post,rome,author,title,brief FROM list WHERE rome = "%s" ORDER BY post DESC,kana DESC LIMIT %s,20'%(rome,(page - 1) * 20))

        if judge == 0:
            yield from cur.close()
            conn.close()
            jsonback = {"content":"","more":0}
            return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')
        else:
            out = yield from cur.fetchall()
            yield from cur.close()
            conn.close()

    more = 1 if len(out) == 20 else 0
    content = ""

    for onepost in out:

        link = '/' + onepost[1] + '/' + onepost[0].strftime('%Y%m%d%H%M')
        # timeinfo = timefriendly(onepost[0])
        timedata = timeutc(onepost[0])
        
        card='''
        <div class="card" onclick="window.location.href='{link}'">
            <div class="line"><span class="post" data-post="{timedata}"></span></div>
            <div class="title">{title}</div>
            <div class="brief">{brief}</div>
        </div> '''.format(link = link,timedata = timedata,title = onepost[3],brief = onepost[4])

        content = content + card

    html='''<!DOCTYPE html>
<html>
<head>
<title>%s</title>
<meta charset="UTF-8" />
<meta name="theme-color" content="#eeeeee">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
<meta name="mobile-web-app-capable" content="yes">
<link rel="manifest" href="/manifest.json">
<link rel="stylesheet" type="text/css" href="/static/css/pwa-member.css" />
</head>
<body>
<div id="topbar" onclick="pagescroll();">
    <div id="back" onclick="event.cancelBubble=true;javascript:history.back(-1);"></div>
    <div id="name"><span id="kaji">%s</span><span id="rome">%s</span></div>
    <div id="avatar" style="background-image:url(/avatar/%s.jpg)"></div>
</div>
<div id="content">%s
</div>
</body>
<script src="https://cdn.bootcss.com/moment.js/2.18.1/moment.min.js"></script>
<script src="/static/js/main.js"></script>
</html>'''


    if page == 1:
        return web.Response(text=html%(out[0][2],out[0][2],re.sub("-"," ",rome),out[0][1],content),content_type='text/html',charset='utf-8')
    else:
        jsonback = {"content":content,"more":more}
        return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')


@asyncio.coroutine
def redirect(request):
    return aiohttp.web.HTTPFound(request.path_qs[0:-1])

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/{name:[a-z|-]+}/{time:\d{12}}', view)
    app.router.add_route('GET', '/{name:[a-z|-]+}', member)
    app.router.add_route('GET', '/{url:[\s\S]+/}',redirect)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9980)
    print('Server started at port 9980...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(create_pool())
loop.run_until_complete(init(loop))
loop.run_forever()
