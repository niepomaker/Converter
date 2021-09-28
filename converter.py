import json, os

os.system("wget --certificate=/usr/share/n6/roman.osinski-dzp.pl.pem --private-key=/usr/share/n6/roman.osinski.n6.key https://n6beta.cert.pl/report/threats.json -P /home/lukasz/Converter/Converter")


file_json = open('threats.json')
data = json.load(file_json)
for i in data:
    print(i)


file_json.close()
