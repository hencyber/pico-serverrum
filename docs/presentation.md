# Upplägg för slutdemon

Ett stöd för hur vi lägger upp redovisningen. Innehållet i varje punkt är sånt vi ska
**berätta**, inte läsa innantill. Räkna med ungefär 10 minuter plus frågor.

Alla fyra ska prata. Förslag på fördelning står vid varje avsnitt, byt om ni hellre vill.

---

## Bild 1 - Titel (Henrik, 30 sek)

- piCo Serverrumsvakt
- Våra namn och att vi är utvecklingsteamet på πCo
- En mening om vad produkten gör

## Bild 2 - Problemet (Salah, 1,5 min)

Börja med problemet, inte med tekniken. Berätta som en historia:

- Ett litet företag har sina servrar i ett städskåp eller ett litet rum
- Blir det för varmt stryper servrarna prestandan, i värsta fall stängs de av
- Blir luftfuktigheten för hög riskerar man kondens och korrosion
- De flesta har ingen övervakning alls, utan märker det först när något gått sönder
- Vår produkt kostar under 300 kr per enhet

Ta gärna med en siffra eller ett exempel som gör det konkret.

## Bild 3 - Vad vi byggde (Alan, 1 min)

- Bild på den färdiga enheten
- Pico 2 W med en DHT11-sensor och en statuslysdiod
- Mäter var tredje sekund, lysdioden lyser när allt är OK och blinkar vid larm
- Larmgränser: 27 °C och 60 % luftfuktighet, och varför vi valde just dem

## Bild 4 - Arkitektur (Tarik, 2 min)

Visa arkitekturskissen från README:n och gå igenom pilarna en i taget:

- Pico:n mäter och publicerar JSON över MQTT
- Mosquitto är brokern som tar emot
- Consumern prenumererar och skriver till TimescaleDB
- Grafana läser från databasen och ritar upp det live
- Allt utom Pico:n körs i Docker

Den fråga som brukar komma: **varför inte skicka direkt från Pico:n till databasen?**
Ha svaret klart: MQTT gör att Pico:n inte behöver veta något om databasen, flera enheter
och flera konsumenter kan kopplas på utan att vi ändrar koden på enheterna, och meddelanden
går inte förlorade om consumern startar om.

## Bild 5 - Demo (Henrik och Salah, 3 min)

Det här är det viktigaste. Öva på det innan.

1. Visa enheten med lysdioden lysande och Grafana bredvid som uppdaterar sig
2. Värm sensorn med handen eller andas på den
3. Visa hur temperaturen stiger i grafen, hur KPI:n blir röd och lysdioden börjar blinka
4. Visa tabellen med de senaste mätvärdena

> Ha en plan B: om wifi eller hårdvaran krånglar, kör
> `uv run --with paho-mqtt scripts/testdata.py` så fylls dashboarden med testdata.
> Säg i så fall rakt ut att det är simulerad data.

## Bild 6 - Kort om koden (Tarik, 1,5 min)

Visa två saker, inte mer:

- Loopen i `src_pico/main.py`: mät, sätt status, publicera, visa status med lysdioden
- `on_message` i `consumer.py`: ta emot, packa upp JSON, skriv till databasen

Gå inte in i detaljer. Det räcker att visa att det är enkelt och läsbart.

## Bild 7 - Problem vi löste (Alan, 1,5 min)

Välj två, berätta vad som hände och hur vi kom på lösningen:

- DHT11:an svarade inte varje gång och programmet kraschade
- Mosquitto släppte inte in Pico:n, den lyssnade bara lokalt
- Consumern startade före databasen
- Loggarna syntes inte i docker logs så vi felsökte blint

Det här avsnittet är ofta det som ger mest respekt, för det visar att vi förstår systemet.

## Bild 8 - Kostnad och arbetssätt (Salah, 1 min)

- Materiallistan: kostnad per enhet och vad tio enheter skulle kosta
- Hur vi jobbade: issues, branches, pull requests, kanban-tavlan
- Visa gärna brädan eller ett skärmklipp på den

## Bild 9 - Nästa steg (Henrik, 30 sek)

- LCD-skärm på enheten
- Fler sensorer
- Driftsätta pipelinen i Azure
- Larm via mejl eller telegram

Avsluta med en mening om vad produkten skulle kunna bli om πCo tog den vidare.

---

## Checklista innan demon

- [ ] Allt testat på plats, inte bara hemma
- [ ] Docker igång innan vi börjar prata
- [ ] Grafana redan uppe i en flik
- [ ] Testdata-skriptet redo som plan B
- [ ] Vi har kört igenom hela presentationen minst en gång tillsammans
- [ ] Alla vet vilka bilder just de ska prata om
