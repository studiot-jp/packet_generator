#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from dpkt import ethernet
from dpkt import ip
from dpkt import tcp
from dpkt.psocket import SocketHndl
import socket
 
def main():
    # Ethernet header
    eth      = ethernet.Ethernet()
    eth.src = "\x00\x0c\x29\xdf\xe3\xca"
    eth.dst = "\x00\x0c\x29\x29\x85\xdc"
    eth.type = ethernet.ETH_TYPE_IP
    # IP header
    ipp     = ip.IP()
    ipp.src = socket.inet_aton("172.168.177.133")
    ipp.dst = socket.inet_aton("172.168.177.136")
    ipp.p   = ip.IP_PROTO_TCP
    # TCP header
    tcpp       = tcp.TCP()
    tcpp.sport = 60001
    tcpp.dport = 80
    tcpp.flags = tcp.TH_SYN
    tcpp.sum = 0
    tcpp.data = "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10"
 
    ipp.data = tcpp
    ipp.len = len(ipp.pack())
    ipp.sum = 0
    eth.data = ipp

    # open sockets using the socket handler
    sock_l2 = SocketHndl(iface_name="eth2", mode=SocketHndl.MODE_LAYER_2)
    # send raw bytes
    sock_l2.send(eth.pack())

if __name__ == '__main__':
    main()
