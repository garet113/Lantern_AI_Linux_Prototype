#!/bin/bash
# Interactive live-boot check; does not report an automatic boot pass.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
mode=${1:-bios}
iso=build/live-image-amd64.hybrid.iso
[[ $mode == bios || $mode == uefi ]] || { echo "Usage: bash boot-test.sh [bios|uefi]"; exit 1; }
[[ -s $iso ]] || { echo "ISO missing. Build it first with sudo bash build-iso.sh"; exit 1; }
command -v qemu-system-x86_64 >/dev/null || { echo "Install qemu-system-x86 and ovmf on your Debian VM."; exit 1; }
(cd build && sha256sum -c live-image-amd64.hybrid.iso.sha256)
mkdir -p test-results
accel=tcg
[[ -r /dev/kvm && -w /dev/kvm ]] && accel=kvm
firmware=()
if [[ $mode == uefi ]]; then
    code=/usr/share/OVMF/OVMF_CODE_4M.fd
    vars=/usr/share/OVMF/OVMF_VARS_4M.fd
    [[ -f $code && -f $vars ]] || { echo "Install ovmf; expected Debian OVMF 4M firmware files."; exit 1; }
    cp "$vars" test-results/uefi-vars.fd
    firmware=(-drive "if=pflash,format=raw,readonly=on,file=$code" -drive "if=pflash,format=raw,file=test-results/uefi-vars.fd")
fi
echo "Check the boot menu, live desktop, networking and Lantern AI launcher."
echo "No hard disk is attached. This checks live boot only; it cannot validate installation."
echo "Close QEMU when finished and record observations in BOOT_CHECKLIST.md."
qemu-system-x86_64 -machine q35 -accel "$accel" -m 4096 -smp 2 \
    "${firmware[@]}" -cdrom "$iso" -boot order=d -nic user,model=virtio-net-pci \
    -serial "file:test-results/$mode-serial.log" -no-reboot
