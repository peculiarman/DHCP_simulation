# -*- coding: cp936 -*-
import argparse, sys, socket, time

MAX_BYTES = 1024
ADDRESS = "192.168.1.1"
Dest = "255.255.255.255"
listenPort = 67
clientPort = 68

class DHCP_server(object):

	def dhcpoffer_get(self):
		packet = b''
		packet += b'\x02'   #Message type: Boot Request (1)
		packet += b'\x01'   #Hardware type: Ethernet
		packet += b'\x06'   #Hardware address length: 6
		packet += b'\x00'   #Hops: 0 
		packet += b"\x39\x03\xf3\xfa"       #Transaction ID
		packet += b'\x00\x00'    #Seconds elapsed: 0
		packet += b'\x00\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
		packet += b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
		packet += b'\xc0\xa8\x00\x0a'   #Your (client) IP address: 0.0.0.0
		packet += b'\xc0\xa8\x00\x01'   #Next server IP address: 0.0.0.0
		packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
		packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
		packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
		packet += b'\x00' * 64  #Server host name not given
		packet += b'\x00' * 128 #Boot file name not given
		packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
		packet += b'\x35\x01\x02'   #DHCP Message Type = DHCP Discover
		packet += b'\x01\x04\xff\xff\xff\x00'
		packet += b'\x3a\x04\x00\x00\x07\x08'
		packet += b'\x3b\x04\x00\x00\x0c\x4e'
		packet += b'\x33\x04\x00\x00\x0e\x10'
		packet += b'\x36\x04\x7f\x00\x00\x01'
		packet += b'\xff'
		packet += b'\x00' * 26 #end padding
		return packet
	
	def dhcpack_get(self):
		
		packet = b''
		packet += b'\x02'   #Message type: Boot Request (1)
		packet += b'\x01'   #Hardware type: Ethernet
		packet += b'\x06'   #Hardware address length: 6
		packet += b'\x00'   #Hops: 0 
		packet += b"\x39\x03\xf3\xfb"       #Transaction ID
		packet += b'\x00\x00'    #Seconds elapsed: 0
		packet += b'\x00\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
		packet += b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
		packet += b'\xc0\xa8\x00\x0a'   #Your (client) IP address: 0.0.0.0
		packet += b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
		packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
		packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
		packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
		packet += b'\x00' * 64  #Server host name not given
		packet += b'\x00' * 128 #Boot file name not given
		packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
		packet += b'\x35\x01\x05'   #Option: (t=53,l=1) DHCP Message Type = DHCP Discover
		packet += b'\x3a\x04\x00\x00\x07\x08'
		packet += b'\x3b\x04\x00\x00\x0c\x4e'
		packet += b'\x33\x04\x00\x00\x0e\x10'
		packet += b'\x36\x04\x7f\x00\x00\x01'
		packet += b'\x01\x04\xff\xff\xff\x00'
		packet += b'\xff'
		packet += b'\x00' * 26   #End Option
		return packet

	def server(self):

		print("DHCP server is starting.")
		dest = (Dest, clientPort)
		
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		sock.bind(('0.0.0.0', listenPort))
		
		
		
		while 1:
			#try:
				print('\nwaiting DHCPDISCOVER')
				data, address = sock.recvfrom(MAX_BYTES)
				print('\nreciving DHCPDISCOVER')
				print(data)
		
				#offer.
				print('\nsending DHCPOFFER')
				#data = ack.encode('ascii')
				data = self.dhcpoffer_get()
				#sock.sendto(data, address)
				sock.sendto(data, dest)
		
				while 1:
					#try:
						print('\nwaiting DHCPREQUEST')
						data, address = recvfrom(MAX_BYTES)
						print('\nreciving DHCPREQUEST')
						print(data)
						
						#Acknowledge.
						print('\nsending DHCPACK')
						#data = ack2.encode('ascii')
				
						#sock.sendto(data, address)
						sock.sendto(data, dest)
				
						break
					
					#except (KeyboardInterrupt, SystemExit):
						#raise
					#except:
						#traceback.print_exc()
				break
			
			#except (KeyboardInterrupt, SystemExit):
				#raise
			#except:
			#	traceback.print_exc()
				
if __name__ == '__main__':
	dhcp_server = DHCP_server()
	dhcp_server.server()
