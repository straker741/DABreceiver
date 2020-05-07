#!/bin/bash

function validate_ip()
{
    # source: https://www.linuxjournal.com/content/validating-ip-address-bash-script
    local  ip=$1
    local  stat=1

    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS=$IFS
        IFS='.'
        ip=($ip)
        IFS=$OIFS
        [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        stat=$?
    fi
    return $stat
}

DEFAULT_COLOUR='\033[0;37m'
RED_COLOUR='\033[1;31m'
YELLOW_COLOUR='\033[1;33m'
GREEN_COLOUR='\033[1;32m'
while [[ 0 ]]
do
    echo -e "${YELLOW_COLOUR}Zadajte IPv4 adresu, na ktorej sa nachadza SNMP manazer: ${DEFAULT_COLOUR}"
    read -p "" target
    if validate_ip $target; then break; else echo -e "${RED_COLOUR}Zadali ste nespravny tvar IP adresy!"; fi
done
echo -e "${GREEN_COLOUR}OK!"
echo -e "${YELLOW_COLOUR}Slovne popiste, kde sa bude riadene zariadenie nachadzat: ${DEFAULT_COLOUR}"
read -p "" location
echo -e "${GREEN_COLOUR}OK!${DEFAULT_COLOUR}"
echo $location > ~/DABreceiver/trapConfig.txt
echo $target >> ~/DABreceiver/trapConfig.txt

# Changing the access permissions of files
chmod +x ~/DABreceiver/install/welle.sh
chmod +x ~/DABreceiver/install/enable_interfaces.sh
chmod +x ~/DABreceiver/install/change_apache2_configuration.sh
chmod +x ~/DABreceiver/install/mysql/mysql.sh
chmod +x ~/DABreceiver/install/mysql/mysql_tables.sh
chmod +x ~/DABreceiver/install/mysql/mysql_db_user.sh
chmod +x ~/DABreceiver/python/*
sudo chmod 666 ~/DABreceiver/python/bandwidth.txt

sudo apt-get update && sudo apt-get -y upgrade

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
~/DABreceiver/install/change_apache2_configuration.sh

# PHP
sudo apt-get install -y php libapache2-mod-php

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
sudo apt-get install -y python-mysqldb python3-mysqldb
sudo apt-get install -y libmysqlcppconn-dev
sudo pip install mysql-connector-python

# RTLSDR - defaultne je uz nainstalovany
sudo apt-get install -y rtl-sdr

# pyrtlsdr - Python kniznica na komunikaciu s driverom
# https://pypi.org/project/pyrtlsdr/
sudo pip install pyrtlsdr
# pysnmp
sudo pip3 install pysnmp

# 1-Wire a I2C
#sudo apt-get install -y libopenjp2-7
sudo apt-get install -y python-smbus i2c-tools python3-pil
~/DABreceiver/install/enable_interfaces.sh

# Adafruit
#sudo apt-get install -y python3-rpi.gpio
sudo pip3 install Adafruit-SSD1306

# MATPLOTLIB
sudo apt-get install -y python-matplotlib

# Welle.io
sudo apt-get install -y libfftw3-dev librtlsdr-dev libfaad-dev libmp3lame-dev libmpg123-dev
git clone https://github.com/straker741/welle.io ~/DABreceiver/welle.io
~/DABreceiver/install/welle.sh

# Download some data for testing
wget -c https://sdr.kt.agh.edu.pl/sdrdab-decoder/downloads/data/Record3_katowice_iq.raw -P ~/DABreceiver/welle.io/data/

# radio Kraków, low noise 30-40 dB (?)
wget -c https://sdr.kt.agh.edu.pl/sdrdab-decoder/downloads/data/antena-1_dab_229072kHz_fs2048kHz_gain42_1.raw -P ~/DABreceiver/welle.io/data/


echo -e "${GREEN_COLOUR}REBOOTING!${DEFAULT_COLOUR}"
# END !
sudo reboot
