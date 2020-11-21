from scapy.all import Dot11, sniff
import subprocess
import time

def stopfilter(x):
    # If we need filtering
    # Dummy filter
    if x.name == 'TEST':
        return True
    else:
        return False


def start_sniffing():
    timeout_sec = int(input("Enter timeout in seconds (Recomended=100): "))
    print("Monitoring probe requests:")
    sniff(iface="wlan0mon", prn=PacketHandler,
          timeout=timeout_sec, stop_filter=stopfilter)   

# TODO Add RSSI to get signal strength
def PacketHandler(packet):
    if packet.haslayer(Dot11):
        if packet.type == 0 and packet.subtype == 4:            
            print("Acces point MAC: %s with SSID: %s " %(packet.addr2, packet.info))
            

