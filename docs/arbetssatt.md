# Vårt arbetssätt

Det här dokumentet är vi alla fyra överens om. Vi skrev det första veckan och har hållit oss
till det under hela projektet.

## Gruppen

| Namn | GitHub | Huvudansvar |
| ---- | ------ | ----------- |
| Henrik | [@hencyber](https://github.com/hencyber) | Pico-koden och sensorn |
| Tarik | [@mulisictarik](https://github.com/mulisictarik) | MQTT och consumern |
| Salah | [@Salah-Ud-Din01](https://github.com/Salah-Ud-Din01) | Docker, TimescaleDB och Grafana |
| Alan | [@alanzangana1](https://github.com/alanzangana1) | Wokwi-simulering, BOM och dokumentation |

Vi har huvudansvar men jobbar inte ensamma - alla har varit inne och hjälpt till i varandras
delar, och vi har parprogrammerat när något har krånglat.

## Agilt arbetssätt

- Vi kör i sprintar på en vecka.
- Vi har en kort standup varje gång vi ses i skolan: vad gjorde jag sist, vad gör jag nu, är
  jag fast på något?
- I slutet av varje sprint går vi igenom vad som blev klart och flyttar över det som inte
  hann bli klart till nästa sprint.

## GitHub Projects

Vi använder en projektbräda med fyra kolumner:

`Backlog` → `To do` → `In progress` → `Done`

Regler vi kommit överens om:

- Allt arbete börjar med en issue. Finns det ingen issue så finns det inget arbete.
- Man tilldelar sig själv issuen och flyttar den till `In progress` innan man börjar koda.
- Max två issues i `In progress` per person, annars blir ingenting klart.

## Branches och pull requests

- `main` är alltid körbar. Vi pushar aldrig direkt till `main`.
- En branch per issue, döpt efter vad den gör, till exempel `feature/mqtt-publish` eller
  `fix/dht11-timeout`.
- När man är klar öppnar man en pull request som kopplas till issuen med `Closes #12`.
- **Minst en annan i gruppen ska godkänna** innan man mergar. Den som granskar kör koden
  lokalt om det går.
- Vi mergar med squash så historiken i `main` blir lätt att läsa.

## Commit-meddelanden

Korta meddelanden i presens som börjar med vad det handlar om:

```
add dht11 reading to main.py
fix crash when sensor does not answer
update readme with grafana screenshot
```

## Kodstil

- Vi följer den stil vi lärt oss i kursen och håller koden enkel och läsbar.
- Tydliga variabelnamn på engelska i koden, kommentarer och dokumentation på svenska eller
  engelska - men samma inom en fil.
- DRY: upprepar vi oss tre gånger så bryter vi ut det till en funktion.
- Inga lösenord eller WiFi-uppgifter i repot. De ligger i `.env` och
  `wifi_credentials.json` som båda är i `.gitignore`.

## Om vi blir oense

Vi provar båda lösningarna om det går snabbt, annars röstar vi. Blir det lika röster frågar
vi läraren. Ingen sitter fast mer än en halvtimme på samma problem utan att fråga gruppen.
