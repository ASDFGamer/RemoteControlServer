import paho.mqtt.client as mqtt
import requests

topic = "smartControl"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe(topic+"/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    interpretMessage(msg)

def interpretMessage(msg):
    if msg.topic == topic+"/stop":
        print("stop")
        r = requests.post('http://192.168.2.52:56789/apps/SmartCenter','<remote><key code=1013/></remote>')
        print(r.status_code)

server = "192.168.2.2"


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(server, 1883, 60)

    client.loop_forever()