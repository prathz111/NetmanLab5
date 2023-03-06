#
# """
# snmpwalk -v2c -c netman 198.51.101.22 1.3.6.1.2.1.4.20.1.1
# snmpwalk -v 2c -c netman 198.51.101.22 IP-MIB::ipAdEntAddr
# snmpwalk -v 2c -c netman 198.51.101.22 IF-MIB::ifDescr (2.2.1.8)
# snmpwalk -v 2c -c netman 198.51.101.22 1.3.6.1.2.1.4.20.1
# """
#
# from pysnmp.hlapi import *
#
# oid = "1.3.6.1.2.1.4.20.1.1"
#
# for (errorIndication, errorStatus, errorIndex, varBinds) in \
#         nextCmd(SnmpEngine(),
#                 CommunityData('netman', mpModel=0),
#                 UdpTransportTarget(('198.51.101.22', 161)),
#                 ContextData(),
#                 ObjectType(ObjectIdentity(oid))):
#     if errorIndication:
#         print(errorIndication)
#         break
#     elif errorStatus:
#         print('%s at %s' % (errorStatus.prettyPrint(),
#                             errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
#         break
#     else:
#         for varBind in varBinds:
#             print('%s = %s' % (varBind[0], varBind[1]))


import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

SYSNAME = '.1.3.6.1.2.1.4.34.1.3.2'

host = '198.51.101.22'
snmp_ro_comm = 'netman'

# Define a PySNMP CommunityData object named auth, by providing the SNMP community string
auth = cmdgen.CommunityData(snmp_ro_comm)

# Define the CommandGenerator, which will be used to send SNMP queries
cmdGen = cmdgen.CommandGenerator()

# Query a network device using the getCmd() function, providing the auth object, a UDP transport
# our OID for SYSNAME, and don't lookup the OID in PySNMP's MIB's
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    auth,
    cmdgen.UdpTransportTarget((host, 161)),
    cmdgen.MibVariable(SYSNAME),
    lookupMib=False,
)

# Check if there was an error querying the device
if errorIndication:
    sys.exit()

# We only expect a single response from the host for sysName, but varBinds is an object
# that we need to iterate over. It provides the OID and the value, both of which have a
# prettyPrint() method so that you can get the actual string data
for oid, val in varBinds:
    print(oid.prettyPrint(), val.prettyPrint())