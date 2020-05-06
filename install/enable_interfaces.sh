#!/bin/bash

# Enable 1-Wire
sudo echo 'dtoverlay=w1-gpio' >> /boot/config.txt

# Enable I2C
sudo sed -i -e 's/#dtparam=i2c_arm=on/dtparam=i2c_arm=on/g' /boot/config.txt
sudo sed -i -e 's/dtparam=i2c_arm=off/dtparam=i2c_arm=on/g' /boot/config.txt