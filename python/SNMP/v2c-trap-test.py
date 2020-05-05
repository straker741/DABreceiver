"""
SNMPv2c TRAP via NOTIFICATION-TYPE
++++++++++++++++++++++++++++++++++

Initialize TRAP message contents from variables specified
in *NOTIFICATION-TYPE* SMI macro.

* SNMPv2c
* with community name 'public'
* over IPv4/UDP
* send TRAP notification
* with TRAP ID 'linkUp' specified as a MIB symbol
* include values for managed objects implicitly added to notification
  (via NOTIFICATION-TYPE->OBJECTS)

"""#
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    sendNotification(
        SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget(('192.168.178.24', 162)),
        ContextData(),
        'trap',
        #NotificationType(
        #    ObjectIdentity('1.3.6.1.4.1.1916.1.1.6.0.2')                #'1.3.6.1.6.3.1.1.5.2'
        #).addVarBinds(
        #    ("1.3.6.1.2.1.1.1.0", OctetString('Example Notificator')),              # 1.3.6.1.2.1.1.1 - sysDescr
        #    ("1.3.6.1.2.1.1.5.0", OctetString('Notificator Example'))               # 1.3.6.1.2.1.1.5 - sysName
        #)
        (
            ("1.3.6.1.2.1.1.1.0", OctetString('Example Notificator')),              # 1.3.6.1.2.1.1.1 - sysDescr
            ("1.3.6.1.2.1.1.5.0", OctetString('Notificator Example'))               # 1.3.6.1.2.1.1.5 - sysName
        )
        # .0 at the end of every variable signifies it is a scalar 
    )
)

if errorIndication:
    print(errorIndication)

#1.3.6.1 - internet

#towerID
#towerName
#????