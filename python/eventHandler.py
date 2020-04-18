# Autor: Jakub Svajka
# Datum: 22.3.2020

import fileHandler
import subprocess

path = "~/DABreceiver/python/"
mode = fileHandler.getConfig()[1]

if mode == "explore":
    # Kill processes if exist
    subprocess.run("pkill -f welle-cli", shell=True)
 
    # Check how many processes with name explore.py are running
    # Note that when starting process ps fx, total 3 processes are found
    p = subprocess.Popen("ps fx | grep explore.py", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    out = p.communicate()[0].splitlines()

    # We do not need to kill explore.py
    if len(out) < 3:
        # Start explore.py
        subprocess.run("nohup python " + path + "explore.py >/dev/null 2>&1 &", shell=True)
elif mode == "monitor":
    # Kill processes if exist
    subprocess.run("pkill -f explore.py", shell=True)
    subprocess.run("pkill -f welle-cli", shell=True)

    # Start monitor.py
    subprocess.run("nohup python " + path + "monitor.py >/dev/null 2>&1 &", shell=True)
