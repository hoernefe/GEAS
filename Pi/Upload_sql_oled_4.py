from __future__ import print_function
from datetime import *
import RPi.GPIO as GPIO
import serial, struct, sys, time, subprocess, time, string, pynmea2, socket, os
import urllib
import mysql
import mysql.connector

from lib_oled96 import ssd1306
from smbus import SMBus
from PIL import ImageFont

datenDesWetters = [0,0,0,0,0,0]

print("Upload_sql_oled_4.py wurde gestartet (das ist eine nachrich, die ich ins Proragramm geschriben habe)")

i2cbus = SMBus(1)
oled = ssd1306(i2cbus)
draw = oled.canvas
FreeSans12 = ImageFont.truetype('FreeSans.ttf', 12)
FreeSans16 = ImageFont.truetype('FreeSans.ttf', 16)
FreeSans20 = ImageFont.truetype('FreeSans.ttf', 20)


GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


oled.cls()
oled.display()
draw.text((0, 0), "Wilkommen", font=FreeSans20, fill=1)
draw.text((0, 30), "Bitte warten bis Werte" , font=FreeSans12, fill=1)
draw.text((0, 45), "erscheinen" , font=FreeSans12, fill=1)
oled.display()

time.sleep(5)

status = "Not connected"

while status != "Connected":
        try:
                url = "https://www.google.com"
                urllib.urlopen(url)
                status = "Connected"
        except:
                status = "Not connected"
        oled.cls()
        oled.display()
        draw.text((0, 0), "Verbindungsfehler", font=FreeSans16, fill=1)
        draw.text((0, 30), "Keine Verbindung zum" , font=FreeSans12, fill=1)
        draw.text((0, 45), "Internet vorhanden" , font=FreeSans12, fill=1)
        oled.display()
        print(status)
        time.sleep(2)

oled.cls()
oled.display()
draw.text((0, 0), "Verbunden", font=FreeSans16, fill=1)
draw.text((0, 30), "Verbindung zum" , font=FreeSans12, fill=1)
draw.text((0, 45), "Internet vorhanden" , font=FreeSans12, fill=1)
oled.display()

time.sleep(2)

#enter your data for the server
mydb = mysql.connector.connect(
  host="enter host",
  user="enter user",
  password="enter password",
  database="enter database"
)

mycursor = mydb.cursor()

now = datetime.now()

anzahl=0

gezeigt=False

f=open('daten.csv', 'a')


DEBUG = 0
CMD_QUERY_DATA = 4

ser = serial.Serial()
ser.port = "/dev/ttyUSB0"
ser.baudrate = 9600

ser.open()
ser.flushInput()

def construct_command(cmd, data=[]):
    assert len(data) <= 12
    data += [0,]*(12-len(data))
    checksum = (sum(data)+cmd-2)%256
    ret = "\xaa\xb4" + chr(cmd)
    ret += ''.join(chr(x) for x in data)
    ret += "\xff\xff" + chr(checksum) + "\xab"

    if DEBUG:
        dump(ret, '> ')
    return ret

def process_data(d):
    r = struct.unpack('<HHxxBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(ord(v) for v in d[2:8])%256
    return [pm25, pm10]

def read_response():
    byte = 0
    while byte != "\xaa":
        byte = ser.read(size=1)

    d = ser.read(size=9)

    if DEBUG:
        dump(d, '< ')
    return byte + d

def cmd_query_data():
    ser.write(construct_command(CMD_QUERY_DATA))
    d = read_response()
    values = []
    if d[1] == "\xc0":
        values = process_data(d)
    return values


#getting the weatherdata from openweathermap
def wetterdaten():
    import urllib
    import time

    status = "Not connected"

    while status != "Connected":
        try:
            urllib.urlopen("https://www.google.com")
            status = "Connected"
        except:
            status = "Not connected"
        #print(status)
        time.sleep(2)

    wetterdaten = [0,0,0,0,0,0]

    response=urllib.urlopen("http://api.openweathermap.org/data/2.5/weather?appid=[enter APPID]&q=Karlsruhe") #the brackets have to be replaced with your own ID

    x = response.read()

    #print('Empfangene Daten')
    #print x

    #print('-------------------')
    #print('Temperatur in Grad Celsius')

    temp_string = x.split("temp",1)[1]
    cut_temp_string = temp_string.split(",",1)[1]
    temp_string =temp_string.replace(cut_temp_string, "")
    temp_string = temp_string[2:]
    cut_temp_string = temp_string[-1:]
    temp_string = temp_string.replace(cut_temp_string, "")
    temp = float(temp_string)
    temp = temp - 273.15
    #print temp
    wetterdaten [0] = temp

    #print('-------------------')
    #print('Feuchtigkeit in Prozent')
    humi_string = x.split("humidity",1)[1]
    cut_humi_string = humi_string.split(",",1)[1]
    humi_string = humi_string.replace(cut_humi_string, "")
    humi_string = humi_string[2:]
    cut_humi_string = humi_string[-1:]
    humi_string = humi_string.replace(cut_humi_string, "")
    cut_humi_string = humi_string[-1:]
    if cut_humi_string == "}":
        #print "extra"
        humi_string = humi_string.replace(cut_humi_string, "")
    humi = float(humi_string)
    #print humi
    wetterdaten [1] = humi

    #print('-----------------')
    #print('Luftdruck in hPa')

    pres_string = x.split("pressure",1)[1]
    cut_pres_string = pres_string.split(",",1)[1]
    pres_string = pres_string.replace(cut_pres_string, "")
    pres_string = pres_string[2:]
    cut_pres_string = pres_string[-1:]
    pres_string = pres_string.replace(cut_pres_string, "")
    pres = float(pres_string)
    #print pres
    wetterdaten [2] = pres

    #print('----------------')
    #print('Windgeschwindigkeit in m/s')

    sped_string = x.split("speed",1)[1]
    cut_sped_string = sped_string.split(",",1)[1]
    sped_string = sped_string.replace(cut_sped_string, "")
    sped_string = sped_string[2:]
    cut_sped_string = sped_string[-1:]
    sped_string = sped_string.replace(cut_sped_string, "")
    sped = float(sped_string)
    #print sped
    wetterdaten [3] = sped

    #print('---------------')
    #print('Windrichtung in Grad')

    deg_string = x.split("deg",1)[1]
    cut_deg_string = deg_string.split(",",1)[1]
    deg_string = deg_string.replace(cut_deg_string, "")
    deg_string = deg_string[2:]
    cut_deg_string = deg_string[-1:]
    deg_string = deg_string.replace(cut_deg_string, "")
    deg = float(deg_string)
    #print deg
    wetterdaten [4] = deg

    #print('-------------------')
    #print('Wolken in Prozent')
    clou_string = x.split("all",1)[1]
    cut_clou_string = clou_string.split(",",1)[1]
    clou_string = clou_string.replace(cut_clou_string, "")
    clou_string = clou_string[2:]
    cut_clou_string = clou_string[-1:]
    clou_string = clou_string.replace(cut_clou_string, "")
    cut_clou_string = clou_string[-1:]
    if cut_clou_string == "}":
        #print "extra"
        clou_string = clou_string.replace(cut_clou_string, "")
    clou = float(clou_string)
    #print clou
    wetterdaten [5] = clou

    #print('-------------------')
    #print('Liste')
    #print wetterdaten
    return wetterdaten

datenDesWetters = wetterdaten()

print(datenDesWetters)

anzahl = 0

t0 = time.time()


#when all data is available it is sen to the server and a massage is displayed on the oled
while True:

    t1 = time.time()
    if t1-t0 > 900:
        datenDesWetters = wetterdaten()
        t0 = time.time()

    if GPIO.input(16):
        print("gestoppt")
        f.close()
        oled.cls()
        oled.display()
        oled.display()
        draw.text((0, 0), "Ausgeschaltet", font=FreeSans20, fill=1)
        draw.text((0, 30), "Die Box schaltet sich" , font=FreeSans12, fill=1)
        draw.text((0, 45), "jetzt aus" , font=FreeSans12, fill=1)
        oled.display()
        while True:
            time.sleep(1)

    print("loop")
    now = datetime.now()
    port="/dev/ttyAMA0"
    serG=serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=serG.readline()
    values = cmd_query_data();
    if newdata[0:6] == "$GPRMC":
        newmsg=pynmea2.parse(newdata)
        lat=newmsg.latitude
        lng=newmsg.longitude

        if(lat + lng != 0):

            #gezeigt=False

            gps = "Latitude :" + str(lat) + ",  Longitude: " + str(lng)
            print(gps)
            print(now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S"), ", PM2.5: ", values[0], ", PM10: ", values[1])

            sql = "INSERT INTO FeinstaubVonPi (ID, Datum, Zeit, Breitengrad, Langengrad, PM25, PM10, temperature, humidity, pressure, windSpeed, windAngle, clouds) VALUES (" '1' + ',' + now.strftime("%Y%m%d") + ',' + now.strftime("%H%M%S") + ','+ str(lat) + ',' + str(ln$            mycursor.execute(sql)
            mydb.commit()

            print(mycursor.rowcount, "record inserted.")

            print(now.strftime("%Y/%m/%d"), now.strftime("%H:%M:%S"), ',',str(lat), ',', str(lng), ',', values[0], ',', values[1], file=f)
            anzahl = anzahl+1

            oled.cls()
            oled.display()

            draw.text((0, 0), "PM 2,5: ", font=FreeSans16, fill=1)
            draw.text((70, 0), str(values[0]), font=FreeSans16, fill=1)

            draw.text((0, 15), "PM 10: ", font=FreeSans16, fill=1)
            draw.text((70, 15), str(values[1]), font=FreeSans16, fill=1)

            draw.text((0, 30), str(lat), font=FreeSans16, fill=1)
            draw.text((0, 45), str(lng), font=FreeSans16, fill=1)


            oled.display()

        else:

            #if(not gezeigt):

            oled.cls()
            oled.display()
            gezeigt=True

            draw.text((0, 0), "Verbindungsfehler", font=FreeSans16, fill=1)
            draw.text((0, 30), "Es werden keine GPS" , font=FreeSans12, fill=1)
            draw.text((0, 45), "Daten empfangen" , font=FreeSans12, fill=1)

            oled.display()
            time.sleep(1 )
