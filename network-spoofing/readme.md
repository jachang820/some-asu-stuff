# UDP/TCP Spoofing

## Purpose

A test server on a VPN only takes UDP/TCP connections from a trusted source IP, but returns a flag to another IP specified by the trusted source. For TCP, the transaction IDs are generated using a flawed mechanism of randomly shuffling the order of 4 bytes, and mutating 1 byte every several connections.

These couple of programs use **scapy** to spoof the trusted source IP, then run a replay attack on TCP to guess the transaction ID in order to retrieve the flag. The IP only works on a VPN hosted by the university.

## Issues

There is an issue where the Linux kernel sends a reset (RST() because it is
unaware of what Scapy is doing in userland, according to the documentation. So
the solution to that is to use a local firewall to block the kernel:

> sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -s [LOCAL IP]-j DROP

where [LOCAL IP] is replaced by the tunneling IP at the time.

## Method

The code would grab a TCP sequence using my own IP, and then replay that
sequence number twice using the source IP. In another window, I used
Scapy's sniff() to monitor UDP payloads, since it's easier to pick out the
flag,

> capture = sniff(iface="tap0", filter='udp', prn=lambda p: p[UDP].payload) 

## Dependencies

**Python 3.8.5** -- <https://www.python.org/>
**Scapy 2.4.3** -- <https://scapy.net/index>