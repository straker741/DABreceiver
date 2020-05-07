#!/usr/bin/python3
# Autor: Jakub Svajka
# Date:  11.3.2020
# -------------------- # Adafruit_SSD1306 library # ------------------------- #
# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import glob
import time
import MySQLdb

# Initialization
try:
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
except:
    print("Thermometer DS18B20 not found!")
    exit()

try:
    db = MySQLdb.connect(host="localhost", user="stu", passwd="korona2020", db="bakalarka")
    cursor = db.cursor()
except:
    print("Could not connect to database!")
    exit()

# Adafruit_SSD1306 library and 128x32 I2C display
display = True
try:
    import Adafruit_SSD1306
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)    # on the PiOLED this pin isnt used
    disp.begin()
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Define some constants to allow easy resizing of shapes.
    padding = 8
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0
except:
    display = False
    print("Display is not connected or library Adafruit_SSD1306 is missing!")

if display:
    # Load font
    try:
        font = ImageFont.truetype('/home/pi/DABreceiver/fonts/Greenscr.ttf', 18)
        degreeC = " " + u"\u00F8" + "C"
    except:
        print("Could not find custom font file. Setting default font.")
        font = ImageFont.load_default()

# Functions
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0       
        return temp_c

# Main loop
try:
    while True:
        mytemp = read_temp()
        print(mytemp)
        loggit = "INSERT INTO temperature (temp) VALUES (" + str(mytemp) + ")"
        cursor.execute(loggit)
        db.commit()
        if display:
            # Draw a black filled box to clear the image.
            draw.rectangle((0,0,width,height), outline=0, fill=0)   
            # Write out text.
            draw.text((x, top), str(mytemp) + degreeC, font=font, fill=255)
            # Display image.
            disp.image(image)
            disp.display()
        time.sleep(1)
except KeyboardInterrupt:
    print("End of temperature readings!")
    cursor.close()
    db.close()