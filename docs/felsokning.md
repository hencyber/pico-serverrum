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
