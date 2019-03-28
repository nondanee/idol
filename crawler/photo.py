# -*- coding: utf-8 -*-

import datetime, os, re, subprocess, math, json, base64
import requests, PIL.Image
import secret

def locate(meta, index, extension, usage):
    host_dir = '../'
    date = datetime.datetime.strptime(meta['post'], '%Y/%m/%d %H:%M').strftime('%Y%m%d')

    if usage == 'thumb':
        thumb_dir = os.path.join(host_dir, 'thumb')
        if not os.path.exists(thumb_dir): os.mkdir(thumb_dir)
        return os.path.join(thumb_dir, '{}.{}'.format(meta['feed_id'].zfill(7), 'jpg'))
    else:
        photo_dir = os.path.join(host_dir, 'photo', meta['romaji'])
        if not os.path.exists(photo_dir): os.makedirs(photo_dir)
        return os.path.join(photo_dir, '{}-{}-{}.{}'.format(date, meta['feed_id'].zfill(7), str(index).zfill(4), extension))

def transfer(path, name):
#     subprocess.Popen(['gsutil', 'cp', path, path.replace('../photo/','gs://aidoru-storage/')]).wait()
    response = requests.post(
        url = 'https://www.googleapis.com/oauth2/v4/token',
        headers = {'content-type': 'application/x-www-form-urlencoded', 'user-agent': 'google-oauth-playground'},
        data = 'client_id={}&client_secret={}&grant_type=refresh_token&refresh_token={}'.format(secret.storage['client_id'], secret.storage['client_secret'], secret.storage['refresh_token'])
    )
    access_token = json.loads(response.text)['access_token']
    response = requests.post(
        url = 'https://www.googleapis.com/upload/storage/v1/b/{}/o'.format(secret.storage['bucket_name']),
        params = {'uploadType': 'media', 'name': name},
        headers = {'Authorization': 'Bearer {}'.format(access_token), 'Content-Type': {'.gif': 'image/gif', '.jpg': 'image/jpeg', '.png': 'image/png'}[os.path.splitext(path)[-1]]},
        data = open(path, 'rb').read()
    )
    assert response.status_code == 200
    os.remove(path)

def process(meta, text):

    urls_find = re.findall(r'\!\[[^\]]*\]\(([^\)]+)\)', text)
    urls = list(set(urls_find))
    urls.sort(key = urls_find.index)

    index = 1
    thumbnail = False
    images = []

    for url in urls:

        if re.search(r'.jpg$', url, flags = re.I) or re.search(r'.jpeg$', url, flags = re.I):
            extension = 'jpg'
        elif re.search(r'.png$', url, flags = re.I):
            extension = 'png'
        elif re.search(r'.gif$', url, flags = re.I):
            extension = 'gif'
        elif re.search(r'awalker', url):
            extension = 'jpg'
        else:
            text = re.sub(r'\!\[[^\]]*\]\({}\)'.format(re.escape(url)), '', text)
            # raise error
            continue

        photo_path = locate(meta, index, extension, 'normal')
        status = download(url, photo_path)
        if status == 1:
            size = measure(photo_path)
            transfer(photo_path, photo_path.replace('../photo/', ''))
#             if not thumbnail and suit(extension, size):
#                 thumb_path = locate(meta, index, extension, 'thumb')
#                 thumbnail = True
#                 compress(photo_path, thumb_path)
        else:
            size = [0, 0]
            print(meta['feed_id'], url, status)

        substitution = '![{}x{}]({}.{})'.format(size[0], size[1], index, extension)
        text = re.sub(r'\!\[[^\]]*\]\({}\)'.format(re.escape(url)), substitution, text)

        # if re.search(re.escape(img_url),text) != None:
        #     print 'img dealing error'

        images.append([index, extension, url, size[0], size[1], status])
        index += 1

    return text, thumbnail, images

def download(url, path):

#     test = requests.get('http://localhost:8080/search?url=' + base64.urlsafe_b64encode(url.encode('utf-8')).decode('utf-8'), allow_redirects = False)
#     if test.status_code == 302: url = test.headers['location']

    if os.path.exists(path): return 1
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'} 
    # proxies = {'http': 'http://127.0.0.1:1080', 'https': 'http://127.0.0.1:1080'}

    session = requests.Session()
    session.headers.update(headers)
    # session.proxies = proxies

    if url.find('awalker') != -1:
        retry = 0
        while True:
            try:
                response = session.get(url, timeout = 5)
                if response.text.find(u'この画像は保存期間が終了したため削除されました') != -1: return 2
            except:
                retry += 1
                if retry > 10: return 0
            else:
                if url.find('img1.php?id') != -1:
                    url = url.replace('img1.php?id','img2.php?sec_key')
                elif url.find('/view/') != -1:
                    url = url.replace('/view/','/i/')
                break

    for i in range(10):
        f = open(path,'wb')
        try:
            response = session.get(url, timeout = 5, stream = True)
            for chunk in response.iter_content(chunk_size = 512):
                if chunk:
                    f.write(chunk)
        except:
            f.close()
            if os.path.exists(path): os.remove(path)
        else:
            f.close()
            convert(path)
            return 1
    return 0


def measure(path):
    image = PIL.Image.open(path)
    return image.size

def suit(extension, size):
    if extension == 'gif': return False
    elif size[0] < 240 or size[1] < 240: return False
    else: return True

def compress(source, destination):
    short_side = 270.0
    image = PIL.Image.open(source)
    if image.mode != 'RGB': image = image.convert('RGB')
    width, height = image.size
    radio = 1.0 * width / height  if width > height else 1.0 * height / width
    long_side = math.ceil(radio * short_side)
    if width < height:
        size = [int(short_side), int(long_side)]
    else:
        size = [int(long_side), int(short_side)]
    image.thumbnail(tuple(size))
    image.save(destination, 'JPEG')

def convert(path):
    f = open(path, 'rb')
    header = f.read(16)
    f.close()
    if header.find(b'ftypheic') != -1: subprocess.Popen(['tifig', path, path]).wait()
