#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import urllib.request
import json
import os
import time
from collections import OrderedDict
from bs4 import BeautifulSoup

# Url base des directions
dir_url = 'http://www.t2c.fr/admin/synthese?SERVICE=page&p=17732927961956390&noline='
# Url base des arrêts
stop_url = 'http://www.t2c.fr/admin/synthese?SERVICE=page&p=17732927961956392&numeroroute='

lines = {
    'A': '11821953316814895',
    'B': '11821953316814897',
    'C': '11821953316814915',
    '3': '11821953316814882',
    '4': '11821953316814888',
    '5': '11821953316814889',
    '7': '11821953316814891',
    '8': '11821953316814892',
    '9': '11821953316814893',
    '10': '11821953316814874',
    '12': '11821953316814875',
    '13': '11821953316814876',
    '20': '11821953316814877',
    '21': '11821953316814878',
    '22': '11821953316814879',
    '23': '11822086460801028',
    '24': '11821953316814913',
    '25': '11822086460801025',
    '26': '11821953316814880',
    '27': '11821953316814881',
    '28': '11822086460801030',
    '31': '11821953316814883',
    '32': '11821953316814884',
    '33': '11821953316814914',
    '34': '11821953316814885',
    '35': '11821953316814886',
    '36': '11821953316814887',
    '37': '11822086460801032'
}


# Récupère chaque direction / arrêt pour une ligne donnée
def get_line_data(url):
    item_list = OrderedDict()
    req = urllib.request.urlopen(url)
    soup = BeautifulSoup(req, from_encoding='utf-8', features='html.parser')

    for item in soup.find_all('option')[1:]:
        item_name = item.text.strip()
        item_num = item['value']
        item_list[item_name] = item_num

    return item_list


# Scrap les infos des lignes / directions / arrêts et les stocke dans un fichier JSON
def fill_json():
    data = {'lines': []}

    for line_name, line_num in lines.items():
        print(f'Traitement de la ligne {line_name}')
        line_data = {'line_name': line_name, 'line_num': line_num, 'directions': []}

        line_dir = get_line_data(dir_url + line_num)
        for dir_name, dir_num in line_dir.items():
            dir_data = {'dir_name': dir_name, 'dir_num': dir_num, 'stops': []}

            line_stop = get_line_data(stop_url + dir_num)
            for stop_name, stop_num in line_stop.items():
                dir_data['stops'].append({'stop_name': stop_name, 'stop_num': stop_num})

            line_data['directions'].append(dir_data)

        data['lines'].append(line_data)


    # Sauvegarde les données dans un fichier JSON
    with open('t2c_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    fill_json()
