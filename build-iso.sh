#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
[[ $EUID -eq 0 ]] || { echo "Run: sudo bash build-iso.sh"; exit 1; }
. /etc/os-release
[[ ${ID:-} == debian && ${VERSION_ID:-} == 13 ]] || { echo "Build on Debian 13 amd64, preferably in a fresh VM."; exit 1; }
[[ $(dpkg --print-architecture) == amd64 ]] || { echo "An amd64 Debian builder is required."; exit 1; }
[[ ! -e build ]] || { echo "build/ already exists. Use a new extracted copy for a clean build."; exit 1; }
apt-get update
apt-get install -y live-build debootstrap xorriso squashfs-tools
mkdir build
cd build
lb config --mode debian --distribution trixie --architectures amd64 \
  --binary-images iso-hybrid --bootloaders "syslinux grub-efi" \
  --debian-installer live --debian-installer-distribution trixie \
  --archive-areas "main contrib non-free non-free-firmware" \
  --bootappend-live "boot=live components hostname=lantern-ai username=lantern" \
  --iso-application "LANTERN AI Linux Prototype" --iso-volume "LANTERN_AI"
mkdir -p config/package-lists config/includes.chroot/opt/lantern config/includes.chroot/usr/share/applications config/includes.chroot/etc/skel/Desktop config/hooks/live
cat > config/package-lists/lantern.list.chroot <<'EOF'
linux-image-amd64
live-boot
live-config
systemd-sysv
task-xfce-desktop
network-manager
network-manager-gnome
firefox-esr
python3
python3-tk
curl
ca-certificates
git
mousepad
qemu-guest-agent
open-vm-tools-desktop
sudo
EOF
install -m 755 ../app/lantern_ai.py config/includes.chroot/opt/lantern/lantern_ai.py
cp ../assets/lantern.desktop config/includes.chroot/usr/share/applications/
install -m 755 ../assets/lantern.desktop config/includes.chroot/etc/skel/Desktop/
install -m 644 ../assets/wallpaper.svg config/includes.chroot/opt/lantern/
cp ../assets/0100-theme.hook.chroot config/hooks/live/
chmod +x config/hooks/live/*
lb build 2>&1 | tee build.log
sha256sum live-image-amd64.hybrid.iso > live-image-amd64.hybrid.iso.sha256
echo "ISO and checksum are in build/. Boot-test before using the installer."
