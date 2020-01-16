#import env as env
#!/usr/bin/env python

import subprocess
import optparse
import re
import sys

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC Address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    if not options.new_mac:
        parser.error("[-] Please specify an MAC address, use --help for more info")
    return options

def get_current_mac(interface):
    ifconfig_result = str(subprocess.check_output(["ifconfig", interface]))
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("[-] Could not read MAC address")



# subprocess.call("ifconfig " + interface + " down", shell=True)
# subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
# subprocess.call("ifconfig " + interface + " up", shell=True)
options = get_arguments()
current_mac = get_current_mac(options.interface)    #before changing MAC
print("Current MAC = ", str(current_mac))
if current_mac == None:
    print("[-] Sorry!!Program getting terminated")
    sys.exit(1)
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)  #after changing MAC
if current_mac == options.new_mac:
    print("[+] MAC address sucessfully got changed to", current_mac)
else:
    print("[-] MAC address did not get changed")