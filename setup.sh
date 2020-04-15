#!/bin/bash
cd ~/DABreceiver/
sudo apt-get -y update && sudo apt-get -y upgrade

# pip
sudo apt-get install -y python3-pip python-pip
# git
sudo apt-get install -y git
# cmake
sudo apt-get install -y cmake
# expect
sudo apt-get install -y expect

# Apache Web Server
sudo apt-get install -y apache2
sudo cp ~/DABreceiver/html/* /var/www/html

# MySQL
sudo apt-get install -y mariadb-server

# Setting up MySQL
~/DABreceiver/install/mysql/mysql.sh

# Creating a MySQL Database and User
~/DABreceiver/install/mysql/mysql_db_user.sh

# Creating MySQL tables
~/DABreceiver/install/mysql/mysql_tables.sh

# MySQL connectors
sudo apt-get install -y php-mysql
sudo apt-get install -y python-mysqldb
sudo apt-get install -y libmysqlcppconn-dev

# pyrtlsdr - Python kniznica na komunikaciu s driverom
# https://pypi.org/project/pyrtlsdr/
sudo pip install pyrtlsdr
# pysnmp
sudo pip install pysnmp

# I2C
sudo apt install -y python-imaging python-smbus i2c-tools python3-pil

# Adafruit 
git clone https://github.com/adafruit/Adafruit_SSD1306.git

# Welle.io
sudo apt-get install -y libfftw3-dev librtlsdr-dev libfaad-dev libmp3lame-dev libmpg123-dev
git clone https://github.com/straker741/welle.io
~/DABreceiver/install/welle.sh
# ak to nepojde skus nieco z tohto: 
#sudo apt install mesa-common-dev libglu1-mesa-dev libpulse-dev libsoapysdr-dev libairspy-dev libasound2-dev libusb-1.0-0-dev


# -------------------------------------------------------------------------------



