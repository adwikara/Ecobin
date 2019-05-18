## Install Drivers to RasPi
sudo apt-get install libusb-1.0-0-dev
wget http://www.phidgets.com/gpgkey/pubring.gpg
sudo apt-key add pubring.gpg
sudo su -c "echo 'deb http://www.phidgets.com/debian stretch main' >> /etc/apt/sources.list.d/phidgets.list"
sudo apt-get update
sudo apt-get install libphidget22 libphidget22extra phidget22networkserver  
sudo reboot

## Setup Phidget Modules
```
python setup.py install
```

## Run Motor
```
python sort_motor.py
```
