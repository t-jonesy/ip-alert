#!/usr/bin/env python3

from time import sleep
import requests

#replace with webhook url
url = 'url'
#how often to check ip in seconds
rate = 5

#get ip from icanhazip.com; returns ip if succesful and error if unsuccesful
def get_ip():
    try:
        ip = requests.get('http://icanhazip.com').text
        ip = ip.strip()
    except:
        ip = 'offline'
    print(ip)
    return(ip)

#monitor for change in IP, loops until change is detected. returns new ip
def monitor_ip():
    old_ip = get_ip()
    new_ip = old_ip
    while new_ip == old_ip:
        sleep(rate)
        new_ip = get_ip()
    print("IP changed to {}.".format(new_ip))
    return(new_ip)

#sends webhook notification with new ip
def send_notification():
    data = {
        "content" : "WAN IP has changed to " + monitor_ip(),
    }
    try:
        result = requests.post(url, json = data)
    except Exception:
        print('error')
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("success, code {}.".format(result.status_code))

#loops send_notification continuously
while 1:
    try:
        send_notification()
    except Exception:
        print('error')