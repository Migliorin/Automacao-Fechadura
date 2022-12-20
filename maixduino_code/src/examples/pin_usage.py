import utime
from Maix import GPIO
from board import board_info
from fpioa_manager import fm

fm.register(board_info.PIN2,fm.fpioa.GPIO0)
fm.register(board_info.LED_R,fm.fpioa.GPIO1)

led_r = GPIO(GPIO.GPIO0,GPIO.OUT)
led = GPIO(GPIO.GPIO1,GPIO.OUT)

while True:
    led_r.value(0)
    led.value(0)
    utime.sleep_ms(5000)
    led_r.value(1)
    led.value(1)
    utime.sleep_ms(500)
    led_r.value(0)
    led.value(0)

fm.unregister(board_info.PIN2)
fm.unregister(board_info.LED_R)