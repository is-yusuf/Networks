from scapy.all import *

# Ethernet Layer
ethernet = Ether(src="7c:24:99:f1:94:20", dst="ff:ff:ff:ff:ff:ff")

# IP Layer
ip = IP(src="10.133.140.69", dst="10.133.159.255")

# UDP Layer
udp = UDP(sport=137, dport=137)

# NetBIOS Name Service
nbns = NBNSRegistrationRequest()  # Replace with the appropriate NetBIOS packet structure if needed.

# Combine the layers
packet = ethernet / ip / udp / nbns

# Send the packet (requires root/administrator privileges)
sendp(packet, iface="en0") 
