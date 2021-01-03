from scapy.all import *
from main import run_command
import time
from subprocess import Popen, PIPE
import configparser

# TODO Change hardcoded interface names to parameters
# Examples:
#   -eth0
#   -wlan0mon

def prepare_AP_reqierments():
    ifconfig_command = "ifconfig wlan0mon up 192.168.2.1 netmask 255.255.255.0;"
    route_add_command = "sudo route add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.2.1;"
    
    nat_command = "sudo iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE;"
    forward_command = "sudo iptables --append FORWARD --in-interface wlan0mon -j ACCEPT;"
    
    Popen("sudo gnome-terminal -x "+ ifconfig_command, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    Popen("sudo gnome-terminal -x "+ route_add_command, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    Popen("sudo gnome-terminal -x "+ nat_command, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    Popen("sudo gnome-terminal -x "+ forward_command, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)    

def create_AP(ssid):    
    print("Preparing requirments...")
    prepare_AP_reqierments()
    
    print(f"Setting up Wi-Fi AP with SSID name: {ssid}\n")
    Popen("sudo gnome-terminal -x hostapd hostapd.conf", stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    time.sleep(3)

    print(f"Starting DHCP server\n")          
    dnsmasq_command = "sudo dnsmasq -C dnsmasq.conf -d"
    Popen("sudo gnome-terminal -x "+ dnsmasq_command, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    time.sleep(3)
    
    # WARNING - if AP will not have internet run following command manually with sudo rights! 
    # sudo echo 1 > /proc/sys/net/ipv4/ip_forward"
    print(f"Creating NAT to forward traffic from eth0 -> wlan0mon\n")    
    ipv4_forward_command = "echo 1 > /proc/sys/net/ipv4/ip_forward"
    Popen("sudo gnome-terminal -x "+ ipv4_forward_command, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    time.sleep(3)
    input("Continue [Enter]...")
