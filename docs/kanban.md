# Kanban-tavla

Vi har en projektbräda på GitHub Projects, men vi håller den här filen uppdaterad också så
att man snabbt ser läget utan att logga in. Kolumnerna är samma som på brädan.

Ansvarig står inom parentes.

## Backlog

- Bonus: LCD-skärm som visar temperaturen på själva enheten (Tarik)
- Bonus: fler sensorer, till exempel en ljussensor (Alan)
- Bonus: driftsätta pipelinen i Azure (Salah)
- Bonus: skicka larm som mejl eller telegram (Henrik)
- Individuell rapport (alla fyra skriver var sin)

## To do

- Grafana-dashboard med KPI:er och livegrafer (Salah)
- Materiallista i Excel med antal prototyper (Alan)
- README med diagram och instruktioner (Alan)
- Dokument om hur vi jobbar i gruppen (Alan)
- Ta skärmbilder till README:n (Alan)
- Presentationsbilder (Tarik, Salah)

## In progress

- Consumer som sparar mätvärdena i TimescaleDB (Tarik)
- Fixa startordningen, consumern startar före databasen (Salah)
- DHT11:an svarar inte varje gång och programmet kraschar (Tarik)

## Done

- Sätta upp repo, .gitignore och kanban-tavla (Henrik)
- Simulera kretsen i Wokwi (Alan)
- Koppla DHT11 och två lysdioder på kopplingsdäcket (Henrik)
- Ladda upp umqtt-biblioteket till Pico:n (Tarik)
- Publicera mätvärden över MQTT (Henrik)
- Docker compose med mosquitto, timescaledb och grafana (Salah)
- Pico:n kom inte in i mosquitto, fixat med egen mosquitto.conf (Salah)
