#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root_dir"

regen_one() {
  local ui_path="$1"
  local out_path="$2"

  if [[ ! -f "$out_path" || "$ui_path" -nt "$out_path" ]]; then
    pyside6-uic "$ui_path" -o "$out_path"
    echo "Regenerated: $out_path"
  else
    echo "Up-to-date: $out_path"
  fi
}

regen_one ui/main_win.ui ui/generated/label.py
regen_one ui/dialog_run.ui ui/generated/dialog_run.py
