import sqlite3
from datetime import date, datetime
import paho.mqtt.client as mqtt
import json
import os
import datetime

def on_message_msgs(mosq, obj, msg):
    print("MESSAGES:", str(msg.payload))

    pload = json.loads(msg.payload)
    if int(pload['distance']) % 10  == 0:
        print(os.path.abspath('C:\\Users\\poltavet\\PycharmProjects\\Rasp_IoT\\db.sqlite3'))
        conn = sqlite3.connect(os.path.abspath('C:\\Users\\poltavet\\PycharmProjects\\Rasp_IoT\\db.sqlite3'))
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO myhome_1_orbi_tmp(created, distance, time, speed) VALUES (?,?,?,?)''',
                   (datetime.datetime.now(), int(pload['distance']), float(pload['time']), float(pload['speed']),))
        conn.commit()
        conn.close()

def main():
    mqttc = mqtt.Client()
    mqttc.message_callback_add("home/orbitrack/impulse", on_message_msgs)
    mqttc.connect("kotok.asuscomm.com", 1883, 60)
    mqttc.subscribe("home/orbitrack/impulse", 0)
   # mqttc.loop_start()
    return mqttc

if __name__ =="__main__":
    main()
    main().loop_forever()