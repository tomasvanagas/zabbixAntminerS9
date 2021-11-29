serverIp = '' # zabbix ip
antminer = '192.168.'
android = '192.168.'
trapperHostInZabbix = 'zabbixTrapper'


userName='root'
userPassword='root'

import datetime,time,sys
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPDigestAuth
from pyzabbix import ZabbixMetric, ZabbixSender
import requests
import json

zabbix_sender = ZabbixSender(zabbix_server=serverIp, zabbix_port=10051)


def currentTemperatures():
    soup=BeautifulSoup((requests.get("http://"+antminer+"/cgi-bin/minerStatus.cgi", auth=HTTPDigestAuth(userName,userPassword))).text,'html.parser')
    tchip=soup.findAll("div", {"id": "cbi-table-1-temp2"})
    out=[]
    for i in tchip:
        out.append(i.next)
        
    return ' '.join(out)


def run():
    while True:

        # 
        try:
            temp1 = currentTemperatures().split(' ')[0]
            temp2 = currentTemperatures().split(' ')[1]
            temp3 = currentTemperatures().split(' ')[1]
            print("1: " + temp1 + "  2: " + temp2 + "  3: " + temp3 + "")
            
            packet = [
                ZabbixMetric(trapperHostInZabbix, 'Miner1', temp1),
                ZabbixMetric(trapperHostInZabbix, 'Miner2', temp2),
                ZabbixMetric(trapperHostInZabbix, 'Miner3', temp3)
            ]

            result = zabbix_sender.send(packet)
        except:
            pass

        try:
            session = requests.Session()
            htmlContent = session.get('http://' + android + ':1880/sensor').text
            jsonObj = json.loads(htmlContent)
            print(jsonObj['temperature'])

            packet = [
                ZabbixMetric(trapperHostInZabbix, 'RoomTemp', jsonObj['temperature']),
            ]

            result = zabbix_sender.send(packet)
        except:
            pass
        time.sleep(5)
    

run()
