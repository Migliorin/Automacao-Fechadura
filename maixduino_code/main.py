import utime
from Maix import GPIO
from board import board_info
from fpioa_manager import fm

fm.register(board_info.PIN2,fm.fpioa.GPIO0)
fm.register(board_info.LED_R,fm.fpioa.GPIO1)

led_r = GPIO(GPIO.GPIO0,GPIO.OUT)
led = GPIO(GPIO.GPIO1,GPIO.OUT)

led_r.value(0)
led.value(0)

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


from http import post

import sensor
import image
import lcd
import time

from simple import MQTTClient

clock = time.clock()
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.set_hmirror(1) # set hmirror if can not recognize qr code
sensor.skip_frames(30)

mqtt = MQTTClient(client_id="maixduino_controlador", server="10.0.0.190",port=1883)
mqtt.connect()

response = None

def print_msg(*args):
    global response
    print(args)
    response = True


while True:
    clock.tick()
    img = sensor.snapshot()
    res = img.find_qrcodes()
    fps = clock.fps()
    if len(res) > 0:
        # print(img.binary_to_rgb())
        img.draw_string(2,2, res[0].payload(), color=(0,128,0), scale=2)

        mqtt.set_callback(print_msg)



        mqtt.publish("foobar", str(res[0].payload()))
        mqtt.subscribe("response")
        start = time.time()
        while(response is None) and ((time.time() - start) > 5):
            print('esperando resposta')
            mqtt.wait_msg()

        print('Fim da resposta')



    lcd.display(img)



mqtt.disconnect()





