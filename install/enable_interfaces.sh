#!/bin/bash

# Enable 1-Wire
cmd=$(cat /boot/config.txt | grep '#dtoverlay=w1-gpio')

if [[ $cmd == "#dtoverlay=w1-gpio" ]]
then
    sudo sed -i -e 's/#dtoverlay=w1-gpio/dtoverlay=w1-gpio/g' /boot/config.txt
else
    #sudo echo 'dtoverlay=w1-gpio' >> /boot/config.txt          # Permission denied
    sudo sh -c 'echo "dtoverlay=w1-gpio" >> /boot/config.txt'
fi

# Enable I2C
sudo sed -i -e 's/#dtparam=i2c_arm=on/dtparam=i2c_arm=on/g' /boot/config.txt
sudo sed -i -e 's/dtparam=i2c_arm=off/dtparam=i2c_arm=on/g' /boot/config.txt

# REBOOT NEEDED !!!
