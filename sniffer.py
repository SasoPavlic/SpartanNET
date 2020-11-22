from scapy.all import Dot11, sniff
import subprocess
import time
import re

BSSID_FILE = "bssid.txt"
APs = []

def manf(bss):
    file = open(BSSID_FILE, 'r')
    for line in file.read().splitlines():
        bssid_man = line[0:8]
        if bssid_man == bss[0:8]:
            man_name = line[18:]
            return (re.sub('\ |\?|\.|\!|\/|\;|\:|\,', '', man_name)) + bss[8:]
        else:
            continue 

def stopfilter(x):
    # If we need filtering
    # Dummy filter (FF:FF:FF:xx:xx:xx)
    x = x.getlayer(Dot11)
    if hasattr(x, 'addr2') and hasattr(x,'info'):
        MAC = str(x.addr2).upper()
        SSID = x.info.decode("utf-8") 
        if MAC == 'FF:FF:FF:xx:xx:xx' and len(SSID)!=0:
            print(f"Device with entered MAC address found with SSID: {x.info}")
            input("Continue [Enter]...")
            return True
    else:
        return False


def start_sniffing(inf_name):
    timeout_sec = int(input("Enter timeout in seconds (Recomended=100): "))
    print("Monitoring probe requests:")
    sniff(iface=inf_name, prn=PacketHandler,
          timeout=timeout_sec, stop_filter=stopfilter)
    for bss in APs:
        print(f"Captured device with MAC address: {manf(bss)}")
    input("Continue [Enter]...")
    
def PacketHandler(packet):    
    if packet.haslayer(Dot11):
        bss = str(packet.getlayer(Dot11).addr2).upper()
        if bss not in APs:
            APs.append(bss)
        if (packet.type == 0 or packet.type == 2) and (packet.subtype == 4 or packet.subtype ==12):
            sn = str(packet.getlayer(Dot11).addr2).upper()            
            if hasattr(packet, 'info'):
                print("Acces point MAC: %s with dBm: %s SSID: %s " %(manf(sn), packet.dBm_AntSignal, packet.info))
            else:
                print("Acces point MAC: %s with dBm: %s " %(manf(sn), packet.dBm_AntSignal))
                