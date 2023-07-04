import datetime
import json, os
import psycopg2
from datetime import date
import datetime
from datetime import datetime as xd

os.system("wget ... -P /home/lukasz/Converter/Converter")

connection = psycopg2.connect(user="postgres", password="JeBJh4tELW9nq4Ohk9VA", host="localhost",
                              port="5432", database="roman")
cursor = connection.cursor()

def saveToFile(i):
    file_txt = open(i['category']  + '.txt', "a")
    counter = 0
    if ('address' in i):
        while (counter < len(i['address'])):
            print(i['address'][counter]["ip"])
            file_txt.write(i['address'][counter]["ip"] + '\n')
            counter = counter + 1


def writeToBase(id, category, confidance, name, url, time, source, cc, ip, asn, fqdn, block, sha256, dport, target):

    postgres_insert_query = """ INSERT INTO json (id, category, confidence, name, url, time, source, cc, ip, asn, fqdn, block, sha256, dport, target) 
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (
    id, category, confidance, name, url, time, source, cc, ip, asn, fqdn, block, sha256, dport, target)
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()

def readIdFromBase():
    allId = []
    postgres_insert_query = """SELECT id FROM json"""
    cursor.execute(postgres_insert_query)
    data = cursor.fetchall()
    for row in data:
        allId.append(row[0])
    return allId

def saveToFile(i):
    file_txt = open(i['category'] + '.txt', "a")
    counter = 0
    if ('address' in i):
        while (counter < len(i['address'])):
            file_txt.write(i['address'][counter]["ip"] + '\n')
            counter = counter + 1


def saveToBaseWithAddress(i, keys, counter):
    for key in keys:
        if key in i.keys():
            keys[key] = i[key]

    for j in i['address'][counter]:
        keys[j] = i['address'][counter][j]

    if (counter == 0):
        writeToBase(keys["id"], keys["category"], keys["confidence"], keys["name"], keys["url"], keys["time"], keys["source"],
             keys["cc"], keys["ip"], keys["asn"], keys['fqdn'], keys['block'],
             keys['sha256'], keys['dport'], keys['target'])
    else:
        writeToBase(keys["id"] + "/" + str(counter), keys["category"], keys["confidence"], keys["name"], keys["url"],
             keys["time"], keys["source"], keys["cc"], keys["ip"], keys["asn"], keys['fqdn'], keys['block'],
             keys['sha256'], keys['dport'], keys['target'])


def saveToBaseWithoutAddress(i, keys):
    for key in keys:
        if key in i.keys():
            keys[key] = i[key]

    writeToBase(keys["id"], keys["category"], keys["confidence"], keys["name"], keys["url"], keys["time"], keys["source"],
         keys["cc"], keys["ip"], keys["asn"], keys['fqdn'], keys['block'],
         keys['sha256'], keys['dport'], keys['target'])

def newEmptyDictionary(data):
    dict = {}
    for i in data:
        for key in i.keys():
            if key not in dict:
                dict[key] = "null"

    del dict['address']
    dict['cc'] = "null"
    dict['ip'] = "null"
    dict['asn'] = "null"
    return dict

file_json = open('threats.json')
data = json.load(file_json)

print("JSON został dodany do bazy danych oraz zostały utworzone pliki .txt")

counter = 0
counter1 = 0

def takeAllRecords():
    postgres_insert_query = """SELECT * FROM json"""
    cursor.execute(postgres_insert_query)
    data = cursor.fetchall()
    return data

for i in data:
    counter1 += 1
    date0 = i['time'].replace("T", " ").split(" ")[0]
    date1 = xd.strptime(date0, '%Y-%m-%d')

    today = date.today() - datetime.timedelta(days=1)
    today1 = today.strftime("%Y-%m-%d")

    currentDay = xd.strptime(date0, '%Y-%m-%d')
    weekAgo = xd.strptime(today1, '%Y-%m-%d')
    if currentDay >= weekAgo:
        counter += 1

print(counter)
print(counter1)
file_json.close()
os.remove("/home/lukasz/Converter/Converter/threats.json")
if connection:
    cursor.close()
    connection.close()
