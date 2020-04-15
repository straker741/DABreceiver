# http://snmplabs.com/pysnmp/docs/pysnmp-hlapi-tutorial.html

from pysnmp.hlapi import *

"""
'1.3.6.1.6.3.1.1.5.2' - warmStart
'1.3.6.1.2.1.1.1.0'   - sysDescr 
    This value should include the full name and version identification of
    the system's hardware type, software operating-system, and networking software.


"""

def sendTrap():
    print("Sending trap!")
    errorIndication, errorStatus, errorIndex, varBinds = next(
        sendNotification(
            SnmpEngine(),
            CommunityData('public', mpModel=1),                 # SNMPv2
            UdpTransportTarget(('192.168.178.35', 162)),     # Represents IPv4 adress
            ContextData(),
            'trap',                                             # type of Notification (either 'trap' or 'inform')
            NotificationType(
                ObjectIdentity('1.3.6.1.6.3.1.1.5.2')           # warmStart
            ).addVarBinds(
                ('1.3.6.1.6.3.1.1.4.3.0', '1.3.6.1.4.1.20408.4.1.1.2'),     # snmpTrapEnterprise OBJECT-TYPE
                ('1.3.6.1.2.1.1.1.0', OctetString('Windows 10'))
            )
        )
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))


sendTrap()