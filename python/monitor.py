# Autor: Jakub Svajka
# Datum: 22.3.2020

import DABplus
import fileHandler
import subprocess

# Getting frequency
f = fileHandler.getConfig()[0]
# Getting corresponding channel
ch = fileHandler.DABchannels[f]

# Loading kernel module
sdr = DABplus.RtlSdr()
# Check bandwidth before start of welle-cli
bandwidth = DABplus.checkBandwidth(sdr, f)
# Unloading kernel module
sdr.close()

if True:
    
    range = 1000
    if (1536000 - range < bandwidth < 1536000 + range):
        cmd = "nohup ~/welle-cli -c " + ch + " >/dev/null 2>&1 &"
        # Executing command - oppening pipe
        subprocess.run(cmd, shell=True)
    else:
        print("Bandwidth is not in the range. Aborting!")
else:
    fileHandler.wFile("/home/pi/DABreceiver/python/bandwidth.txt", bandwidth)