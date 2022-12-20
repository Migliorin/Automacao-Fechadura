import utime

SSID = "FEMTOLAB"
PASW = "Km#873910*b"


def enable_esp32():
    from network_esp32 import wifi
    if wifi.isconnected() == False:
        for i in range(5):
            try:
                wifi.reset()
                print('try AT connect wifi...')
                wifi.connect(SSID, PASW)
                if wifi.isconnected():
                    print('wifi connect successfully to',SSID)
                    break
            except Exception as e:
                print(e)
    print('network state:', wifi.isconnected(), wifi.ifconfig())


enable_esp32()



from mqtt import MQTTClient

def print_msg(*args):
    print(args)


class MosquittoTests():

    def test_connect(self):
        mqtt = MQTTClient(client_id="umqtt_client", server="127.0.0.1")
        mqtt.connect()
        mqtt.disconnect()

    def test_publish(self):
        mqtt = MQTTClient(client_id="maixduino_controlador", server="10.0.0.190",port=1883)
        mqtt.connect()
        # mqtt.subscribe("foobar")
        mqtt.publish("foobar", 'Mensagem enviada do controlador')
        # mqtt.wait_msg()
        mqtt.disconnect()
    def test_sub(self):
        mqtt = MQTTClient(client_id="maixduino_controlador", server="10.0.0.190",port=1883)
        mqtt.connect()
        mqtt.set_callback(print_msg)
        mqtt.subscribe("resposta")
        while(True):
            mqtt.wait_msg()
        # mqtt.disconnect()



mosq = MosquittoTests()
mosq.test_sub()