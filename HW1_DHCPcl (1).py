# -*- coding: cp936 -*-
import argparse, sys, socket, time
from datetime import datetime

MAX_BYTES = 1024
Src = "0.0.0.0"
Dest = "255.255.255.255"
listenPort = 68
serverPort = 67

class DHCP_client(object):

	def client(self):

		print("DHCP client is starting.")
		dest = (Dest, serverPort)

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		sock.bind((Src, listenPort))
		print("\nsending DHCPDISCOVER")
		#data, address = sock.recvfrom(MAX_BYTES)
		data = DHCP_client.dhcpdiscover_get()
		sock.sendto(data, dest)
		print("\nwaiting DHCPOFFER")
		data, address = sock.recvfrom(MAX_BYTES)
		print("\nreciving DHCPOFFER")
		print(data)

		print("\nsend DHCPREQUEST")
		data = DHCP_client.dhcprequest_get()
		sock.sendto(data, dest)
		print("\nwaiting DHCPACK")
	
		data, address = sock.recvfrom(MAX_BYTES)
		print("\nreciving DHCPACK")
		print(data)




	def dhcpdiscover_get():
		packet = b''
		packet += b'\x01'   #Message type: Boot Request (1)
		packet += b'\x01'   #Hardware type: Ethernet
		packet += b'\x06'   #Hardware address length: 6
		packet += b'\x00'   #Hops: 0 
		packet += b"\x39\x03\xf3\xfa"       #Transaction ID
		packet += b'\x00\x00'    #Seconds elapsed: 0
		packet += b'\x00\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
		packet += b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
		packet += b'\x00\x00\x00\x00'   #Your (client) IP address: 0.0.0.0
		packet += b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
		packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
		packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
		packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
		packet += b'\x00' * 64  #Server host name not given
		packet += b'\x00' * 128 #Boot file name not given
		packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
		packet += b'\x35\x01\x01'   #Option: (t=53,l=1) DHCP Message Type = DHCP Discover
		packet += b'\x3d\x07\x01\x00\x26\x9e\x04\x1e\x9b'
		packet += b'\x32\x04\x00\x00\x00\x00'   #Option: (t=55,l=3) Parameter Request List
		packet += b'\x37\x04\x00\x00\x00\x00'
		packet += b'\xff'   #End Option
		packet += b'\x00' * 7
		return packet

	def dhcprequest_get():
		packet = b''
		packet += b'\x01'   #Message type: Boot Request (1)
		packet += b'\x01'   #Hardware type: Ethernet
		packet += b'\x06'   #Hardware address length: 6
		packet += b'\x00'   #Hops: 0 
		packet += b"\x39\x03\xf3\xfb"       #Transaction ID
		packet += b'\x00\x00'    #Seconds elapsed: 0
		packet += b'\x80\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
		packet += b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
		packet += b'\xC0\xA8\x01\x64'   #Your (client) IP address: 0.0.0.0
		packet += b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
		packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
		packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
		packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
		packet += b'\x00' * 64  #Server host name not given
		packet += b'\x00' * 128 #Boot file name not given
		packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
		packet += b'\x35\x01\x03'   #Option: (t=53,l=1) DHCP Message Type = DHCP Discover
		packet += b'\x3d\x07\x01\x00\x26\x9e\x04\x1e\x9b'
		packet += b'\x32\x04\xc0\xa8\x00\x0a'   #Option: (t=55,l=3) Parameter Request List
		packet += b'\x36\x04\xc0\xa8\x00\x01'
		packet += b'\x37\x04\x01\x03\x06\x2a'
		packet += b'\xff'   #End Option
		packet += b'\x00'
		return packet

if __name__ == '__main__':
	dhcp_client = DHCP_client()
	dhcp_client.client()