import paho.mqtt.client as pahoMqtt
import requests

class mqtt(object):

    topic = "smartControl"
    port = 1883

    def __init__(self, ip):
        self.ip = ip
        self.__setupMQTT()

    def __on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.topic+"/#")

    def __on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        self.interpretMessage(msg)

    def interpretMessage(self, msg):
        if msg.topic == self.topic+"/stop":
            print("stop")
            r = requests.post('http://192.168.2.52:56789/apps/SmartCenter','<remote><key code=1013/></remote>')
            print(r.status_code)

    def __setupMQTT(self):
        client = pahoMqtt.Client()
        client.on_connect = self.__on_connect
        client.on_message = self.__on_message
        client.connect(self.ip, self.port, 60)
        client.loop_forever()
        self.client = client