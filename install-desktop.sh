#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
[[ $EUID -eq 0 ]] || { echo "Run: sudo bash install-desktop.sh"; exit 1; }
. /etc/os-release
[[ ${ID:-} == debian ]] || { echo "This installer targets Debian. Use a Debian VM first."; exit 1; }
apt-get update
apt-get install -y python3 python3-tk
install -d /opt/lantern /usr/share/applications
install -m 755 app/lantern_ai.py /opt/lantern/
install -m 644 assets/lantern.desktop /usr/share/applications/
install -m 644 assets/wallpaper.svg /opt/lantern/
echo "Installed LANTERN AI in your application menu. See README.md for Ollama setup."
