# SpartanNET
### Description 📝
Automated Wi-Fi vulnerabilities exploiter written in Python language for beginners.
It tries to reduce needed knowledge about penetration testing to a bare minimum **(Plug&Select&Play)**.
### What it can do? 👀
* **Change Wi-Fi card state** (monitor <-> managed)
* **Rename Wi-Fi card** (sometimes it's useful to quickly change the name back to original, if we got stuck somewhere (other scripts failed, process canceled, etc...)
* **Sniffs probe requests** in area (get client MAC, dBm, SSID name of "last" AP)
* **Create Evil-Twin AP** 
NOTE: If AP will note have internet access try to execute:
`echo 1 > /proc/sys/net/ipv4/ip_forward`
* **Capture WPA2 handshake** (de-Auth clients on selected Wi-Fi AP, capturing handshake, outputs **handshake.cap** file for leter usage with Hashcat) 
### Requirements ✅
Anaconda enviroment with Python 3.7.x (To run SpartanNET script (main.py) a.k.a. console menu)
##### INSTALL ALL
pip3 install -r requirements.txt
##### MANUAL INSTALL
* pip install console-menu
* pip install menu
* pip install scapy
### PLUS (in case you want to Capture the WPA2 handshake) 
* Anaconda enviroment with **Python 2.7.x** and name **py2** (to capture WPA2 handshake (captureHandShake.py).
*In other words, SpartanNET (main.py) will run (captureHandShake.py) it for you if it can find the enviroment **py2 with Python 2.7.x)**
### Documentation 📘 
* Faculty paper written in Slovenian language (you can still translate it to English and figure out a lot of things 😏)
[Google Docs link](https://docs.google.com/document/d/1uIwj4-HJyQNUju9b_4l_-atU1H54xv4_uDSFtwpmb2o/edit?usp=sharing)

