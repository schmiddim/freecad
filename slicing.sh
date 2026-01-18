#!/usr/bin/env bash
set -euo pipefail

# Ziel-Workspace (0-basiert); 1 entspricht Bildschirm/Arbeitsfläche 2
TARGET_WS="${TARGET_WS:-1}"
CAJA_CMD="${CAJA_CMD:-caja}"
BAMBU_CMD="${BAMBU_CMD:-bambu-studio}"

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Fehlender Befehl: $1" >&2
    exit 1
  fi
}

require_cmd wmctrl

start_and_move() {
  local cmd="$1"
  local match="$2"

  # Anwendung im Hintergrund starten
  setsid -- bash -lc "$cmd" >/dev/null 2>&1 &
  local pid=$!
  local win_id=""

  # Auf Fenster warten und es auf Workspace TARGET_WS verschieben
  for _ in {1..40}; do
    sleep 0.25
    win_id=$(wmctrl -lp | awk -v pid="$pid" '$3==pid {print $1; exit}')
    [ -n "$win_id" ] && break
    win_id=$(wmctrl -lx | awk -v pat="$match" '{
      tgt=tolower(pat); cls=tolower($3); line=tolower($0);
      if (index(cls, tgt) || index(line, tgt)) {print $1; exit}
    }')
    [ -n "$win_id" ] && break
  done

  if [ -n "$win_id" ]; then
    wmctrl -i -r "$win_id" -t "$TARGET_WS"
  else
    echo "Warnung: Kein Fenster für $cmd gefunden" >&2
  fi
}

start_and_move "$CAJA_CMD" "caja"
start_and_move "$BAMBU_CMD" "bambu"
