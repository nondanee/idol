# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import random
import md5
import json
import os


      
members = {
    u"井口眞緒":[u"いぐち まお","iguchi-mao"],
    u"潮紗理菜":[u"うしお さりな","ushio-sarina"],
    u"柿崎芽実":[u"かきざき めみ","kakizaki-memi"],
    u"影山優佳":[u"かげやま ゆうか","kageyama-yuuka"],
    u"加藤史帆":[u"かとう しほ","katou-shiho"],
    u"齊藤京子":[u"さいとう きょうこ","saitou-kyouko"],
    u"佐々木久美":[u"ささき くみ","sasaki-kumi"],
    u"佐々木美玲":[u"ささき みれい","sasaki-mirei"],
    u"高瀬愛奈":[u"たかせ まな","takase-mana"],
    u"高本彩花":[u"たかもと あやか","takamoto-ayaka"],
    u"長濱ねる":[u"ながはま ねる","nagahama-neru"],
    u"東村芽依":[u"ひがしむら めい","higashimura-mei"],
    u"石森虹花":[u"いしもり にじか","ishimori-nijika"],
    u"今泉佑唯":[u"いまいずみ ゆい","imaizumi-yui"],
    u"上村莉菜":[u"うえむら りな","uemura-rina"],
    u"尾関梨香":[u"おぜき りか","ozeki-rika"],
    u"織田奈那":[u"おだ なな","oda-nana"],
    u"小池美波":[u"こいけ みなみ","koike-minami"],
    u"小林由依":[u"こばやし ゆい","kobayashi-yui"],
    u"齋藤冬優花":[u"さいとう ふゆか","saitou-fuyuka"],
    u"佐藤詩織":[u"さとう しおり","satou-shiori"],
    u"志田愛佳":[u"しだ まなか","shida-manaka"],
    u"菅井友香":[u"すがい ゆうか","sugai-yuuka"],
    u"鈴本美愉":[u"すずもと みゆ","suzumoto-miyu"],
    u"長沢菜々香":[u"ながさわ ななこ","nagasawa-nanako"],
    u"土生瑞穂":[u"はぶ みづほ","habu-mizuho"],
    u"原田葵":[u"はらだ あおい","harada-aoi"],
    u"平手友梨奈":[u"ひらて ゆりな","hirate-yurina"],
    u"守屋茜":[u"もりや あかね","moriya-akane"],
    u"米谷奈々未":[u"よねたに ななみ","yonetani-nanami"],
    u"渡辺梨加":[u"わたなべ りか","watanabe-rika"],
    u"渡邉理佐":[u"わたなべ りさ","watanabe-risa"],

    u"秋元真夏":[u"あきもと まなつ","akimoto-manatsu"],
    u"生田絵梨花":[u"いくた えりか","ikuta-erika"],
    u"生駒里奈":[u"いこま りな","ikoma-rina"],
    u"伊藤万理華":[u"いとう まりか","itou-marika"],
    u"井上小百合":[u"いのうえ さゆり","inoue-sayuri"],
    u"衛藤美彩":[u"えとう みさ","etou-misa"],
    u"川後陽菜":[u"かわご ひな","kawago-hina"],
    u"川村真洋":[u"かわむら まひろ","kawamura-mahiro"],
    u"齋藤飛鳥":[u"さいとう あすか","saitou-asuka"],
    u"斎藤ちはる":[u"さいとう ちはる","saitou-chiharu"],
    u"斉藤優里":[u"さいとう ゆうり","saitou-yuuri"],
    u"桜井玲香":[u"さくらい れいか","sakurai-reika"],
    u"白石麻衣":[u"しらいし まい","shiraishi-mai"],
    u"高山一実":[u"たかやま かずみ","takayama-kazumi"],
    u"中田花奈":[u"なかだ かな","nakada-kana"],
    u"中元日芽香":[u"なかもと ひめか","nakamoto-himeka"],
    u"西野七瀬":[u"にしの ななせ","nishino-nanase"],
    u"能條愛未":[u"のうじょう あみ","noujou-ami"],
    u"橋本奈々未":[u"はしもと ななみ","hashimoto-nanami"],
    u"樋口日奈":[u"ひぐち ひな","higuchi-hina"],
    u"星野みなみ":[u"ほしの みなみ","hoshino-minami"],
    u"松村沙友理":[u"まつむら さゆり","matsumura-sayuri"],
    u"若月佑美":[u"わかつき ゆみ","wakatsuki-yumi"],
    u"和田まあや":[u"わだ まあや","wada-maaya"],
    u"伊藤かりん":[u"いとう かりん","itou-karin"],
    u"伊藤純奈":[u"いとう じゅんな","itou-junna"],
    u"北野日奈子":[u"きたの ひなこ","kitano-hinako"],
    u"相楽伊織":[u"さがら いおり","sagara-iori"],
    u"佐々木琴子":[u"ささき ことこ","sasaki-kotoko"],
    u"新内眞衣":[u"しんうち まい","shinuchi-mai"],
    u"鈴木絢音":[u"すずき あやね","suzuki-ayane"],
    u"寺田蘭世":[u"てらだ らんぜ","terada-ranze"],
    u"堀未央奈":[u"ほり みおな","hori-miona"],
    u"山崎怜奈":[u"やまざき れな","yamazaki-rena"],
    u"渡辺みり愛":[u"わたなべ みりあ","watanabe-miria"],
    u"伊藤理々杏":[u"いとう りりあ","itou-riria"],
    u"岩本蓮加":[u"いわもと れんか","iwamoto-renka"],
    u"梅澤美波":[u"うめざわ みなみ","umezawa-minami"],
    u"大園桃子":[u"おおぞの ももこ","oozono-momoko"],
    u"久保史緒里":[u"くぼ しおり","kubo-shiori"],
    u"阪口珠美":[u"さかぐち たまみ","sakaguchi-tamami"],
    u"佐藤楓":[u"さとう かえで","satou-kaede"],
    u"中村麗乃":[u"なかむら れの","nakamura-reno"],
    u"向井葉月":[u"むかい はづき","mukai-hazuki"],
    u"山下美月":[u"やました みづき","yamashita-mizuki"],
    u"吉田綾乃クリスティー":[u"よしだ あやの くりすてぃー","yoshida-ayano-christie"],
    u"与田祐希":[u"よだ ゆうき","yoda-yuuki"],
    u"３期生":[u"さんきせい","sankisei"],
    u"運営スタッフ":[u"うんえい スタッフ","unei-sutaffu"],
    u"administrator":[u"うんえい スタッフ","unei-sutaffu"]
}


def baidufanyi(strin):

    appId = '*???*' 
    secretKey = '*???*'
    fromLang = 'jp'
    toLang = 'zh'

    salt = random.randint(32768, 65536)
    sign = appId+strin+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate?appid=%s&q=%s&from=%s&to=%s&salt=%s&sign=%s"%(appId,urllib.quote(strin),fromLang,toLang,str(salt),sign)
    
    request = urllib2.Request(url=url)

    reconnect = 0
    while reconnect < 8:
        try:
            response = urllib2.urlopen(request,timeout = 3)
        except:
            reconnect = reconnect + 1
            print "retry",reconnect
        else:
            break
    jsondata = response.read()

    decodejson = json.loads(jsondata)
    strout = decodejson['trans_result'][0]['dst']   
    return strout


def youdaofanyi(strin):

    appId = '*???*'
    appKey = '*???*'
    fromLang = 'ja'
    toLang = 'zh-CHS'


    salt = random.randint(32768, 65536)
    sign = appId+strin+str(salt)+appKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()

    url = 'http://openapi.youdao.com/api?q=%s&from=%s&to=%s&appKey=%s&salt=%s&sign=%s'%(urllib.quote(strin),fromLang,toLang,appId,str(salt),sign)

    request = urllib2.Request(url=url)

    reconnect = 0
    while reconnect < 8:
        try:
            response = urllib2.urlopen(request,timeout = 3)
        except:
            reconnect = reconnect + 1
            print "retry",reconnect
        else:
            break
    jsondata = response.read()

    decodejson = json.loads(jsondata)
    strout = decodejson["translation"][0]
    return strout



def translate(original):#original <type 'unicode'>
    waittrans = re.findall(u'[一-龠|ぁ-ん|ァ-ヶ|ー|々]+',original,re.U)
    findnum = len(waittrans)
    subnum = 0
    waitfill = original
    while(findnum!=subnum):
        waitfill = re.sub(u'[一-龠|ぁ-ん|ァ-ヶ|ー|々]+',"%s",waitfill,re.U)
        subnum = len(re.findall('%s',waitfill))
    # if len(re.findall('%',waitfill)) != subnum:
    waitfill = re.sub(u'%(?!s)','∉'.decode("utf-8"),waitfill)
    
    filltext=[]
    print "workload",len(waittrans)
    for line in waittrans:     
              
        if line in { u"っ" : "", u"ノ" : ""}:
            filltext.append(line)
            continue

        send = line.encode("utf-8") 
        gettrans = baidufanyi(send)

        if re.search(u"[。！？]",gettrans[-1]):
            gettrans = gettrans[0:-1]              
           
        filltext.append(gettrans)

    translation = waitfill %tuple(filltext)
    translation = re.sub("∉".decode("utf-8"),'%',translation)
    return translation
    

def convertmark(matched):
    markcode = matched.group("mark");
    marks = {
        "&uuml;":"Ü",
        "&lrm;":"",
        "&uml;":"¨",
        "&uarr;":"↑",
        "&sup3;":"³",
        "&rsaquo;":"›",
        "&rdquo;":"”",
        "&omega;":"ω",
        "&nu;":"ν",
        "&nbsp;":" ",
        "&nabla;":"∇",
        "&macr;":"¯",
        "&lt;":"<",
        "&lsaquo;":"‹",
        "&hellip;":"…",
        "&hearts;":"♥",
        "&gt;":">",
        "&forall;":"∀",
        "&deg;":"°",
        "&darr;":"↓",
        "&circ;":"ˆ",
        "&bull;":"•",
        "&acute;":"´",
        "&loz;":"◊",
        "&ordm;":"º",
        "&Delta;":"Δ",
        "&dagger;":"†",
        "&equiv;":"≡",
        "&rarr;":"→",
        "&part;":"∂",
        "&amp;":"&",
        "&epsilon;":"ε",
        "&times;":"×",
        "&cap;":"∩",
        "&minus;":"−",
        "&sub;":"⊂",
        "&Uuml;":"Ü",
        "&cedil;":"¸",
        "&sigma;":"σ",
        "&raquo;":"»",
        "&lowast;":"∗",
        "&perp;":"⊥",
        "&sup;":"⊃",
        "&Theta;":"Θ",
        "&middot;":"·",
        "&upsilon;":"υ"
        }
    return marks[markcode]


def indent(article):
    article = re.sub(r"^(<br>)*",'<br>',article)
    textsplit = article.split("<br>")
    text = ''

    for i in xrange(0,len(textsplit)):
        if textsplit[i] == '':
            thisline = '<p><br></p>'
        elif re.search(r'<img[^>]+>',textsplit[i]) != None:
            besidesimg = re.sub(r'<img[^>]+>','',textsplit[i])
            besidesimg = re.sub(u'[\s|(&nbsp;)|(\u3000)|(\xa0)]+','',besidesimg)
            if besidesimg == '':
                thisline = ''
                allimg = re.findall(r'<img src="([^"]+)">',textsplit[i])
                for j in xrange(0,len(allimg)):
                    thisline = thisline + '<img class="wide" src="' + allimg[j] + '">'
            else:
                thisline = "<p>" + textsplit[i] + "</p>"
        else:
            thisline = "<p>" + textsplit[i] + "</p>"
    
        text = text + thisline

    return text


def sortout(text):

    text=re.sub(r'[\n|\r]',"",text)
    
    text=re.sub(r'<p[^>]*>\s*</p>','',text)
    text=re.sub(r'<div[^>]*>\s*</div>','',text)
    
    
    text=re.sub(u'<p[^>]*>[\s|(&nbsp;)|\u3000|\xa0]+</p>','<br>',text)
    text=re.sub(u'<div[^>]*>[\s|(&nbsp;)|\u3000|\xa0]+</div>','<br>',text)

    text=re.sub(r'<div[^>]*><span[^>]*>[^<]*<br[^>]*></span></div>','<br>',text)
    text=re.sub(r'<p[^>]*><span[^>]*>[^<]*<br[^>]*></span></p>','<br>',text)
    text=re.sub(r'<div[^>]*>[^<]*<br[^>]*>[^<]*</div>','<br>',text)
    
    
    text=re.sub(r'<p[^>]*>([\s\S]+?)</p>','\g<1><br>',text)
    text=re.sub(r'<div[^>]*>([\s\S]+?)</div>','\g<1><br>',text)
                
    while re.search(r'<a href="http://dcimg.awalker.jp/img1.php\?id=[^"]+?"><img[\s\S]*?src="[^"]+?"[^>]*></a>',text) != None:
        text=re.sub(r'<a href="(http://dcimg.awalker.jp/img1.php\?id=[^"]+?)"><img[\s\S]*?src="([^"]+?)"[^>]*></a>','<img src="\g<1>">',text)

    text=re.sub(r'<a href="http://blog.nogizaka46.com/staff/img/([^"]+?)"[\s\S]*?>[^<]*<img[^>]+?>','<img src="http://img.nogizaka46.com/blog/staff/img/\g<1>">',text)    
    text=re.sub(r'<a href="http://img.nogizaka46.com/([^"]+?)"[^>]*?>[^<]*<img[^>]+?>','<img src="http://img.nogizaka46.com/\g<1>">',text)

    text=re.sub(r'<(?!(br|img))[\s\S]+?>',"",text)

    while re.search(r'&\w+?;',text)!=None:
        text = re.sub(r'(?P<mark>&[\w]+?;)',convertmark,text)


    text=re.sub(r'<br[^>]*?>','<br>',text)
    text=re.sub(r'<img[^>]+?src=""[^>]*?>',"",text)
    text=re.sub(r'<img[^>]+?src="([^"]+)"[^>]*?>','<img src="\g<1>">',text)
    text=re.sub(r'<img[^>]+?src="(/files/[^"]+)"[^>]*?>','<img src="http://www.keyakizaka46.com\g<1>">', text)

    text=re.sub(r'[\s|\u3000|\xa0]*?<br>[\s|\u3000|\xa0]*?','<br>',text)    
    # text=re.sub(u'\u3000',' ',text)
    text=re.sub(r'^[\s|\u3000|\xa0]*(<br>)*',"",text)
    text=re.sub(r'(<br>)*[\s|\u3000|\xa0]*$',"",text)

    return text


def summary(text):

    brief=re.sub(r'<br>'," ",text)
    brief=re.sub(r'<img src="([\s\S]+?)">'," ", brief)
    brief=re.sub(r'http://',"", brief)
    brief=re.sub(r'https://',"", brief)
    brief=re.sub(r'\s|\u3000|\xa0'," ",brief)
    brief=re.sub(r'\s+'," ",brief)    
    brief=re.sub(r'^\s+',"",brief)
    brief=brief[0:80]
    brief=re.sub(r'\s$',"",brief)
    brief=brief+"..."

    return brief


def findid(link):
    if re.search(r'nogizaka46',link) != None:
        idtry = re.search(r'\d{4}/\d{2}/(\d{6})',link)
        if idtry != None:
            postid = idtry.group(1).zfill(6)
        else:
            postid = '0'
    elif re.search(r'keyakizaka46',link) != None:
        idtry = re.search(r'diary/detail/(\d+)\?ima',link)
        if idtry != None:
            postid = idtry.group(1).zfill(6)
        else:
            postid = '0'

    return postid


def identifysankisei(title):

    sankisei = {
        u"伊藤理々杏":u"伊藤理々杏",
        u"伊藤 理々杏":u"伊藤理々杏",
        u"岩本蓮加":u"岩本蓮加",
        u"岩本 蓮加":u"岩本蓮加",
        u"梅澤美波":u"梅澤美波",
        u"梅澤 美波":u"梅澤美波",
        u"大園桃子":u"大園桃子",
        u"大園 桃子":u"大園桃子",
        u"久保史緒里":u"久保史緒里",
        u"久保 史緒里":u"久保史緒里",
        u"阪口珠美":u"阪口珠美",
        u"阪口 珠美":u"阪口珠美",
        u"佐藤楓":u"佐藤楓",
        u"佐藤 楓":u"佐藤楓",
        u"中村麗乃":u"中村麗乃",
        u"中村 麗乃":u"中村麗乃",
        u"向井葉月":u"向井葉月",
        u"向井 葉月":u"向井葉月",
        u"山下美月":u"山下美月",
        u"山下 美月":u"山下美月",
        u"吉田綾乃クリスティー":u"吉田綾乃クリスティー",
        u"吉田綾乃 クリスティー":u"吉田綾乃クリスティー",
        u"吉田 綾乃 クリスティー":u"吉田綾乃クリスティー",
        u"与田祐希":u"与田祐希",
        u"与田 祐希":u"与田祐希"
    }

    author = "３期生"

    for member in sankisei:

        if re.search(sankisei[member],title) != None:
            author = sankisei[member]
            title = re.sub(author,"",title)
            title = re.sub(r'[\u3000|\xa0|\s]*$',"",title)
            break

    return (author,title)



def downloadphoto(rome,filename,url):
    serverpath = '*???*'
    filepath = serverpath + "/" + rome + "/" + filename
    if os.path.exists(filepath):
        return 1

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'} 

    if re.search(r'awalker',url)!=None:

        photourl = re.sub(r"img1.php\?id",'img2.php?sec_key',url)

        headers['Host'] = 'dcimg.awalker.jp'

        request = urllib2.Request(url=url, headers=headers)
        reconnect = 0
        while reconnect < 8:
            try:
                response = urllib2.urlopen(request,timeout = 3)
            except:
                reconnect = reconnect + 1
                "retry",reconnect
            else:
                break

        if "set-cookie" in response.headers:
            cookie = response.headers["set-cookie"]
        else:
            if re.search("この画像は保存期間が終了したため削除されました",response.read())!=None:
                return 2
            
        cookie = re.sub(r';[\s\S]+$','',cookie)
        headers["Referer"] = url
        headers["Cookie"] = cookie
         
        request = urllib2.Request(url=photourl, headers=headers)
        reconnect = 0
        while reconnect < 5:
            try:
                response = urllib2.urlopen(request,timeout = 5)
            except:
                reconnect = reconnect + 1
                print "retry",reconnect
            else:
                break

    else:

        request = urllib2.Request(url=url, headers=headers)
        reconnect = 0
        while reconnect < 8:
            try:
                response = urllib2.urlopen(request,timeout = 5)
            except:
                reconnect = reconnect + 1
                print "retry",reconnect
            else:
                break

    pic = response.read()
    f = open(filepath,'wb')
    f.write(pic)
    f.close()
    return 1
