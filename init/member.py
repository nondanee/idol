# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 14:30:07 2018

@author: Nzix
"""

with open('member.txt', 'r', encoding = 'utf-8') as f: data = f.readlines()

sql = ''

for line in data:
    line = line.replace('\n', '')
    if not line: continue
    if line.startswith('#'): continue

    id, name, furigana, romaji = line.split('\t')
    sql += 'insert into member values({}, "{}", "{}", "{}", "{}", {}, {});\n'.format(id, romaji, name, furigana, '', 0, 0)

with open('member.sql', 'w', encoding = 'utf-8') as f: f.write(sql)