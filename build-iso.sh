#!/bin/sh
# Builds the Cardnull OS 2 witness disc: dist/cardnull-os-2.iso.
#
# The disc carries everything, and nothing else is needed:
#
#   /boot/cardnull.elf    the system itself
#   /boot/settings.bin    the settings module (Stone 4)
#   /boot/card.bin        the guest's card module (Stone 5)
#   /boot/guest.bin       the welcome guest (Stone 5)
#   /boot/boot.img        the BIOS boot image: Cardnull's
#                         own bootloader (Stone 11 —
#                         boot/cardnull-boot.asm)
#   /boot/efi.img         the EFI system partition image:
#                         \EFI\BOOT\BOOTX64.EFI — Cardnull's
#                         own EFI loader (Stone 16 —
#                         boot/cardnull-efi.c) — and its own
#                         copies of the kernel and modules
#
# The disc boots BOTH ways (the EFI door was healed by
# Stone 9 — see the README): on a BIOS machine through the
# El Torito boot image, and on a UEFI machine through the
# EFI system partition. At BOTH doors stands Cardnull's
# OWN loader now: at the BIOS door since Stone 11 (written
# for this repository, in assembly, public domain), and at
# the EFI door since Stone 16 (boot/cardnull-efi.c, a
# freestanding C program compiled for the firmware's own
# calling way and linked as an EFI application). Each
# reads the system and its modules, sets the picture mode
# the system asks for, lays the multiboot information in
# the same shape, and hands over — no GRUB stands at
# either door any more. The disc is laid with xorriso's
# El Torito support for both entries. (The bench's
# grub-mkrescue was tried first, long ago, and, from its
# relocated tree, silently produced a disc with no boot
# image at all; the explicit route below is the one that
# is proven — see prove-iso.sh.)
#
# The EFI loader's building: clang (a system clang when
# present, else the bench's own tree at ~/qemu-root)
# compiles the loader's C and its handover assembly for
# the Windows x64 calling way the UEFI world speaks, the
# system linker lays them as a PE file of the console
# kind, and a two-byte patch — the PE subsystem field,
# set by a small python3 pass below, because the linker
# will not name the EFI kind — makes it an EFI
# application, the kind the firmware loads. The spike of
# this road stands behind Stone 16's README section.
#
# The EFI partition is formed with mtools at its own
# default reckoning for a small image (which lays down
# FAT12): forcing FAT32 at this size was measured on the
# bench to make a partition the firmware would not boot.
#
# Tooling: xorriso and mtools from the PATH; the
# assembler and linker from the system.
#
# Overrides (used by prove-iso.sh to lay variant discs):
#   ISO_OUT, KERNEL_FILE, SETTINGS_FILE, CARD_FILE, GUEST_FILE

set -e
cd "$(dirname "$0")"

./build.sh >/dev/null

ISO_OUT="${ISO_OUT:-dist/cardnull-os-2.iso}"
KERNEL_FILE="${KERNEL_FILE:-build/cardnull.elf}"
SETTINGS_FILE="${SETTINGS_FILE:-build/settings.bin}"
CARD_FILE="${CARD_FILE:-build/card.bin}"
GUEST_FILE="${GUEST_FILE:-build/guest.bin}"

if command -v clang >/dev/null 2>&1; then
    CLANG=clang
elif [ -x "$HOME/qemu-root/usr/bin/clang" ]; then
    CLANG="$HOME/qemu-root/usr/bin/clang"
else
    echo "FAIL: no clang found (system or ~/qemu-root) — the EFI loader is built with it" >&2
    exit 1
fi
command -v xorriso >/dev/null 2>&1 || { echo "FAIL: no xorriso found" >&2; exit 1; }
command -v mformat >/dev/null 2>&1 || { echo "FAIL: no mtools found (mformat)" >&2; exit 1; }
command -v mcopy >/dev/null 2>&1 || { echo "FAIL: no mtools found (mcopy)" >&2; exit 1; }
command -v as >/dev/null 2>&1 || { echo "FAIL: no assembler found (as) — the BIOS bootloader is built with it" >&2; exit 1; }
command -v ld >/dev/null 2>&1 || { echo "FAIL: no linker found (ld) — both bootloaders are linked with it" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "FAIL: no python3 found — the EFI application's subsystem patch is laid with it" >&2; exit 1; }

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/root/boot" "$(dirname "$ISO_OUT")"

cp "$KERNEL_FILE" "$WORK/root/boot/cardnull.elf"
cp "$SETTINGS_FILE" "$WORK/root/boot/settings.bin"
cp "$CARD_FILE" "$WORK/root/boot/card.bin"
cp "$GUEST_FILE" "$WORK/root/boot/guest.bin"

# The BIOS door: Cardnull's own bootloader (Stone 11),
# assembled from boot/cardnull-boot.asm and linked flat at
# 0x7C00, padded to whole sectors — the El Torito catalog's
# load size spans the whole image, so the firmware lays it
# all at the doorstep and it runs as one stage.
as --32 -o "$WORK/boot.o" boot/cardnull-boot.asm
ld -m elf_i386 -Ttext 0x7C00 --oformat binary -o "$WORK/root/boot/boot.img" "$WORK/boot.o"
BOOT_SIZE=$(wc -c < "$WORK/root/boot/boot.img")
BOOT_SECTORS=$(( (BOOT_SIZE + 511) / 512 ))
truncate -s $(( BOOT_SECTORS * 512 )) "$WORK/root/boot/boot.img"

# The EFI door: Cardnull's own EFI loader (Stone 16),
# compiled from boot/cardnull-efi.c and its handover
# (boot/cardnull-efi-hand.S), linked as a PE file, and
# patched to the EFI application kind (subsystem 10) —
# the two bytes at the PE optional header's +68 that the
# firmware reads to know what it is loading.
mkdir -p "$WORK/esp/EFI/BOOT" "$WORK/esp/boot"
"$CLANG" --target=x86_64-pc-windows-gnu -ffreestanding -nostdinc \
    -fno-stack-protector -fno-builtin -mno-red-zone -O1 \
    -c boot/cardnull-efi.c -o "$WORK/efi.o"
"$CLANG" --target=x86_64-pc-windows-gnu -ffreestanding \
    -c boot/cardnull-efi-hand.S -o "$WORK/efi-hand.o"
ld -mi386pep -e efi_main "$WORK/efi.o" "$WORK/efi-hand.o" \
    -o "$WORK/esp/EFI/BOOT/BOOTX64.EFI"
python3 - "$WORK/esp/EFI/BOOT/BOOTX64.EFI" <<'PYEOF'
import struct
import sys
path = sys.argv[1]
data = bytearray(open(path, "rb").read())
pe = struct.unpack_from("<I", data, 0x3C)[0]
assert data[pe:pe + 4] == b"PE\0\0", "not a PE file"
struct.pack_into("<H", data, pe + 4 + 20 + 68, 10)  # EFI application
open(path, "wb").write(data)
PYEOF
cp "$KERNEL_FILE" "$WORK/esp/boot/cardnull.elf"
cp "$SETTINGS_FILE" "$WORK/esp/boot/settings.bin"
cp "$CARD_FILE" "$WORK/esp/boot/card.bin"
cp "$GUEST_FILE" "$WORK/esp/boot/guest.bin"
dd if=/dev/zero of="$WORK/root/boot/efi.img" bs=1M count=8 2>/dev/null
mformat -i "$WORK/root/boot/efi.img" ::
mcopy -i "$WORK/root/boot/efi.img" -s "$WORK/esp/EFI" ::
mcopy -i "$WORK/root/boot/efi.img" -s "$WORK/esp/boot" ::

xorriso -as mkisofs -o "$ISO_OUT" \
    -b boot/boot.img -no-emul-boot -boot-load-size "$BOOT_SECTORS" \
    -eltorito-alt-boot -e boot/efi.img -no-emul-boot \
    "$WORK/root" 2>/dev/null

SIZE=$(wc -c < "$ISO_OUT")
SHA=$(sha256sum "$ISO_OUT" | awk '{print $1}')
echo "Built $ISO_OUT ($SIZE bytes)"
echo "sha256: $SHA"
