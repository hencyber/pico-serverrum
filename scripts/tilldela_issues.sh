#!/usr/bin/env bash
# Tilldelar issues till rätt person.
#
# GitHub låter en inte tilldela en issue till någon som inte tackat ja till
# inbjudan till repot än. Kör därför det här skriptet när alla fyra har
# accepterat inbjudan, så läser det "Ansvarig: @namn" ur varje issue och
# tilldelar den.
#
#   bash scripts/tilldela_issues.sh

set -e

echo "Tilldelar issues..."

for nummer in $(gh issue list --state all --limit 100 --json number --jq '.[].number'); do
  ansvarig=$(gh issue view "$nummer" --json body --jq .body | grep -oP '(?<=Ansvarig: @)\S+' || true)

  if [ -z "$ansvarig" ]; then
    continue
  fi

  redan=$(gh issue view "$nummer" --json assignees --jq '.assignees | length')
  if [ "$redan" -gt 0 ]; then
    echo "  #$nummer har redan en ansvarig"
    continue
  fi

  if gh issue edit "$nummer" --add-assignee "$ansvarig" > /dev/null 2>&1; then
    echo "  #$nummer -> $ansvarig"
  else
    echo "  #$nummer kunde inte tilldelas $ansvarig (har hen tackat ja till inbjudan?)"
  fi
done

echo "Klart."
