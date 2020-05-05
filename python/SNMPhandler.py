from pysnmp.hlapi import *
import subprocess
import fileHandler

def __get_sysDescr():
    """A textual description of the entity. 
    This value should include the full name and version 
    identification of the system's hardware type, software operating-system, and networking software."""
    # Hardware
    p = subprocess.Popen("cat /proc/cpuinfo | grep 'model name\|Model'", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].splitlines()
    result = "Hardware: " + data[-1][9:] + data[0][12:] + "\n"
    # Software
    p = subprocess.Popen("cat /proc/version | sed 's/ (.*)//'", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0]
    result += "Software: " + data
    # Network
    p = subprocess.Popen("lsusb -t | grep Vendor | cut -f 1 -d ',' | cut -f 2 -d 'v'", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].strip()
    p = subprocess.Popen("lsusb | grep 'Device 00" + data + "' | cut -f 3 -d ':' | cut -f 2- -d ' '", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].strip()
    result += "Network:  " + data
    return result  

def __get_sysName():
    """An administratively-assigned name for this managed node. 
    By convention, this is the node's fully-qualified domain name. 
    If the name is unknown, the value is the zero-length string."""

    p = subprocess.Popen("hostname -I", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    result = p.communicate()[0].strip()
    return result

def __get_sysLocation_and_target():
    """The physical location of this node. 
    If the location is unknown, the value is the zero-length string."""
    data = fileHandler.rFile("../trapConfig.txt")
    if data == False:
        return False
    else:
        return data.splitlines()

def __get_towerInfo():

    pass

def sendTrap():
    # sysD == sysDescr:     1.3.6.1.2.1.1.1.0
    # sysN == sysName:      1.3.6.1.2.1.1.5.0
    # sysL == sysLocation:  1.3.6.1.2.1.1.6.0
    sysD = __get_sysDescr()
    sysN = __get_sysName()
    sysL, target = __get_sysLocation_and_target()

    errorIndication, errorStatus, errorIndex, varBinds = next(
        sendNotification(
            SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget((target, 162)),
            ContextData(),
            'trap',
            (
                ("1.3.6.1.2.1.1.1.0", OctetString(sysD)),
                ("1.3.6.1.2.1.1.5.0", IpAddress(sysN)),
                ("1.3.6.1.2.1.1.6.0", OctetString(sysL))
            )
            # .0 at the end of every variable signifies it is a scalar 
        )
    )

    if errorIndication:
        print(errorIndication)
    else:
        print("Trap sent successfully!")
