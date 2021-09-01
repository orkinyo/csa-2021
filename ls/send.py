#!/usr/bin/python3
import requests
import os


DELETE = 1
#get_commands:
if os.path.exists("./commands.zip") and DELETE:
    os.remove("./commands.zip")
os.system("zip ./commands.zip ./commands.txt")

with open("./commands.zip", "rb") as f:
    data = f.read()

print("[+] Zipped!")

url = "https://ls.csa-challenge.com/upload-zip"

s = requests.Session()

response = s.post(url, headers= {"Content-Type": "application/zip"},data= data)
print(response.text)
print(response)