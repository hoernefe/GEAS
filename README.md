# GEAS
**A mobile sensor platform for big scale collection of geodata.**

The Geodata Acquisition and Analysis System aims to develop a mobile system that enables large-scale and efficient collection of geodata. The collected data should be presented in a clear and insightful way to draw conclusions for sustainable and health-oriented urban development optimization.

One successful application of this system was a measurement campaign on the topic of fine particle pollution in the Karlsruhe area. For this purpose, a measurement module based on a Raspberry Pi was mounted on bicycles to systematically capture measurement data of the city area of Karlsruhe. The data collected by the measurement module were stored in a database and processed by a Python program. The results were visualized using GIS software.

The geodata acquisition and analysis system has multiple use cases and enables decision-making based on sound data for sustainable and health-oriented urban development.

## Sensor platform

## Database
For the databased we used a phpMyAdmin server which is very similar to MySQL. Any SQL basedsystem should do the trick.

The structe we used is the following:
![](/pictures/database_structure.JPG)
(Breitengrad is german for latitude and Langengrad means longitude)

## Analysis
The geodata from the database has to be proccesed to create a good visualisation. To do this we wrote some python code. It can be found in the analysis folder. For the python code all neccesary libraries must be importet. Alternativle cou can use our .exe file, but you're computer will give you a virus threat warning and you shoukd'nt trust people on the internet so try to use the python file.
Currently the interface is in german, but we're working on an english version so it is easier to use.
