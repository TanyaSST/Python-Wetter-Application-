#Bibliiotek für Visualisierung
import matplotlib.pyplot as plt
#JSON -Datei lesen ,schreiben usw
import json
#Vermeiden Sevice API-Key  direkt in Script zu legen
from configparser import ConfigParser
#Modul füe manipulation von Datum und Uhzeit
import datetime
#CRUD(CREATE,READ;UPDATE;DELETE)-Dienste zu erledigen
import requests
#Bibliiotek für Visualisierung
import matplotlib

#Die Schriftgröße in der bestimmen
SMALL_SIZE = 7
matplotlib.rc('font', size=SMALL_SIZE)

def make_graph(lon,lat,city,count):
    url="https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,hourly&appid={}"
    config_file = "config.ini"
    config = ConfigParser()
    config.read(config_file)
    api_key = config["api_key"]["key"]
    #Configdatei ist gelesen und es wurde die API-key in einem Variable geschrieben
    #Aktuelle Wetterdaten für 7 Tage in einem Standort abrufen
    long_data=requests.get(url.format(lat,lon,api_key))
    #Die Daten in JSON umwandeln
    long_json=long_data.json()
    #3 Liste für das Datum, die niedrigste Temperatur und hoheste Temperatur erstellen
    data_list = []
    min_temp = []
    max_temp = []
    for i in range(0, 8):
        #Das Datum als timestemp in Variable speichern
        int_date = long_json["daily"][i]["dt"]
        #als Datum darstellen und im Datumliste einfügen
        date = datetime.datetime.fromtimestamp(int_date).date()
        data_list.append(date)

        #die niedrigste Temperatur in der liste speichern
        min_day_temp=float(long_json["daily"][i]["temp"]["min"]) - 273.15
        min_temp.append(min_day_temp)

        #die höchste Temperatur in der Liste speichern
        max_day_temp = float(long_json["daily"][i]["temp"]["max"]) - 273.15
        max_temp.append(max_day_temp)

    #Die Maßen der Figure eingeben
    plt.figure(figsize=(7, 4))

    #Wir setzen ein Title mit einer Parameter-Stadtname
    plt.title(f"Die Wettervorhersage in {city} für 7 Tage")
    #Die Daten aus data_list, min_temp,max_temp grafisch darstellen
    plt.bar(data_list,max_temp,color="red",label="Die höchste Temperatur in C°")
    plt.bar(data_list,min_temp, color="blue",label="Die niedrigste Temperatur in C°")
    plt.xlabel("Datum")
    plt.ylabel("Die Temperatur in Celsius")
    plt.legend()

    # als Bild speichern
    plt.savefig(f"Matplotlib{count}.png")

#make_graph(lat,lon)
make_graph(48.2085,16.3721,"Vienna",3)
#make_graph(43.2167,27.9167,"Varna",1)
#make_graph(48.1374,11.5755,"Munich",2)
#make_graph(51.5167,7.45,"Dortmund",4)



