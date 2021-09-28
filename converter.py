import json, os

os.system("wget --certificate=/usr/share/n6/roman.osinski-dzp.pl.pem --private-key=/usr/share/n6/roman.osinski.n6.key https://n6beta.cert.pl/report/threats.json -P /home/lukasz/Converter/Converter")

def saveToFile(i):
    file_txt = open(i['category']  + '.txt', "a")
    counter = 0
    if ('address' in i):
        while (counter < len(i['address'])):
            print(i['address'][counter]["ip"])
            file_txt.write(i['address'][counter]["ip"] + '\n')
            counter = counter + 1

file_json = open('threats.json')
data = json.load(file_json)
for i in data:
    saveToFile(i)
    print(i)


file_json.close()
