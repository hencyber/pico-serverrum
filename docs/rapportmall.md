# Mall för den individuella rapporten

Rapporten är **individuell** - alla fyra skriver var sin och lämnar in som PDF. Totalt 2-3
sidor. Den här mallen är bara ett stöd så att vi inte missar något av kraven, skriv med egna
ord.

---

## Rubrik: [Produktens namn] - individuell rapport

**Namn, klass, datum**

### 1. Produkten och problemet (ca 1/2 sida)

- Vad är det vi har byggt?
- Vilket problem löser den och för vem?
- Varför är det ett problem värt att lösa?

### 2. Teknisk lösning (ca 1 sida)

- Hårdvaran: Pico 2 W, DHT11, lysdioder, motstånd. Varför just de komponenterna?
- Hur mätvärdena tas fram och vad gränsvärdena är.
- Pipelinen: Pico → Mosquitto → consumer → TimescaleDB → Grafana. Förklara varför vi går via
  MQTT istället för att skicka direkt till databasen.
- Varför TimescaleDB och inte vanlig Postgres?
- Ta med en bild på kopplingen, en på Grafana-dashboarden och gärna arkitekturskissen.

### 3. Problem vi stötte på (ca 1/2 sida)

Välj två eller tre och beskriv vad som hände och hur ni löste det. Exempel från vårt projekt:

- DHT11:an svarar inte varje gång (löstes med try/except)
- Mosquitto släppte inte in Pico:n (egen mosquitto.conf)
- consumern startade före databasen (sleep + restart: on-failure)

### 4. Individuell reflektion (1/2 - 1 sida)

- Vad har **jag** bidragit med? Var konkret: vilka issues, vilka filer, vilka PR:ar.
- Vad har de andra tre bidragit med?
- Vad fungerade bra i gruppen och vad hade vi kunnat göra bättre?
- Vad tar jag med mig till nästa projekt?

---

**Checklista innan inlämning**

- [ ] 2-3 sidor totalt
- [ ] Bilder och skärmbilder med
- [ ] Reflektionen är personlig och nämner alla i gruppen
- [ ] Exporterad som PDF
