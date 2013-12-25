#!/usr/bin/env python
"""
Author:     phillips321 contact at phillips321.co.uk
License:    CC BY-SA 3.0
Use:        Simple python arp ping
Released:   www.phillips321.co.uk
Dependencies:
    netifaces (needs python-dev then easy_install netifaces)
ChangeLog:
    v0.2 - fixed response to search for target ip
    v0.1 - first release
"""
version = "0.2"
import socket
import struct
import sys
import netifaces
import binascii
if len(sys.argv) == 3 :
    target = sys.argv[1]
    interface = sys.argv[2]
elif len(sys.argv) == 2: 
    target = sys.argv[1]
    interface = "eth0"
    print "No interface given so defaulting to eth0"
else: #no values defined print help
    print "Usage: %s IP [interface] \n   eg: %s 192.168.1.0 eth0" % (sys.argv[0],sys.argv[0])
    exit(1)

networkdetails = netifaces.ifaddresses(interface)
ipaddress = networkdetails[2][0]['addr']
macaddress = networkdetails[17][0]['addr']
print "Attempting to arp ping %s from %s using %s" % (target,ipaddress,macaddress)

# create packet
eth_hdr = struct.pack("!6s6s2s", '\xff\xff\xff\xff\xff\xff', macaddress.replace(':','').decode('hex'), '\x08\x06')              
arp_hdr = struct.pack("!2s2s1s1s2s", '\x00\x01', '\x08\x00', '\x06', '\x04', '\x00\x01')          
arp_sender = struct.pack("!6s4s", macaddress.replace(':','').decode('hex'), socket.inet_aton(ipaddress))
arp_target = struct.pack("!6s4s", '\x00\x00\x00\x00\x00\x00', socket.inet_aton(target))

count = 5
while count != 0:
    count = count - 1
    try:
        # send packet
        rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0806))
        rawSocket.bind((interface, socket.htons(0x0806)))
        rawSocket.send(eth_hdr + arp_hdr + arp_sender + arp_target)
        
        # wait for response
        rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0806))
        rawSocket.settimeout(0.5)
        response = rawSocket.recvfrom(2048)
        if target == socket.inet_ntoa(response[0][28:32]):
            print "Response from the folloiwing mac " + binascii.hexlify(response[0][6:12]).swapcase()
            break
        continue
    except socket.timeout:
        print "Attempt number %i did not get a response" % (count + 1)
        continue
