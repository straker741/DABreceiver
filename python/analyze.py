# Autor: Jakub Svajka
# Datum: 22.3.2020

import DABplus
import configHandler
import subprocess

# Getting frequency
f = configHandler.getConfig()[0]
# Getting corresponding channel
ch = configHandler.DABchannels[f]

# Loading kernel module
sdr = DABplus.RtlSdr()
# Check bandwidth before start of welle-cli
bandwidth = DABplus.checkBandwidth(sdr, f)
# Unloading kernel module
sdr.close()

if False:
    range = 1000
    if (1536000 - range < bandwidth < 1536000 + range):
        cmd = "nohup ~/welle-cli -c " + ch + " >/dev/null 2>&1 &"
        # Executing command - oppening pipe
        subprocess.run(cmd, shell=True)
else:
    configHandler.wFile("~/python/test.txt", bandwidth)