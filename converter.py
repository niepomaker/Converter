import json, os
import psycopg2

os.system("wget --certificate=/usr/share/n6/roman.osinski-dzp.pl.pem --private-key=/usr/share/n6/roman.osinski.n6.key https://n6beta.cert.pl/report/threats.json -P /home/lukasz/Converter/Converter")

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

def base(id, category, confidance, name, url, time, source, cc, ip, asn, fqdn, block, sha256, dport, target):

    postgres_insert_query = """ INSERT INTO json (id, category, confidence, name, url, time, source, cc, ip, asn, fqdn, block, sha256, dport, target) 
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (
    id, category, confidance, name, url, time, source, cc, ip, asn, fqdn, block, sha256, dport, target)
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()


def saveToFile(i):
    file_txt = open(i['category'] + '.txt', "a")
    counter = 0
    if ('address' in i):
        while (counter < len(i['address'])):
            print(i['address'][counter]["ip"])
            file_txt.write(i['address'][counter]["ip"] + '\n')
            counter = counter + 1


def saveToBaseWithAddress(i, keys, counter):
    for key in keys:
        if key in i.keys():
            keys[key] = i[key]

    for j in i['address'][counter]:
        keys[j] = i['address'][counter][j]

    if (counter == 0):
        base(keys["id"], keys["category"], keys["confidence"], keys["name"], keys["url"], keys["time"], keys["source"],
             keys["cc"], keys["ip"], keys["asn"], keys['fqdn'], keys['block'],
             keys['sha256'], keys['dport'], keys['target'])
    else:
        base(keys["id"] + "/" + str(counter), keys["category"], keys["confidence"], keys["name"], keys["url"],
             keys["time"], keys["source"],
             keys["cc"], keys["ip"], keys["asn"], keys['fqdn'], keys['block'],
             keys['sha256'], keys['dport'], keys['target'])


def saveToBaseWithoutAddress(i, keys):
    for key in keys:
        if key in i.keys():
            keys[key] = i[key]

    base(keys["id"], keys["category"], keys["confidence"], keys["name"], keys["url"], keys["time"], keys["source"],
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

for i in data:
    saveToFile(i)
    counter = 0
    if 'address' in i:
        while(len(i['address']) > counter):
            saveToBaseWithAddress(i, newEmptyDictionary(data), counter)
            counter += 1
    else:
        saveToBaseWithoutAddress(i, newEmptyDictionary(data))


file_json.close()
if connection:
    cursor.close()
    connection.close()
