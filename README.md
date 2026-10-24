# LANTERN AI Linux — prototype 0.2

Debian 13 (trixie), amd64, XFCE desktop, LANTERN wallpaper and local AI chat.
This archive is source and build scripts, NOT a bootable ISO. The full image has
not been built or boot-tested. Voice input, autonomous actions, custom kernel,
and preloaded AI models are not included. Debian retains its normal identity,
updates, licensing and installer. Hardware compatibility requires testing.

## Fast path: use it inside Windows

1. Install a VM application such as VirtualBox, VMware, or Hyper-V.
2. Download an official Debian 13 amd64 installer from https://www.debian.org/ .
3. Create a VM with 4 CPU cores, 8 GB RAM and 50 GB disk (suggested starting
   allocation; your Windows host needs additional RAM). Select XFCE at install.
4. Extract this ZIP inside Debian. In a terminal in this folder run:

   sudo bash install-desktop.sh

5. Install Ollama using the AI setup below. Open LANTERN AI from the app menu.

The desktop installer adds the app and wallpaper file to an existing Debian
system; it does not change that system's desktop environment or wallpaper.

## Build your custom bootable ISO

Use a fresh Debian 13 amd64 VM with internet access, sudo, and at least 30 GB
free disk for building. These scripts are Linux scripts, not Windows commands.
From this extracted folder run:

    sudo bash build-iso.sh

This installs build dependencies, creates a new build/ directory and runs
Debian live-build. The output is:

    build/live-image-amd64.hybrid.iso
    build/live-image-amd64.hybrid.iso.sha256

Build time and download size depend on mirrors and your connection. If the
build fails, inspect build/build.log. Retry from a new extracted source folder.
The image includes an XFCE live desktop, LANTERN launcher and Debian live
installer. AI runtime and model downloads are a separate post-install step.
Default live credentials are managed by Debian live-config: user lantern,
commonly password live. Verify in the VM; do not expose a live session to
untrusted networks. Installed systems use the account created by the installer.

### VM boot check

Create a new blank VM and attach the generated ISO as its optical drive. Boot
Live first; check desktop, networking and LANTERN launcher. Test installation to
the VM's blank virtual disk, detach the ISO, and verify that it boots again.
For an interactive live-boot check on Debian with a graphical desktop:

    sudo apt-get install qemu-system-x86 ovmf
    bash boot-test.sh bios
    bash boot-test.sh uefi

The launcher uses KVM when accessible, otherwise slower software emulation.
It attaches no hard disk and cannot validate installation. Record observations
in BOOT_CHECKLIST.md. Closing QEMU does not establish a passing boot test.
Test BIOS and UEFI VM modes separately before claiming support for either.
Secure Boot, GPU drivers and particular Wi-Fi adapters are not validated.

### Direct installation on a computer

Back up your files and save Windows recovery/BitLocker information first.
Write the generated ISO to a spare USB using Rufus or another image writer;
writing erases the selected USB. Boot the USB and choose Live to test hardware
before launching Debian's installer. Installation can erase the selected disk:
check the target carefully. For dual boot, retain Windows partitions and use
manual partitioning only after reviewing your disk layout. This project does
not automatically partition disks or modify Windows. Prefer the VM test first.

## Local AI setup (after Debian installation)

The model is not bundled. Internet is required initially; downloaded local
models can then run offline. CPU inference works but speed varies. Start with
8 GB RAM; larger models need more memory. VM graphics acceleration does not
necessarily provide GPU inference.

Follow https://ollama.com/download/linux for current installation instructions.
For an inspectable download of their installer:

    curl -fL https://ollama.com/install.sh -o ollama-install.sh
    less ollama-install.sh
    sh ollama-install.sh
    ollama pull qwen2.5:1.5b
    ollama list

Open LANTERN AI. Its model field must exactly match an installed model name.
It connects only to http://127.0.0.1:11434/api/chat and sends chat history there.
Keep Ollama bound to loopback. The app cannot execute commands or read files.
History lives in RAM until the window closes; Ollama has its own logs and model
storage. Other desktop software, updates and downloads may use the internet.
Review each model's license before redistribution or commercial use.

If chat fails, run `ollama list`, confirm the selected model, and check
`systemctl status ollama`. The first response may take time while a model loads.
Downloading models in a nonpersistent live session loses them after reboot;
install to disk first or configure persistence separately.

## Validation and limits

Python compilation, shell syntax and mocked AI protocol/error tests are run on
source. These do not establish bootability, installer success, actual model
inference, theme compatibility across monitors, or hardware support. See
VALIDATION.txt for the checks completed in the creation environment.

## Source references

- https://live-team.pages.debian.net/live-manual/html/live-manual.en.html
- https://manpages.debian.org/trixie/live-build/lb_config.1.en.html
- https://github.com/ollama/ollama/blob/main/docs/api/introduction.mdx
- https://ollama.com/download/linux

## License

Original LANTERN scripts and vector artwork: MIT (see LICENSE). Debian packages,
Ollama and AI model weights retain their respective licenses. Before sharing a
built image, review bundled package licenses and applicable source obligations.
