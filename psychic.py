import requests
import json

import pdb

import env_vars

def get_train_data():
    json = requests.get('http://api.bart.gov/api/etd.aspx?key=MW9S-E7SL-26DU-VV8V&json=y&cmd=etd&orig=12TH&plat=2').json()
    etds = json['root']['station'][0]['etd']
    etds_of_correct_routes = filter(lambda x: x['abbreviation'] == 'MLBR' or x['abbreviation'] == 'SFIA', etds)
    valid_etds = map(lambda x: x['estimate'], etds_of_correct_routes)

    all_train_data = {}
    for destination in etds_of_correct_routes:
        min_etds = map(lambda x: int(x['minutes']), destination['estimate'])
        all_train_data[destination['destination']] = min_etds

    etds_in_minutes = []

    for arr in valid_etds:
        for x in arr:
            etds_in_minutes.append(int(x['minutes']))

    etds_in_minutes.sort()

    reachable_trains = filter(lambda x: x > 7, etds_in_minutes)
    next_reachable_train = reachable_trains[0]

    data_obj = {
        'next_reachable_train': next_reachable_train,
        'all_trains': all_train_data
    }

    # pdb.set_trace()
    return data_obj

print get_train_data()
