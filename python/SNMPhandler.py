from pysnmp.hlapi import *
import sysInfo

def __get_towerInfo():
    pass

def sendTrap():
    # sysD == sysDescr:     1.3.6.1.2.1.1.1.0
    # sysN == sysName:      1.3.6.1.2.1.1.5.0
    # sysL == sysLocation:  1.3.6.1.2.1.1.6.0
    sysD = sysInfo.get_sysDescr()
    sysN = sysInfo.get_sysName()
    sysL, target = sysInfo.get_sysLocation_and_target()

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
