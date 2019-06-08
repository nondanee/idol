# -*- coding: utf-8 -*-

import hashlib, random, json, re
import requests
import secret

def baidu_translate(string):

    app_id = secret.translate['baidu']['id']
    secret_key = secret.translate['baidu']['key']
    from_lang = 'jp'
    to_lang = 'zh'

    salt = random.randint(32768, 65536)
    salt = 64330
    sign = hashlib.md5('{}{}{}{}'.format(app_id, string, salt, secret_key).encode('utf8')).hexdigest()

    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    query_string = {
        'appid': app_id,
        'q': string,
        'from': from_lang,
        'to': to_lang,
        'salt': salt,
        'sign': sign
    }

    for i in range(5):
        try:
            response = requests.get(url, params = query_string, timeout = 5)
            json_data = json.loads(response.text)
            return json_data['trans_result'][0]['dst']
        except:
            pass

def youdao_translate(string):

    app_id = secret.translate['youdao']['id']
    app_key = secret.translate['youdao']['key']
    from_lang = 'ja'
    to_lang = 'zh-CHS'


    salt = random.randint(32768, 65536)
    sign = hashlib.md5('{}{}{}{}'.format(app_id, string, salt, app_key).encode('utf8')).hexdigest()

    url = 'http://openapi.youdao.com/api'

    query_string = {
        'q': string,
        'from': from_lang,
        'to': to_lang,
        'appKey': app_id,
        'salt': salt,
        'sign': sign
    }

    for i in range(5):
        try:
            response = requests.get(url, params = query_string, timeout = 5)
            json_data = json.loads(response.text)
            return json_data['translation'][0]
        except:
            pass

def no_need_translate(text):
    if text in {
        'っ',
        'ノ',
        '年',
        '月',
        '日'
    }:
        return True
    else:
        return False

def discard_punctuation(text):
    if text[-1] in {'。', '！', '？'}:
        return text[0:-1]
    else:
        return text

def translate_unit(matched):
    original = matched.group('part')

    if no_need_translate(original):
        translation = original
    else:
        translation = baidu_translate(original)
        # translation = youdao_translate(original)
        translation = discard_punctuation(translation)

#     print(original + '\n' + translation + '\n')
    return translation

def translate(text):
    return re.sub(r'(?P<part>[一-龠|ぁ-ん|ァ-ヶ|ー|々]+)', translate_unit, text)
