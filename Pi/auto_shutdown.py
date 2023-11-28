import os
import time

import RPi.GPIO as GPIO
from lib_oled96 import ssd1306
from PIL import ImageFont
from smbus import SMBus

i2cbus = SMBus(1)
oled = ssd1306(i2cbus)
draw = oled.canvas
FreeSans12 = ImageFont.truetype("FreeSans.ttf", 12)
FreeSans16 = ImageFont.truetype("FreeSans.ttf", 16)
FreeSans20 = ImageFont.truetype("FreeSans.ttf", 20)

time.sleep(2)

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.OUT)

GPIO.output(16, False)

# The GPIO pinis used to communicate between the two programms. We know this is ugly and multithreading would have made it way easier, but it works for V1. V2 will be better

print("LOW")

while True:
    button_state = GPIO.input(23)
    if button_state == False:
        oled.cls()
        oled.display()
        draw.text((0, 0), "Ausgeschaltet", font=FreeSans20, fill=1)
        draw.text((0, 30), "Die Box schaltet sich", font=FreeSans12, fill=1)
        draw.text((0, 45), "jetzt aus", font=FreeSans12, fill=1)
        oled.display()
        print("HIGH")
        GPIO.output(16, True)
        time.sleep(2)
        oled.cls()
        oled.display()
        os.system("poweroff")
        while True:
            print("fertig")
            time.sleep(100)
