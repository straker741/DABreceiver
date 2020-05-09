#!/bin/bash

sudo mv -r ~/DABreceiver/html/* /var/www/html
sudo chown -R pi:pi /var/www/html
sudo chmod 666 /var/www/html/config.txt
sudo chmod 777 /var/www/html/obrazky
sudo sed -i -e 's/APACHE_RUN_USER=www-data/APACHE_RUN_USER=pi/g' /etc/apache2/envvars
sudo sed -i -e 's/APACHE_RUN_GROUP=www-data/APACHE_RUN_GROUP=pi/g' /etc/apache2/envvars