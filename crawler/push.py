# -*- coding: utf-8 -*-

import json, datetime
import requests
import secret

def firebase(connect, fresh):
    if not fresh: return
    cursor = connect.cursor()
    subscriber = cursor.execute(
        ''' select end_point 
            from user 
            where id in (
                select distinct uid 
                from subscription
                where mid in ({})
            )
        '''.format(','.join(fresh))
    )
    if not subscriber: return
    subscription_list = cursor.fetchall()

    data = json.dumps({'registration_ids': registration_ids})
    headers = {
        'Authorization': secret.firebase['token'],
        'Content-Type': 'application/json'
    }

    response = requests.request('POST', 'https://android.googleapis.com/gcm/send', data = data, headers = headers, timeout = 5)
    push_status = json.loads(response.content)

    pid = push_status['multicast_id']
    values = []
#     for feed in fresh:
#         values.append()

    try:
        cursor.executemany('insert into push values(%s, %s, now())', values)
    except Exception as e:
        print(e)
    else:
        connect.commit()
        print('push save')

    cursor.close()
