#!/usr/bin/python3

import subprocess
import fileHandler
import json

def __get_HW():
    """Hardware."""
    p = subprocess.Popen("cat /proc/cpuinfo | grep 'model name\|Model'", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].splitlines()
    return (data[-1][9:] + data[0][12:])

def __get_SW():
    """Software."""
    p = subprocess.Popen("cat /proc/version | sed 's/ (.*)//'", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0]
    return data

def __get_NW():
    """Network."""
    p = subprocess.Popen("lsusb -t | grep Vendor | cut -f 1 -d ',' | cut -f 2 -d 'v'", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].strip()
    p = subprocess.Popen("lsusb | grep 'Device 00" + data + "' | cut -f 3 -d ':' | cut -f 2- -d ' '", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].strip()
    return data

def get_sysDescr():
    """A textual description of the entity. 
    This value should include the full name and version 
    identification of the system's hardware type, software operating-system, and networking software."""
    
    result  = "Hardware: " + __get_HW() + "\n"
    result += "Software: " + __get_SW()
    result += "Network:  " + __get_NW()
    return result  

def get_sysName():
    """An administratively-assigned name for this managed node. 
    By convention, this is the node's fully-qualified domain name. 
    If the name is unknown, the value is the zero-length string."""

    p = subprocess.Popen("hostname -I", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    result = p.communicate()[0].strip()
    return result

def get_sysLocation_and_target():
    """The physical location of this node. 
    If the location is unknown, the value is the zero-length string."""
    data = fileHandler.rFile("../trapConfig.txt")
    if data == False:
        return False
    else:
        return data.splitlines()

if __name__ == "__main__":
    hw = __get_HW()
    sw = __get_SW()
    nw = __get_NW()
    hn = get_sysName()

    info = {
        "hardware": hw,
        "software": sw,
        "network": nw,
        "hostname": hn
    }

    # convert into JSON:
    out = json.dumps(info)
    print(out)
