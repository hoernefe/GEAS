# GEAS
**A mobile sensor platform for big scale collection of geodata.**

The Geodata Acquisition and Analysis System aims to develop a mobile system that enables large-scale and efficient collection of geodata. The collected data should be presented in a clear and insightful way to draw conclusions for sustainable and health-oriented urban development optimization.

One successful application of this system was a data collection campaign on the topic of fine particle pollution in the Karlsruhe area. For this purpose, a sensor module based on a Raspberry Pi was mounted on bicycles to systematically capture data of the city area of Karlsruhe. The data collected by the sensor module were stored in a database and processed by a Python program. The results were visualized using GIS software.

The geodata acquisition and analysis system has multiple use cases and enables decision-making based on sound data for sustainable and health-oriented urban development.

## Sensor platform
In every sensor box has a Raspberry Pi is build in. On This Pi the Code from the folder labeld Pi is running. All used libraries have to be installed. For thosw which weren't already pip wasused for the installation. The font-files from the oled library had some problems, but we were able to fix these by putting our ode inside it's folder. To automatically start everything we added the following at the end of the bashrc file:
```
echo Running at boot
python /home/pi/lib_oled96/Upload_sql_oled_4.py> out.txt 2> err.txt &
python /home/pi/lib_oled96/auto_shutdown.py > out2.txt 2> err2.txt &
```

## Database
For the database we used a phpMyAdmin server, which is very similar to MySQL. Any SQL-based system should do the trick.

The structure we used is the following:
![](/pictures/database_structure.JPG)
(Breitengrad is german for latitude and Langengrad means longitude)

## Analysis
The geodata from the database requires processing for a good visualization. To do this, we wrote some python code. It can be found in the analysis folder. For the python code all neccesary libraries must be imported. Alternatively our .exe file may be used, but your computer will give you a virus threat warning and you shouldn't trust people on the internet, so try to use the python file.
Currently the interface is in German, but we're working on an English version for easier use.

## Parts
1x Raspberry Pi Zero WH 

1x Raspberry Pi heatsink 

1x 16gb SD-Card 

1x SDS011 PM Sensor 

1x Neo6m GPS-Module 

1x GPS-Antenna 

1x Huawei E5576-320 SIM-Router 

1x SIM-Card  

1x Anker Powercore 1000mAh power bank 

1x 90-degree angled USB-A to Micro-USB cable 

1x 0,96in i2c OLED-Display 

1x Small plexiglass sheet 

1x On-Off Rocker switch 

1x NO Push-Button 

12x M3 Nylon Nuts + Bolts 

Wires for soldering 

Heat-Shrink tubing  

Double sided tape 

Hot glue 

1x Bike mount (https://www.amazon.de/Rixen-Kaul-KlickFix-Bottlefix-Flaschenhalter/dp/B07498GS82) 

 

## Instructions
Print casing, intermediate floor and sensor opening filter with 1,75mm PLA filament 

Mount filter on sensor opening (heat to attach) and place sensor into designated space 

Solder wires as shown on the soldering diagram. 

Cut and solder angled USB cable as shown on soldering diagram. 

Connect angled USB cable to power bank and place into designated spot, load SIM-card into SIM-Router and place into designated spot, cover with intermediate floor, feed the ends of soldered USB cable through the hole in the middle 

Screw Raspberry Pi Zero onto intermediate floor, connect the original Micro-USB end to power input 

Connect remaining Micro-USB end to the SIM-Router below 

Screw GPS-Module into place, connect to Raspberry Pi with the soldered cables, tape antenna onto back wall of the top part, cut a small hole into the side of the top for the antenna cable 

Connect Sensor to Raspberry Pi via the included adapter 

Glue plexiglass into designated hole in the top, glue OLED-display underneath, connect to Raspberry Pi with soldered cables 

Place rocker switch into hole next to “power” in the top, connect to Raspberry Pi with the soldered cables 

Place NO-Button into hole next to “eco” in the top, connect to the cut cable from step 4 

Load Program onto SD-Card, load into Raspberry Pi 

Close module by screwing top onto bottom 

Begin data collection by activating the rocker switch, end session by first pressing the “eco”-Button until the display reads “Ausschalten”, only then turn off the module via the rocker switch. 
