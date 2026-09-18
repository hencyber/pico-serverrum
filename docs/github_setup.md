# Checklista för GitHub

Så här satte vi upp projektet på GitHub, och vad som är kvar att göra inför inlämningen.

## 1. Skapa repot

En av oss skapar ett **publikt** repo på GitHub och lägger till de andra tre som
collaborators (Settings → Collaborators).

```bash
git remote add origin https://github.com/<användarnamn>/pico-serverrum.git
git push -u origin main
```

> Alla fyra måste ha sin egen e-post inställd innan de commitar, annars hamnar commits på fel
> person:
>
> ```bash
> git config user.name "Ditt namn"
> git config user.email "din-github-epost@example.com"
> ```

## 2. GitHub Projects

- Gå till repot → fliken **Projects** → **New project** → mallen **Board**.
- Skapa kolumnerna `Backlog`, `To do`, `In progress`, `Done`.
- Bjud in läraren till projektet (Settings → Manage access).

## 3. Issues

Lägg upp en issue per sak som ska göras och koppla den till projektbrädan. Exempel:

- `Simulera kretsen i Wokwi`
- `Läs DHT11 och tänd rätt lysdiod`
- `Publicera mätvärden över MQTT`
- `Consumer som sparar i TimescaleDB`
- `Grafana-dashboard med KPI:er`
- `Materiallista i Excel`
- `Skriv README med skärmbilder`

## 4. Branch och pull request

Alla fyra måste ha **minst en egen pull request** för att bli godkända.

```bash
git checkout main
git pull
git checkout -b feature/det-jag-gor
# koda
git add .
git commit -m "kort beskrivning"
git push -u origin feature/det-jag-gor
```

Öppna pull requesten på GitHub, skriv `Closes #3` i beskrivningen, be någon annan i gruppen
granska och merga den sedan.

## 5. Kvar innan inlämning

- [ ] Ta skärmbilder och lägg i `bilder/` (kopplingen, Wokwi, Grafana med live-data)
- [ ] Byt `MQTT_BROKER` i `src_pico/main.py` till rätt IP på den dator som kör Docker.
      IP:n får du fram med `hostname -I` på Linux, `ipconfig` på Windows eller
      `ipconfig getifaddr en0` på Mac. Pico:n och datorn måste sitta på samma wifi.
- [ ] Testa pipelinen utan hårdvara med `uv run --with paho-mqtt scripts/testdata.py`
      om ni vill se att Grafana fungerar innan Pico:n är inkopplad
- [ ] Skapa `src_pipeline/.env` från `.env.example` med egna lösenord
- [ ] Skapa `src_pico/wifi_credentials.json` från exempelfilen
- [ ] Alla fyra skriver sin individuella rapport och exporterar som PDF
- [ ] Presentationsbilder
- [ ] Lämna in länk till repot och bjud in läraren till GitHub Project
