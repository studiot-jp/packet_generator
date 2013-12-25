#!/usr/bin/env python
#-*- coding: utf-8 -*-
import socket

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind(("0.0.0.0", 1234))
    print s.recvfrom(65535)
    
#!/usr/bin/env python
#-*- coding: utf-8 -*-
import socket
import struct
import random

class Packet:
	#45 00 0017 0000 4000 ff02 7de2 7f000001 7f000001 313233
	def __init__(self):
		self.version = 4 #ip version
		self.hl = 5 #internet header length
		self.tos = 0 #type of service
		#self.length = 0 #length
		self.id = 0 #identification
		self.flags = 0b010 #reserved+don't fragment(df)+more fragments(mf)
		self.offset = 0 #fragment offset
		self.ttl = 255 #time to live
		self.protocol = 255 #ip protocol raw: 255
		self.checksum = 0 #header checksum 
		self.src = "\x7f\x00\x00\x01" #source ip address
		self.dst = "\x7f\x00\x00\x01" #destination ip address
		self.data = ""
	
	def _get_addr(self, name):
		return socket.inet_aton(socket.gethostbyname(name))
	
	def _get_checksum(self, data):
		result = 0
		for i in xrange(0, len(data), 2):
			try:
				result += (ord(data[i])<<8)+ord(data[i+1])
			except IndexError: #if len(data) % 2 != 0
				result += (ord(data[i])<<8)
		while result > 0xffff:
			result = (result>>16)+(result&0xffff)
		return (~result)&0xffff
	
	def set_src(self, name):
		self.src = self._get_addr(name)
	
	def set_dst(self, name):
		self.dst = self._get_addr(name)
	
	def build(self):
		pack = struct.pack
		length = self.hl*4+len(self.data)
		result = ""
		result += chr((self.version<<4)+self.hl)
		result += chr(self.tos)
		result += pack(">H", length)
		result += pack(">H", self.id)
		result += pack(">H", (self.flags<<13)+self.offset)
		result += chr(self.ttl)
		result += chr(self.protocol)
		result += pack(">H", self._get_checksum(
			result+"\x00\x00"+self.src+self.dst))
		result += self.src+self.dst+self.data
		return result

def UDPPacket(data, dst_addr, src_addr, **kwargs):
	p = Packet()
	for attr, value in kwargs.iteritems():
		setattr(p, attr, value)
	p.protocol = 0x11 #udp
	p.set_src(src_addr[0])
	p.set_dst(dst_addr[0])
	
	pack = struct.pack
	udp_header = pack(">HHH", src_addr[1], dst_addr[1], len(data)+8)
	pseudo_header = p.src+p.dst+"\x00\x11"+udp_header[4:]
	checksum = p._get_checksum(pseudo_header+udp_header+data)
	udp_header += pack(">H", checksum)
	
	p.data = udp_header+data
	return p.build()

if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
	s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1) #dont include ip header
	
	p = UDPPacket("testa", ("127.0.0.1", 1234), ("127.0.0.1", 11111))
	print p.encode("hex")
	s.sendto(p, ("127.0.0.1", 0))
	
	#data, addr = s.recvfrom(0xffff)
	#print addr
	#print data.encode("hex")
