import paho.mqtt.client as pahoMqtt
import requests

class mqtt(object):

    topic = "smartControl"
    port = 1883
    used_interpreters = list()

    def __init__(self, ip):
        self.ip = ip
        self.used_interpreters.append(self.__simpleStopInterpreter)
        self.__setupMQTT()

    #This adds an interpreter that gets the message and trys to interprete it. The interpreter should return True on success and otherwise false.
    def add_Interpreter(self, interpreter):
        if interpreter not in self.used_interpreters:
            self.used_interpreters.append(interpreter)

    def remove_Interpreter(self, interpreter):
        if interpreter in self.used_interpreters:
            self.used_interpreters.remove(interpreter)

    def __on_connect(self, client, userdata, flags, rc):
        print("Connected with result code {}".format(rc))
        client.subscribe(self.topic+"/#")

    def __on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        #try to interprete the message and abort at the first successfull try
        interpreted = False
        for interpreter in self.used_interpreters:
            if interpreter(msg):
                interpreted = True
                break
        if not interpreted:
            print("The message {} couldn't be interpreted.".format(msg.payload))


    def __on_disconnect(self, client, userdata, rc):
        print("Disconnected from server with result code {}.".format(rc))

    def __simpleStopInterpreter(self, msg):
        if msg.topic == self.topic+"/stop":
            print("stop")
            #Bug in Post-reqest, that execution of the methode stops
            #r = requests.post('http://192.168.2.52:56789/apps/SmartCenter',data='<remote><key code=1013/></remote>')
            #print(r.status_code)
            return True
        else:
            return False

    def __setupMQTT(self):
        client = pahoMqtt.Client()
        client.on_connect = self.__on_connect
        client.on_message = self.__on_message
        client.on_disconnect = self.__on_disconnect
        client.connect(self.ip, self.port, 60)
        client.loop_forever()
        self.client = client