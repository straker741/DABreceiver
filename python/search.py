# Autor: Jakub Svajka
# Datum: 22.3.2020

import DABplus
import configHandler
from time import sleep

# Loading kernel module
sdr = DABplus.RtlSdr()
while True:
    try:
        # Getting frequency
        f = configHandler.getConfig()[0]

        DABplus.doPSD(sdr, f)

        sleep(5)
    except:
        # Unloading kernel module
        sdr.close()
        break