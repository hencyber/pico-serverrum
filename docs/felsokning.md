# Felsökningsguide

Under projektet stötte vi på flera problem med Pico 2 W, WiFi, DHT11, MQTT, databasen och Grafana. Här beskriver vi problemen och hur de löstes.

## 1. Pico:n ansluter inte till WiFi vid kallstart

### Symptom

Pico:n kunde ibland inte ansluta till WiFi direkt när den startades.

### Orsak

WiFi-anslutningen hann inte alltid bli klar innan programmet fortsatte.

### Lösning

Vi ändrade WiFi-logiken så att Pico:n försöker ansluta flera gånger och väntar på anslutningen innan resten av programmet startar.

---

## 2. Pico 2 W klarar bara 2,4 GHz WiFi

### Symptom

Pico:n kunde inte ansluta till nätverket trots att datorn var ansluten till WiFi.

### Orsak

Pico 2 W använder 2,4 GHz WiFi, medan datorn kunde vara ansluten till 5 GHz. Routern kunde dessutom använda samma nätverksnamn för båda banden.

### Lösning

Vi anslöt Pico:n till ett 2,4 GHz-nätverk. Vid testning kunde även en mobil hotspot användas. Vi kontrollerade också att SSID och lösenord var rätt.

---

## 3. DHT11 ger OSError

### Symptom

DHT11 kunde ibland ge ett OSError när programmet försökte läsa temperatur och luftfuktighet.

### Orsak

Sensorn svarar inte alltid korrekt på varje mätförfrågan.

### Lösning

Vi använde try/except runt sensorläsningen så att programmet inte kraschar om en mätning misslyckas. Programmet försöker istället läsa sensorn igen.

Exempel:

```python
try:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
except OSError:
    print("Could not read the sensor, trying again")
```

---

## 4. Pico:n släpps inte in i Mosquitto

### Symptom

Brokern startade utan fel, men Pico:n kom aldrig fram. Inga anslutningar syntes i loggen.

### Orsak

Eclipse-mosquitto släpper som standard bara in klienter från samma maskin. Det syns inte
förrän någon försöker ansluta utifrån.

### Lösning

Vi la till en egen `mosquitto.conf` som monteras in i containern:

```
listener 1883
allow_anonymous true
```

---

## 5. Consumern slutar ta emot efter en återanslutning

### Symptom

Det här var den luriga. Pipelinen tystnade över natten utan att något såg trasigt ut. Alla
containrar körde, Pico:n skrev `sent: ... to mosquitto` och mosquitto loggade anslutningar,
men ingenting hamnade i databasen.

### Orsak

Vi anropade `client.subscribe()` en gång innan `loop_forever()`. När paho tappar kontakten
och återansluter återställs inte prenumerationen. Consumern var alltså uppkopplad men
lyssnade på ingenting, och det syns ingenstans i loggen.

### Lösning

Prenumerera i en `on_connect`-callback istället, så att det sker vid varje anslutning:

```python
def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)
```

### Så upptäcker man det

Panelen **Mätvärden senaste minuten** i Grafana blir röd och visar noll, medan de andra
panelerna fortfarande visar gamla värden som ser helt normala ut.

---

## 6. Grafana visar No data trots att databasen är full

### Symptom

Databasen hade tusentals rader och API:et svarade korrekt på testfrågor, men varje panel i
webbläsaren var tom.

### Orsak

Databasnamnet låg i fältet `database` medan Grafana läser det från `jsonData`. Serversidan
byggde sin egen anslutningssträng och fungerade, så felet fanns bara i webbläsarens
datakälla. Panelerna skickade aldrig några frågor alls.

### Lösning

Flytta databasnamnet till `jsonData` i provisioning-filen:

```yaml
jsonData:
  database: $POSTGRES_DB
```

### Lärdom

Ett API-test som går förbi frontend bevisar inte att gränssnittet fungerar. Vi trodde länge
att systemet var friskt eftersom våra kontroller aldrig gick samma väg som webbläsaren.
