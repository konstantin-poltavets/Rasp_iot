import sqlite3
from datetime import date, datetime
import paho.mqtt.client as mqtt
import time

def on_message_msgs(mosq, obj, msg):
    print("MESSAGES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    conn = sqlite3.connect("/home/pi/iot/myhome/db.sqlite3") 
    cursor = conn.cursor()
    today = datetime.today()
    cursor.execute('''INSERT INTO myhome_1_mqtt(topic, payload, created_date) VALUES (?,?,?)''', (msg.topic, float(msg.payload), today,))
    conn.commit()
    conn.close
#    time.sleep(60)

def on_message_bytes(mosq, obj, msg):
    print("BYTES" + msg.topic + " " + str(msg.qos) + " " + str(float(msg.payload)))
    conn = sqlite3.connect("/home/pi/iot/myhome/db.sqlite3") 
    cursor = conn.cursor()
    today = datetime.today()
    cursor.execute('''INSERT INTO myhome_1_mqtt(topic, payload, created_date) VALUES (?,?,?)''', (msg.topic, float(msg.payload), today,))
    conn.commit()
    conn.close


def on_message(mosq, obj, msg):
    print("-->>" + msg.topic + " " + str(msg.qos) + " " + str(float(msg.payload)))
    conn = sqlite3.connect("/home/pi/iot/myhome/db.sqlite3") 
    cursor = conn.cursor()
    today = datetime.today()
    cursor.execute('''INSERT INTO myhome_1_mqtt(topic, payload, created_date) VALUES (?,?,?)''', (msg.topic, float(msg.payload), today,))
    conn.commit()
    conn.close

mqttc = mqtt.Client()

# Add message callbacks that will only trigger on a specific subscription match.
mqttc.message_callback_add("home/poliv/water", on_message_msgs)
mqttc.message_callback_add("home/poliv/temp", on_message_bytes)
#mqttc.on_message = on_message
mqttc.connect("kotok.asuscomm.com", 1883, 60)
mqttc.subscribe("home/#", 0)

mqttc.loop_forever()
