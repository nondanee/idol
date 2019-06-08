import time, datetime, json, re

def time_utc(time_set):
    utc_time = time_set + datetime.timedelta(seconds = -32400)
    return utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')

def jsonify(json_dict):
    return json.dumps(json_dict, ensure_ascii = False, sort_keys = True)

def avatar_locate(id, romaji):
    return '/avatar/{}.jpg'.format(romaji)

def member_affiliate(id):
    id = str(id).zfill(4)
    affiliation = ''
    if id.startswith('0'):
        affiliation = '乃木坂46'
    if id.startswith('1'):
        affiliation = '欅坂46'
    if id.startswith('2'):
        affiliation = '日向坂46'
    # if id.startswith('12'):
    #     affiliation = '欅坂46 2期生'
    # if id.startswith('23'):
    #     affiliation = '日向坂46 3期生'
#     if id.startswith('03'):
#         affiliation = '乃木坂46 3期生'
#     if id.startswith('22'):
#         affiliation = 'けやき坂46 2期生'
    if id.startswith('04'):
        affiliation = '乃木坂46 4期生'
    return affiliation

def thumb_locate(fid, available):
    return None
    if available:
        return '/thumb/{}.jpg'.format(str(fid).zfill(7))
    else:
        return None
      
def photo_locate(romaji, post, fid, text):
    def substitution(matched):
        size = matched.group(1)
        name = matched.group(2).split('.')
        name[0] = name[0].zfill(4)
        return '![{}]({}/{}/{}-{}-{})'.format(size, 'https://storage.aidoru.tk', romaji, post.strftime('%Y%m%d'), str(fid).zfill(7), '.'.join(name))    
    return re.sub(r'\!\[([^\]]*)\]\(([^\)]+)\)', substitution, text)
  
def paging_parse(query_string):
    try: page = int(query_string['page'])
    except: page = 1
    try: size = int(query_string['size'])
    except: size = 10
    page = page if page > 0 else 1
    size = size if size > 0 else 10
    size = size if size < 101 else 100
    return page, size
    
        