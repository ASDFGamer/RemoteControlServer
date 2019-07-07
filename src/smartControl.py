import mqtt



server = "192.168.2.2"

def smartControl():
    client = mqtt.mqtt(server)

if __name__ == '__main__':
    smartControl()