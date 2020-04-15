# Autor: Jakub Svajka
# Datum: 22.3.2020

import configHandler
import subprocess

path = "~/DABreceiver/python/"
mode = configHandler.getConfig()[1]

if mode == "search":
    # Kill processes if exist
    subprocess.run("pkill -f welle-cli", shell=True)
 
    # Check how many processes with name search.py are running
    # Note that when starting process ps fx, total 3 processes are found
    p = subprocess.Popen("ps fx | grep search.py", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    out = p.communicate()[0].splitlines()

    # We do not need to kill search.py
    if len(out) < 3:
        # Start search.py
        subprocess.run("nohup python " + path + "search.py >/dev/null 2>&1 &", shell=True)
elif mode == "analyze":
    # Kill processes if exist
    subprocess.run("pkill -f search.py", shell=True)
    subprocess.run("pkill -f welle-cli", shell=True)

    # Start analyze.py
    subprocess.run("nohup python " + path + "analyze.py >/dev/null 2>&1 &", shell=True)
