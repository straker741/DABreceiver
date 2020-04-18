# Autor: Jakub Svajka
# Datum: 22.3.2020

import DABplus
import fileHandler
from time import sleep

# Getting frequency
f = fileHandler.getConfig()[0]

# Loading kernel module
sdr = DABplus.RtlSdr()
try:
    while True:
        # Check bandwidth 
        bandwidth = DABplus.checkBandwidth(sdr, f)
        fileHandler.wFile("~/DABreceiver/python/bandwidth.txt", bandwidth)

        sleep(4)
except:
    # Unloading kernel module
    sdr.close()