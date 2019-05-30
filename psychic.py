import requests
import json

import time
from time import sleep

import env_vars


def get_train_data():
    json = requests.get('http://api.bart.gov/api/etd.aspx?key=MW9S-E7SL-26DU-VV8V&json=y&cmd=etd&orig=12TH&plat=2').json()
    etds = json['root']['station'][0]['etd']
    etds_of_correct_routes = filter(lambda x: x['abbreviation'] == 'MLBR' or x['abbreviation'] == 'SFIA', etds)
    valid_etds = map(lambda x: x['estimate'], etds_of_correct_routes)

    all_train_data = {}
    for destination in etds_of_correct_routes:
        estimates = destination['estimate']
        min_etds = []
        for estimate in estimates:
            if estimate['minutes'].isdigit():
                # estimate = filter(lambda x: x['minutes'].isdigit(), estimate)
                min_etds.append(int(estimate['minutes']))

        all_train_data[destination['destination']] = min_etds

    etds_in_minutes = []

    for arr in valid_etds:
        for x in arr:
            if x['minutes'].isdigit():
                etds_in_minutes.append(int(x['minutes']))

    etds_in_minutes.sort()

    reachable_trains = filter(lambda x: x > 7, etds_in_minutes)
    next_reachable_train = reachable_trains[0]

    data_obj = {
        'next_reachable_train': next_reachable_train,
        'all_trains': all_train_data
    }

    return data_obj

def is_light_on():
    r = requests.get(env_vars.HUE_GET_LINK)
    return json.loads(r.content)['state']['on']
    # print r.content.json()['state']['on']

def start_reading():
    while True:
        if is_light_on():
            train_data = get_train_data()
            next_reachable_train = train_data['next_reachable_train']
            print train_data
            if next_reachable_train >= 8 and next_reachable_train < 12:
                turn_color(10000 + (3875 * (12 - next_reachable_train)))
                # turn_green()
            elif next_reachable_train >= 12 and next_reachable_train < 15:
                turn_color(1000 + (3000 * (15 - next_reachable_train)))
                # turn_yellow()
            else:
                turn_red()
        sleep(6)

def turn_color(color_num):
    print "turning " + str(color_num)
    r = requests.put(env_vars.HUE_PUT_LINK, json.dumps({"on":True, "sat":254, "bri":254,"hue":color_num}))
    print r.content
def turn_red():
    print "turning red"
    r = requests.put(env_vars.HUE_PUT_LINK, json.dumps({"on":True, "sat":254, "bri":254,"hue":1000}))
    print r.content
def turn_yellow():
    print "turning yellow"
    r = requests.put(env_vars.HUE_PUT_LINK, json.dumps({"on":True, "sat":254, "bri":254,"hue":10000}))
    print r.content
def turn_green():
    print "turning green"
    r = requests.put(env_vars.HUE_PUT_LINK, json.dumps({"on":True, "sat":254, "bri":254,"hue":20000}))
    print r.content
start_reading()
