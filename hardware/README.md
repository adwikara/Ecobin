## Welcome to Ecobin's hardware repository

### RasPi/
The Ecobin uses the Raspberry Pi 3B+, which is has the highest specs among other RasPi microprocessors. The RasPi serves as the main microprocessor for the Ecobin embedded system. The RasPi runs on a Debian-based operating system called Raspbian, which is based on the Linux kernel. This enables the RasPi to easily run Python scripts. To ensure that the Raspbian software is up to date, you can run these lines of code:
```
sudo apt-get update
sudo apt-get dist-upgrade
```

The Ecobin has a main Python script which is required to run to operate the device. This script calls all the sensors and is able to communicate to the API. The script is called ecobin.py
```
python3 ecobin.py
```
The script ecobin.py is modular in that it is separated to modules for the different functionalities of the Ecobin device. The script runs continuously for as long as the device is in operation, and constantly checks for a high signal from the motion sensor, which activates all the other functionalities.

![Screen Shot 2019-04-26 at 10 07 30 PM](https://user-images.githubusercontent.com/33497234/56843506-b4790780-686f-11e9-9971-9a209dbbf5e7.png)

### PIR Motion Sensor/
The Ecobin uses a PIR motion sensor which is able to detect peripheral motion. This sensor is placed next to the lid to detect hand motion. Once a motion is detected, the RasPi drives a high signal to the lid motor, which will open the automatic lid to allow the user to throw away objects into the Ecobin. The PIR sensor has three ports: 5V, GND, and OUT. The 5V and GND is necessary to power the sensor. The OUT port goes into a RasPI GPIO port, which signals the RasPi that it detected motion. The sensor also has two potentiometers to configure the sensitivity and the time delay. Time delay sets how long the output should be high when there is motion. This value could go from 5 seconds to 5 minutes. For the Ecobin, we have set it to the lowest value, 5 seconds. The sensitivity sets up the detection range, from 3 meters to 7 meters. We have set this value to the least sensitive, to minimize the effects of possible noise. The code to run the PIR sensor can be found in the folder individual_sensors, where there is a file motion.py. 
```
python3 motion.py
```
![Screen Shot 2019-04-26 at 10 06 14 PM](https://user-images.githubusercontent.com/33497234/56843492-97443900-686f-11e9-8cdc-58d3bf6010da.png)

### PiCamera/
A PiCamera v2 Camera Board was selected as the main sensor to capture an image of the object. This sensor is highly compatible with the RasPi, which eases the functionality and usage. This camera also has a 8 megapixel resolution which is capable of capturing 3280 x 2464 pixel images. The code to take a picture can be found in the individual_sensors folder, where you can run the code capture.py. 
```
python3 capture.py
```
We have adjusted the specifications of the PiCamera to ensure optimal image classification. Some of the required specifications involved adjusting the values of resolution, ISO, sharpness, brightness, and contrast. The following are the final values for the specifications:
1. Resolution = (240,240)
2. ISO = 500
3. Sharpness = 60
4. Brightness = 70
5. Contrast = 60

A resolution of 240x240 was selected to ease the object classification process, which is done in the cloud. Last of all, before the image is pushed to the API, it has to be encoded. Instead of converting the image into a vector, which could take millions of characters, we encoded the picture using base64. This significantly reduces the number of characters. The backend then decodes the picture and classifies it.
The PiCamera is connected via a band directly to the PiCamera port of the Raspberry Pi. In terms of placement, the camera is mounted onto the wall of the imaging stage, angled in such a way that allows it to capture as much of the imaging stage as possible. To ensure adequate lighting conditions, an LED strip is used.

![Screen Shot 2019-04-26 at 9 57 12 PM](https://user-images.githubusercontent.com/33497234/56843410-57308680-686e-11e9-9ba2-6386b77a2279.png)

*Note on the orientation of how the PiCamera is attached to the RasPi

### LED Strip + Transistor/
We used 12V white LED strip lights activated via a transistor switch to illuminate the imaging platform.
The transistor used is a PN-2222A npn-BJT and the resistor values used were 2.2 kOhms and 2MOhms, between the base and the RasPi GPIO and between the RasPi GPIO and ground respectively. The RasPi sends a high signal when a motion is detected towards the transistor, which triggers the switch and turns on the LED strip. The RasPi sends a low signal after a picture is taken, which turns off the LED strip. The LED strip is placed horizontally above the camera, in order to minimize glare while at the same time ensuring that the whole imaging platform is well lit during imaging.

### Ultrasonic Sensor/
The Ecobin uses two HC-SR04 ultrasonic sensors, which are used to detect the capacity of the recycling and trash bins. An ultrasonic sensor essentially sends out ultra-high frequency sound waves towards a directed point, which reflect onces it hits an object. This is the mechanism that enables the Ecobin to detect capacity. The code to test out the sensors can be found in the individual_sensors folder.

Besides the power ports, hot and ground, there are two other ports on the ultrasonic sensor, namely Trigger and Echo. Trigger signals the sensor to send out the sound waves and Echo relays the detected echoes back to the RasPi. The time difference between the sending out of a sound wave and the time it is received back is used to measure distance to the directed point.
```
ultrasonic.py
```

![Screen Shot 2019-04-26 at 10 09 42 PM](https://user-images.githubusercontent.com/33497234/56843526-04f06500-6870-11e9-8da5-522c64fa9692.png)

### Stepper Motors/
The Ecobin deploys two types of stepper motors to fulfill its electro-mechanical needs. The first stepper motor, which is a NEMA-17 stepper, is used to actuate the automatic lid. This motor has 200 steps per revolution and has a power rating of 12V and 350mA. This means that the motor has a 1.8 step angle, and that one step will rotate the motor by 1.8 degrees. For the lid, we only need is to rotate 1/4 of a full revolution, meaning we need around 50 steps. The lid will require 50 steps to open, and another 50 steps to close it (but the motor has to move in reverse direction). This motor is controlled by an Arduino because an Arduino has a built-in library for stepper motors. The RasPi and Arduino have GPIO ports that are connected to one another. The Arduino constantly waits for the RasPi to send a high signal, which will trigger the automatic lid. This high signal is sent out when there is motion detected. The Arduino code to operate this motor can be found in the motors folder:
```
lid_motor.ino
```

![Screen Shot 2019-04-26 at 10 00 12 PM](https://user-images.githubusercontent.com/33497234/56843433-b1314c00-686e-11e9-92e9-4890921ec07b.png)

*The following image uses a Metro microcontroller for the setup. A Metro or Arduino can be used either way for this application.

The second stepper is a 28STH32 NEMA-11 Bipolar Stepper with 100:1 Gearbox, which is a NEMA stepper that is connected to a gearbox. This slows down the speed of the NEMA but it increases the torque. This motor is used to actuate the sweeper (the sorting mechanism). This motor has 0.018° step angle and 32 kg·cm of torque. Due to the gearbox, this motor cannot be controlled by an Arduino. It has its own microcontroller called the PhidgetStepper Bipolar HC. This microcontroller is compatible with the RasPi and hence the motor can be programmed using Python. The program to control this motor can be found in the motors folder.
```
sort_motor.py
```
The program essentially commands the motor to rotate to a targeted position. We want the sweeper to rotate 180 degrees, either clockwise or anti-clockwise, in order to push the object into the trash or recyclable bin. The calculated value for rotating 180 degrees was a position of 160000 for clockwise, and -160000 for anti-clockwise. This ensures that the sweeper is always returned to its default position after each sorting action.

![Screen Shot 2019-04-26 at 10 02 18 PM](https://user-images.githubusercontent.com/33497234/56843448-fc4b5f00-686e-11e9-98d7-41f830eee02b.png)

*The 28STH32 stepper with the Phidget controller


### Power Requirements

The Ecobin device requires a dual output power supply unit that is able to supply 5V and 12V, 5V to power the Raspberry Pi and 12V to power the motors and LED strip. The 12V output port needs to be able to provide up to 2.5A of current for the 28STH32 NEMA-11 Bipolar Stepper, while the 5V port needs to be able to provide up to 2A for the Raspberry Pi which also powers all the sensors and cameras attached to it. We settled on the Mean Well RD-65 for our power supply unit as it is the only model available that can provide 2.5A from the 12V output port.

![Screen Shot 2019-04-26 at 10 24 03 PM](https://user-images.githubusercontent.com/33497234/56843695-0458ce00-6872-11e9-8126-d79161f426a3.png)

*Mean Well RD-65 PSU

The power supply unit rectifies the 120V AC voltage from the outlet and converts it into 5VDC voltage and a 12VDC at the two output ports. The following are the power requirements for every electronic device in the Ecobin:

12V Devices:
- LED Strip
- 28STH32 NEMA-11 Bipolar Stepper
- NEMA-17 Stepper Motor

5V Devices:
- Raspberry Pi + PiCamera
- Arduino
- PIR Motion Sensor
- Ultrasonic Sensor

As the RasPi also outputs 5VDC power from itself, the sensors and Arduino can be powered directly from the RasPi, thus allowing for a smaller number of required direct connections into the power supply unit.

Despite the seemingly high desired power output requirement, the system does not regularly consume as much power as the biggest consumers of power, namely the motors, sit idle most of the time. However, the high power rating of the Mean Well RD-65 power supply unit is required when the motor functions to sort heavy objects.

### Procedure
The following steps will ensure the functionality, performance, and safety of the hardware system:
1. Test the sensors individually from the code in the individual_sensors folder
2. Test the motors individually from the code in the motors folder
3. Put all the Python scripts in one directory (ecobin.py, code from individual_sensors, and from motors)
4. Make sure all the connections are correct based on the diagram in the schematic
5. Make sure the electronics are mounted properly in the housing (no metal scraps that could short the electronics)
6. Plug in the PSU cord to the outlet
7. Ecobin should start operating!

### Bill of Materials
![Screen Shot 2019-04-26 at 9 42 52 PM](https://user-images.githubusercontent.com/33497234/56843297-c5744980-686c-11e9-8606-41902f7e7e2c.png)


### Hardware Schematics 
The following schematic shows the pinout diagrams of the sensors, power supply unit, and the Raspberry Pi. It shows the connections between the RasPi GPIO ports and the sensors.

![58978337_275805123371284_3091383731559071744_n](https://user-images.githubusercontent.com/33497234/56843290-a5448a80-686c-11e9-92be-0cb53263cc1b.png)

### Ecobin Housing Design
The following schematics shows three main components of the Ecobin housing:
1. The sorting mechanism

![Screen Shot 2019-04-26 at 9 37 51 PM](https://user-images.githubusercontent.com/33497234/56843357-767ae400-686d-11e9-8a27-fade89836b68.png)

2. The lid mechanism

![Screen Shot 2019-04-26 at 9 38 00 PM](https://user-images.githubusercontent.com/33497234/56843361-8266a600-686d-11e9-899d-71e025a6c2b8.png)


3. The fully rendered assembly

![Screen Shot 2019-04-26 at 9 38 08 PM](https://user-images.githubusercontent.com/33497234/56843362-8a264a80-686d-11e9-8e69-c8190d38063a.png)
