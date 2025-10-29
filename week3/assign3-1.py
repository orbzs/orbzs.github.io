# Task1-1
import urllib.request as request
import json

srcCH="https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
with request.urlopen(srcCH) as responseCH:
    dataCH=json.load(responseCH)
chList=dataCH["list"]

srcEN="https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
with request.urlopen(srcEN) as responseEN:
    dataEN=json.load(responseEN)
enList=dataEN["list"]

import csv
with open("hotels.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    enDict = { item["_id"]: item for item in enList }
    for CH in chList:
        EN = enDict.get(CH["_id"])
        if EN:
            writer.writerow([CH["旅宿名稱"], EN["hotel name"], CH["地址"], EN["address"], CH["電話或手機號碼"], CH["房間數"]])


# Task1-2
result={}
districts=[]
import re

for CH in chList:
    pattern="..區"
    hotelAdd=CH["地址"]
    if re.search(pattern,hotelAdd):
        districts.append(re.search(pattern,hotelAdd).group(0))

distS=list(dict.fromkeys(districts))
from collections import defaultdict
result = defaultdict(lambda: {"hotels": 0, "rooms": 0})
for CH in chList:
    for dist in distS:        
        if dist in CH["地址"]:            
            result[dist]["hotels"]+=1
            result[dist]["rooms"]+=int(CH["房間數"])
result = dict(result)

with open("districts.csv", "w", encoding="utf-8", newline="") as file:
     writer = csv.writer(file)
     for distName in result:
        writer.writerow([distName,result[distName]["hotels"], result[distName]["rooms"]]) 