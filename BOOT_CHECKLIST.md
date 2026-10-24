# Boot and installer acceptance checklist

Status: NOT RUN. No ISO was produced in the creation environment.
The boot-test script opens a VM; process startup or a zero exit code is not a pass.
Record the ISO SHA256, test date, firmware mode, VM resources, and observations.

For both BIOS and UEFI (Secure Boot not covered):
- [ ] ISO checksum verifies.
- [ ] Boot menu appears and Live starts without kernel panic.
- [ ] XFCE desktop appears; keyboard and mouse work.
- [ ] Lantern launcher opens its chat window.
- [ ] Wallpaper appears (monitor-specific XFCE paths may require adjustment).
- [ ] Networking works.
- [ ] Missing Ollama is reported clearly without crashing the chat window.

Separate installation test using a new VM with a blank 50 GB virtual disk:
- [ ] Installer offers the virtual disk and completes successfully.
- [ ] Eject ISO and boot from the installed virtual disk.
- [ ] Login works using installer-created credentials.
- [ ] Launcher, networking and desktop work after reboot.
- [ ] Install Ollama and pull the documented model.
- [ ] Receive an actual model response, then disconnect networking and repeat.

Do not attach host physical disks for this test. Do not mark physical hardware
support based on a VM result. Physical USB boot needs its own hardware checks.
