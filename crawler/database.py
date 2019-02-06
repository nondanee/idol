# -*- coding: utf-8 -*-

import pymysql
import secret

def connect():
    return pymysql.connect(
        host = secret.database['mysql']['host'],
        user = secret.database['mysql']['user'],
        passwd = secret.database['mysql']['password'],
        db = secret.database['mysql']['database'],
        charset = 'utf8mb4'
    )
