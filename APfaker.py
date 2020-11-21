from scapy.all import *
from main import run_command
import time

# TODO Change hardcoded interface names to parameters
# Examples:
#   -eth0
#   -wlan0mon

def create_AP(ssid):
    print(f"Setting up Wi-Fi AP with SSID name: {ssid}\n")
    run_command("sudo nohup hostapd hostapd.conf")

    time.sleep(3)

    print(f"Starting DHCP server\n")
    run_command("sudo ifconfig wlan0mon up 192.168.2.1 netmask 255.255.255.0")
    run_command("sudo route add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.2.1")
    run_command("sudo nohup dnsmasq -C dnsmasq.conf -d")
    
    time.sleep(3)
    
    print(f"Creating NAT to forward traffic from eth0 -> wlan0mon\n")
    run_command("sudo iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE")
    run_command("sudo iptables --append FORWARD --in-interface wlan0mon -j ACCEPT")
    run_command("sudo -i;nohup echo 1 > /proc/sys/net/ipv4/ip_forward")   
    time.sleep(3)
    input("Continue [Enter]...")

# TODO function to spam fake Wi-Fi APs [currently just sitting here :)]
def send_beacon(ssid, mac, iface, infinite=True):
    dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac, addr3=mac)
    # ESS+privacy to appear as secured on some devices
    beacon = Dot11Beacon(cap="ESS+privacy")
    essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
    frame = RadioTap()/dot11/beacon/essid
    
    sendp(frame, inter=0.1, loop=1, iface=iface, verbose=0, count=50)