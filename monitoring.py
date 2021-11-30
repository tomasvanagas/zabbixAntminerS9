serverIp='' # zabbix ip
antminer='192.168.'
android='192.168.43.1'

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
    soup=BeautifulSoup((requests.get("http://"+antminer+"/cgi-bin/minerStatus.cgi", timeout=5, auth=HTTPDigestAuth(userName,userPassword))).text,'html.parser')
    tchip=soup.findAll("div", {"id": "cbi-table-1-temp2"})
    out=[]
    for i in tchip:
        out.append(i.next)
        
    return ' '.join(out)


def run():
    while True:
        #print("test")
        try:
            temps = currentTemperatures().split(' ')
            temp1 = temps[0]
            temp2 = temps[1]
            temp3 = temps[2]
            print("Antminer --> 1: " + temp1 + "  2: " + temp2 + "  3: " + temp3 + "")
            
            packet = [
                ZabbixMetric('ZabbixTrapper', 'Miner1', temp1),
                ZabbixMetric('ZabbixTrapper', 'Miner2', temp2),
                ZabbixMetric('ZabbixTrapper', 'Miner3', temp3)
            ]

            result = zabbix_sender.send(packet)
        except:
            print("[*] Antminer not found.")
            pass

        try:
            session = requests.Session()
            htmlContent = session.get('http://' + android + ':1880/sensor', timeout=5).text
            #print(htmlContent)
            jsonObj = json.loads(htmlContent)
            print("Garazas: " + str(jsonObj['temperature']))

            packet = [
                ZabbixMetric('ZabbixTrapper', 'RoomTemp', jsonObj['temperature']),
            ]

            result = zabbix_sender.send(packet)
        except:
            print("[*] Android not found.")
            pass
        print("[*] Working...")
        #print()
        time.sleep(5)
    

run()

