#für Erstellen eine Benutzeroberfläche
from tkinter import *
#Modul für grafische Darstellung der 7-tagigen Vorhersage
from forecastsevendays import make_graph
#Modul für Error-Nachritren bei fehlerhafter Ortnamen
from tkinter import messagebox
#Bilderdatei speichern und laden
from PIL import Image, ImageTk
#Vermeiden Sevice API-Key  direkt in Script zu legen
from configparser import ConfigParser
#CRUD(CREATE,READ;UPDATE;DELETE)-Dienste zu erledigen
import requests

#Die URL-Adresse für aktuelle Wetterdaten für  einen Standort abrufen
url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config["api_key"]["key"]
#Configdatei ist gelesen und es wurde die API-key in einem Variable geschrieben

#Variable für Kordinaten des aktuellen Standort
lon_lat = []
#Zähler für die Bennenung der ersletten Grafik-Dateien
list_count = list(range(1, 100))[::-1]

"""
Die Funktion macht eine Request-Abfrage und bekomment Daten aus dem Server. Die Daten wurden 
 in JSON format umgewandelt und in einezelne Valiable gespeichert.Als  Resultat ergibt die Funktion 
 city, country, temp_celsius, temp_fahrenheit, icon, weather, wind zurück
 """
def get_day_weather(city):
    data = requests.get(url.format(city, api_key))
    if data:
       data_json = data.json()
       print(data_json)
       lon = data_json["coord"]["lon"]
       lat = data_json["coord"]["lat"]
       lon_lat.append(lon)
       lon_lat.append(lat)
       print(lat, lon)

       #(city,country,tem_celsius,temp,fahrenheit,weather_icon,weather)
       city = data_json["name"]
       country = data_json["sys"]["country"]
       temp_kelvin = data_json["main"]["temp"]
       temp_celsius = temp_kelvin - 273.15
       temp_fahrenheit = temp_celsius * 9/5 + 32
       icon = data_json["weather"][0]["icon"]
       weather = data_json["weather"][0]["main"]
       wind = float(data_json["wind"]["speed"]) * 3.6
       result = (city, country, temp_celsius, temp_fahrenheit, icon, weather, wind)
       return result
    else:
        return None

def search():
    global city
    #die Bentzereingabe in city-Varble speichern
    city = city_text.get()
    #Standort wurde als Parameter in vorherige Funktion eingegeben und das Resultat wurde
    # in Variable weather gespeichert
    weather = get_day_weather(city)
    global img
    global my_photo
    #Die Daten werden weter verwendet,nur wenn Variable weather nicht leer ist
    if weather:
        #print(weather)
        #die Stadt und der Staat wurde in erstem Label gespeichert
        location_lbl["text"] = f"{weather[0]} {weather[1]}"
        #die grafische Dastellung vom Wettersituation wurde im Order weather_icon ausgesucht und
        # in Variable img gespeichert
        img=ImageTk.PhotoImage(Image.open(f"weather_icon/{weather[4]}.png"))
        #das Bild wurde an nächstem Label angehängt
        image_icon["image"] = img
        #Die Temperatur in Celsius und in Fahrenheit wurde in nächstem Label gespeichert
        temp_lbl["text"] = f"{weather[2]:.2f}°C, {weather[3]:.2f}°F"
        #Der Wind und die Wettersituation werden in letzten Label gespeichert
        weather_lbl["text"] = F"{weather[5]}, wind {round(weather[6],2)} km/h"
        #Das Eingabefeld wurde leer gemacht
        city_entry.delete(0, END)
        #Das Bild hinter die Wettervorhersage wurde aktualisiert
        my_photo = ImageTk.PhotoImage(Image.open("./img/5.jpg"))
        image["image"] = my_photo

    else:
        #Fals unkorrekte Orteeingabe wurde eine Fehlermeldung ausgelöst
        messagebox.showerror("Error", f"Stadtort {city} konnte nicht gefunden werden ")

#Start Benutzerobefläche
app = Tk()

"""
Die Grafik wurde durch Modul-forecastsevendays erstellt nach der Eingabe der Parameters
Die Kordinaten wurden von List lon_lan genommen
Die Stadtname ist ein globales Variable und der Number wurde  für eine unterschiedliche
Bennenung der Grafiken benutz
Die Grafik als Bild wurde am Ende der Application angehägt
"""
def get_forecast():
    global grafik
    number = list_count.pop()
    lat = lon_lat.pop()
    lon = lon_lat.pop()
    make_graph(lat, lon, city, number)
    grafik = ImageTk.PhotoImage(Image.open(f"Matplotlib{number}.png"))
    image["image"] = grafik

#Wir setzen ein Title,Anwendungsmaße und Hitergrundfarbe
app.title("Wetter-Application")
app.geometry("750x600")
app.configure(bg="skyblue")

#Eingabefeld deklarieren,initialisieren und anhängen
city_text = StringVar()
city_entry = Entry(app, textvariable=city_text, font=("Verdana", 12))
city_entry.pack(ipadx=5, ipady=5)

#Button-Suchen deklarieren,initialisieren und anhängen
search_btn = Button(app, text="Suche nach Ort", width=20, command=search, font=("Verdana", 12))
search_btn.pack()

#Button-7 Tage Vorhersage deklarieren,initialisieren und anhängen
forecast_btn = Button(app, text="7 - Tage Vorhersage", width=20, font=("Verdana", 12), command=get_forecast)
forecast_btn.pack()

#Label für Ort deklarieren,initialisieren und anhängen
location_lbl = Label(app, text="", font=("Verdana", 20), bg="skyblue")
location_lbl.pack()

#Label für Bild- Wettersituation deklarieren,initialisieren und anhängen
image_icon = Label(app, image="", bg="skyblue")
image_icon.pack()

#Label für Temperatur deklarieren,initialisieren und anhängen
temp_lbl = Label(app, text="", bg="skyblue")
temp_lbl.pack()

#Label für Wind  und schriftlische Wettersituation deklarieren,initialisieren und anhängen
weather_lbl = Label(app, text="", font=("Verdana", 10), bg="skyblue")
weather_lbl.pack()

#Label für Bild und 7 -tagigen Vorhersage deklarieren,initialisieren und anhängen
my_photo = ImageTk.PhotoImage(Image.open("./img/5.jpg"))
image = Label(app, image=my_photo)
image.pack(side="bottom", fill="both", expand="yes")

app.mainloop()
#End
