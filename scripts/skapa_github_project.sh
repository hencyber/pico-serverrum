#!/usr/bin/env bash
# Skapar issues och en kanban-tavla (GitHub Project) för projektet.
#
# Kör detta EN gång, när repot redan finns på GitHub och alla fyra är collaborators.
#
#   gh auth login
#   bash scripts/skapa_github_project.sh
#
# Kräver gh och jq.

set -e

OWNER=$(gh repo view --json owner --jq .owner.login)
REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
PROJEKT_NAMN="piCo - Serverrumsvakt"

echo "Repo: $REPO"
echo "Ägare: $OWNER"
echo

# ---------------------------------------------------------------- etiketter
echo "Skapar etiketter..."
gh label create pico --color 1D76DB --description "kod som körs på pico:n" --force
gh label create pipeline --color 0E8A16 --description "mqtt, consumer, databas" --force
gh label create grafana --color F9D0C4 --description "dashboard och visualisering" --force
gh label create dokumentation --color FBCA04 --description "readme, rapport, bom" --force
gh label create bugg --color D73A4A --description "något som inte funkar" --force
gh label create bonus --color 5319E7 --description "VG-krav" --force
echo

# -------------------------------------------------------------------- issues
# format: "status|ansvarig|etiketter|titel|beskrivning"
ISSUES=(
"Done|hencyber|dokumentation|Sätta upp repo, gitignore och kanban-tavla|Skapa repot, lägga in .gitignore så inga lösenord pushas och sätta upp projektbrädan."
"Done|alanzangana1|pico|Simulera kretsen i Wokwi|Bygga kretsen med sensor och två lysdioder i Wokwi innan vi kopplar på riktigt."
"Done|hencyber|pico|Koppla DHT11 och två lysdioder|Koppla sensorn till GP16 och lysdioderna till GP15 och GP14 med 330 ohm motstånd."
"Done|mulisictarik|pico|Ladda upp umqtt-biblioteket till Pico:n|Hämta simple.py och robust.py och lägga dem i en umqtt-mapp på Pico:n."
"Done|hencyber|pico pipeline|Publicera mätvärden över MQTT|Skicka temperatur, fuktighet och status som JSON till mosquitto var tredje sekund."
"Done|Salah-Ud-Din01|pipeline|Docker compose med mosquitto, timescaledb och grafana|Sätta upp hela pipelinen i docker så vi slipper installera saker lokalt."
"Done|Salah-Ud-Din01|pipeline bugg|Pico:n kommer inte in i mosquitto|Mosquitto släpper bara in anslutningar från samma maskin. Behöver egen mosquitto.conf."
"Done|mulisictarik|pipeline|Consumer som sparar mätvärdena i TimescaleDB|Prenumerera på topicen och skriva in varje mätvärde i en hypertable."
"Done|mulisictarik|pico bugg|DHT11:an svarar inte varje gång|Programmet kraschar när sensorn inte svarar. Behöver hantera felet och försöka igen."
"Done|Salah-Ud-Din01|pipeline bugg|Consumern startar före databasen|Consumern kraschar vid uppstart för att timescaledb inte hunnit bli klar."
"Done|Salah-Ud-Din01|pipeline bugg|Loggarna syns inte i docker logs|Python buffrar utskrifterna så vi ser ingenting när vi felsöker."
"Done|Salah-Ud-Din01|grafana|Grafana-dashboard med KPI:er och livegrafer|Dashboard med senaste temperatur, senaste fuktighet, antal larm och grafer som uppdateras live."
"Done|alanzangana1|dokumentation|Materiallista i Excel|BOM med komponent, pris, länk och motivering. Antal prototyper ska gå att ändra."
"Done|alanzangana1|dokumentation|README med diagram och instruktioner|Beskriva produkten, arkitekturen och hur man kör projektet."
"Done|alanzangana1|dokumentation|Dokument om hur vi jobbar i gruppen|Arbetssätt, branches, pull requests och kodstil som alla är överens om."
"Done|hencyber|dokumentation|Mall för den individuella rapporten|Så att vi alla får med det som krävs i rapporten."
"Done|mulisictarik|dokumentation|Checklista för GitHub och inlämning|Vad som ska vara gjort innan vi lämnar in."
"In Progress|alanzangana1|dokumentation|Ta skärmbilder till README:n|Kopplingen på kopplingsdäcket, Wokwi-simuleringen och Grafana med live-data."
"In Progress|mulisictarik|dokumentation|Presentationsbilder till slutdemon|Bilder till redovisningen. Tänk på berättandet och målgruppen."
"Todo|hencyber|dokumentation|Individuell rapport - Henrik|2-3 sidor med teknisk beskrivning och personlig reflektion."
"Todo|mulisictarik|dokumentation|Individuell rapport - Tarik|2-3 sidor med teknisk beskrivning och personlig reflektion."
"Todo|Salah-Ud-Din01|dokumentation|Individuell rapport - Salah|2-3 sidor med teknisk beskrivning och personlig reflektion."
"Todo|alanzangana1|dokumentation|Individuell rapport - Alan|2-3 sidor med teknisk beskrivning och personlig reflektion."
"Todo|hencyber|pipeline|Långtidstest av pipelinen|Låta allt rulla ett dygn och se att varken Pico:n eller consumern hänger sig."
"Todo|hencyber|dokumentation|Bjuda in läraren till vårt GitHub Project|Krav för inlämningen."
"Todo|mulisictarik|bonus|Bonus: LCD-skärm på edge-enheten|Visa temperatur och status direkt på enheten med en 16x2-display."
"Todo|alanzangana1|bonus|Bonus: fler sensorer|Lägga till en ljussensor så vi ser om någon lämnat lampan på i serverrummet."
"Todo|Salah-Ud-Din01|bonus|Bonus: driftsätta pipelinen i Azure|Flytta mosquitto, consumern och databasen till molnet."
"Todo|hencyber|bonus|Bonus: skicka larm som mejl eller telegram|Så att någon får veta om det blir för varmt även när ingen tittar på dashboarden."
)

# ------------------------------------------------------------------ projektet
echo "Skapar projektet \"$PROJEKT_NAMN\"..."
PROJEKT_NUMMER=$(gh project create --owner "$OWNER" --title "$PROJEKT_NAMN" --format json | jq -r .number)
PROJEKT_ID=$(gh project view "$PROJEKT_NUMMER" --owner "$OWNER" --format json | jq -r .id)
echo "Projekt nummer $PROJEKT_NUMMER"
echo

STATUS_FALT=$(gh project field-list "$PROJEKT_NUMMER" --owner "$OWNER" --format json \
  | jq -r '.fields[] | select(.name == "Status")')
STATUS_ID=$(echo "$STATUS_FALT" | jq -r .id)

hamta_option () {
  echo "$STATUS_FALT" | jq -r --arg namn "$1" '.options[] | select(.name == $namn) | .id'
}

echo "Skapar issues och lägger dem på tavlan..."
for rad in "${ISSUES[@]}"; do
  IFS="|" read -r status ansvarig etiketter titel beskrivning <<< "$rad"

  etikett_flaggor=()
  for etikett in $etiketter; do
    etikett_flaggor+=(--label "$etikett")
  done

  URL=$(gh issue create --title "$titel" --body "$beskrivning" \
    --assignee "$ansvarig" "${etikett_flaggor[@]}")
  echo "  $status: $titel"

  ITEM_ID=$(gh project item-add "$PROJEKT_NUMMER" --owner "$OWNER" --url "$URL" --format json | jq -r .id)

  OPTION_ID=$(hamta_option "$status")
  if [ -n "$OPTION_ID" ]; then
    gh project item-edit --project-id "$PROJEKT_ID" --id "$ITEM_ID" \
      --field-id "$STATUS_ID" --single-select-option-id "$OPTION_ID" > /dev/null
  fi

  # stäng de issues som redan är klara
  if [ "$status" = "Done" ]; then
    gh issue close "$URL" > /dev/null
  fi
done

echo
echo "Klart. Tavlan finns här:"
gh project view "$PROJEKT_NUMMER" --owner "$OWNER" --format json | jq -r .url
echo
echo "Glöm inte att bjuda in läraren till projektet under Settings -> Manage access."
