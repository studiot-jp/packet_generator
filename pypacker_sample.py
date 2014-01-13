#! /usr/bin/env python3
#-*- coding: utf-8 -*-

import socket
from pypacker.layer12 import ethernet
from pypacker.layer3 import ip
from pypacker.layer4 import tcp
from pypacker.psocket import SocketHndl

def main():
    # Ethernet header
    eth = ethernet.Ethernet()
    eth.src = b"\x00\x0c\x29\xdf\xe3\xc0"
    eth.dst = b"\x00\x0c\x29\x29\x85\xd2"
    eth.type = ethernet.ETH_TYPE_IP
    # IP header
    ipp = ip.IP()
    ipp.src = socket.inet_aton("172.16.13.165")
    ipp.dst = socket.inet_aton("172.16.13.162")
    ipp.p = ip.IP_PROTO_TCP
    # TCP header
    tcpp = tcp.TCP()
    tcpp.sport = 60001
    tcpp.dport = 80
    tcpp.flags = tcp.TH_SYN

    ipp.data = tcpp
    ipp.len = len(str(ip))
    ipp.id = 1
    tcpp._TCP__calc_sum()
    ipp._IP__calc_sum()
    eth.data = ipp

    # open sockets using the socket handler
    sock_l2 = SocketHndl(iface_name="eth1", mode=SocketHndl.MODE_LAYER_2)
    # send raw bytes
    sock_l2.send(eth.bin())


if __name__ == "__main__":
    main()
