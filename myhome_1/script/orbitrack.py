import paho.mqtt.client as mqtt

def on_message_msgs(mosq, obj, msg):
    print(int(msg.payload))
    return str(msg.payload)


mqttc = mqtt.Client()
mqttc.message_callback_add("home/orbitrack/steps", on_message_msgs)
mqttc.connect("kotok.asuscomm.com", 1883, 60)
mqttc.subscribe("home/orbitrack/steps", 0)
mqttc.loop_forever()

#if __name__=="__main__":
print(on_message_msgs)