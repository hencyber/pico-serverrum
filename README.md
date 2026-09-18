# piCo - Serverrumsvakt 🌡️

Ett projekt i kursen Edge computing. Vi har byggt ett proof of concept åt πCo: en liten
edge-enhet som övervakar klimatet i ett serverrum och larmar när det blir för varmt eller
för fuktigt.

Gruppmedlemmar: Henrik ([@hencyber](https://github.com/hencyber)), Tarik
([@mulisictarik](https://github.com/mulisictarik)), Salah
([@Salah-Ud-Din01](https://github.com/Salah-Ud-Din01)) och Alan
([@alanzangana1](https://github.com/alanzangana1)).

## Problemet vi löser

I ett serverrum eller ett elskåp får det inte bli för varmt, för då börjar servrarna strypa
prestandan och i värsta fall stängs de av. Blir luftfuktigheten för hög riskerar man istället
kondens och korrosion på elektroniken. Många mindre företag har ingen övervakning alls i sina
serverrum utan märker problemet först när något har gått sönder.

Vår produkt är en billig sensor-enhet (under 300 kr per styck) som mäter temperatur och
luftfuktighet var tredje sekund, visar status direkt på plats med en grön och en röd lysdiod,
och skickar all data vidare till en dashboard där man kan se historiken och upptäcka trender
innan det blir ett problem.

## Hårdvara

| Komponent | Ansluten till |
| --------- | ------------- |
| DHT11 (KY-015) data | GP16 |
| DHT11 VCC | 3V3 |
| DHT11 GND | GND |
| Grön lysdiod (OK) | GP15 via 330Ω motstånd |
| Röd lysdiod (LARM) | GP14 via 330Ω motstånd |

Hela materiallistan med priser och motiveringar finns i [BOM_pico_serverrum.xlsx](BOM_pico_serverrum.xlsx).
I den filen kan man ändra antalet prototyper i cell B2 så räknas antal komponenter och
kostnader om automatiskt.

![kopplingen på kopplingsdäcket](bilder/kopplingsschema.jpg)

På bilden lyser statuslysdioden grönt, alltså är klimatet inom gränsvärdena.

## Arkitektur

```mermaid
flowchart LR
    A[DHT11-sensor] --> B[Raspberry Pi Pico 2 W<br/>MicroPython]
    B --> C[Lysdioder<br/>grön = OK, röd = LARM]
    B -->|MQTT över WiFi| D[Mosquitto<br/>broker]
    D -->|prenumererar| E[Consumer<br/>Python + paho-mqtt]
    E --> F[(TimescaleDB)]
    F --> G[Grafana<br/>live dashboard]
```

Allt utom Pico:n körs i Docker-containrar på en laptop.

## Flödesschema för koden på Pico:n

```mermaid
flowchart TD
    Start([Start]) --> Wifi[Anslut till WiFi]
    Wifi --> Wifi_ok{Ansluten?}
    Wifi_ok -->|Nej| Blink[Blinka röd lysdiod och avbryt]
    Wifi_ok -->|Ja| Mqtt[Anslut till Mosquitto]
    Mqtt --> Read[Läs temperatur och fuktighet]
    Read --> Error{Gick läsningen bra?}
    Error -->|Nej| Wait[Vänta 3 sekunder]
    Wait --> Read
    Error -->|Ja| Check{Över gränsvärde?}
    Check -->|Ja| Red[status = ALARM, röd lysdiod]
    Check -->|Nej| Green[status = OK, grön lysdiod]
    Red --> Publish[Publicera JSON till MQTT]
    Green --> Publish
    Publish --> Sleep[Vänta 3 sekunder]
    Sleep --> Read
```

Meddelandet som skickas ser ut så här:

```json
{"device_id": "pico-serverroom-01", "temperature": 24, "humidity": 41, "status": "OK"}
```

## Mappstruktur

```
pico-serverrum/
├── src_pico/            # koden som ligger på Pico:n
│   ├── main.py
│   ├── wifi.py
│   └── umqtt/
├── src_pipeline/        # allt som körs i docker
│   ├── consumer.py
│   ├── docker-compose.yaml
│   ├── grafana/
│   └── utils/
├── wokwi/               # simuleringen
├── docs/                # arbetssätt och rapportmall
└── BOM_pico_serverrum.xlsx
```

## Simulering i Wokwi

Innan vi kopplade upp något på riktigt byggde vi kretsen i
[Wokwi](https://wokwi.com/). Filerna finns i [wokwi/](wokwi/) - skapa ett nytt
MicroPython-projekt för Pico, klistra in `diagram.json` och `main.py` så går det att köra.

I Wokwi finns ingen DHT11 och ingen Mosquitto-broker, så simuleringen använder en DHT22 och
skriver ut mätvärdena i REPL istället för att publicera dem. Logiken för gränsvärden och
lysdioder är exakt densamma som på riktig hårdvara.

![wokwi](bilder/wokwi.png)

## Så kör man projektet

### 1. Pico:n

1. Installera MicroPython på Pico 2 W enligt kursens setup-guide.
2. Kopiera `src_pico/wifi_credentials.example.json` till `wifi_credentials.json` och fyll i
   ert WiFi. Filen är med i `.gitignore` så lösenordet hamnar aldrig på GitHub.
3. Ändra `MQTT_BROKER` i `src_pico/main.py` till IP-adressen för datorn som kör Docker.
4. Ladda upp hela `src_pico/`-mappen till Pico:n med MicroPico i VS Code.

### 2. Pipelinen

```bash
cd src_pipeline
cp .env.example .env     # fyll i egna lösenord
docker compose up -d --build
```

Då startar fyra containrar: `mosquitto`, `consumer`, `timescaledb` och `grafana`.

### 3. Grafana

Gå till <http://localhost:3000> och logga in med användarnamnet och lösenordet från `.env`.
Datakällan och dashboarden läggs in automatiskt, så dashboarden **piCo -
Serverrumsövervakning** ska redan finnas där. Den uppdaterar sig själv var femte sekund.

![grafana-dashboarden](bilder/grafana.png)

Dashboarden innehåller:

- senaste temperatur och senaste luftfuktighet som KPI:er med färg när gränsvärdet passeras
- antal larm senaste timmen
- antal mätvärden senaste minuten, så man ser att enheten lever
- grafer över temperatur och luftfuktighet som uppdateras live
- en tabell med de tio senaste mätvärdena

## Problem vi stötte på

- DHT11:an svarar inte varje gång man frågar den. Vi fick lägga läsningen i en `try/except`
  och hoppa över den mätningen istället för att hela programmet kraschade.
- Mosquitto i Docker släpper som standard bara in anslutningar från samma maskin. Vi la till
  en egen `mosquitto.conf` med `listener 1883` och `allow_anonymous true` för att Pico:n
  skulle komma in.
- Consumern startade snabbare än databasen första gången och kraschade. Vi löste det med en
  `time.sleep(5)` i början och `restart: on-failure` i docker compose.
- DHT11:an ger bara heltal, så temperaturen hoppar med ett helt grader i taget i grafen.

## Arbetssätt

Vi har jobbat med GitHub Projects, issues och branches. Vårt gemensamma arbetssätt finns
beskrivet i [docs/arbetssatt.md](docs/arbetssatt.md) och läget på uppgifterna i
[docs/kanban.md](docs/kanban.md).
