#!/bin/sh
# build-stick.sh — lay the Cardnull stick image (Stone 17).
#
# The stick image is the disc's own bytes — the very ISO
# build-iso.sh lays, an ISO9660 image whose volume
# descriptor stands at byte 32768 — with the ISO's unused
# system area (its first sixteen sectors) given to
# booting as a hard disc:
#
#   sector 0        the master boot record: Cardnull's
#                   own stub (boot/cardnull-mbr.asm),
#                   which loads the bootloader from the
#                   sectors after it and jumps to it
#   sectors 1..N    Cardnull's BIOS bootloader
#                   (boot/cardnull-boot.asm), the same
#                   loader the disc's BIOS door boots;
#                   it asks the device its sector measure
#                   and walks the ISO filesystem from
#                   byte 32768 exactly as on the CD
#   sectors 16..    the ISO, untouched: the system, the
#                   modules, and the EFI system partition
#                   all ride along as on the disc
#
# Nothing foreign stands on the stick: no GRUB, no Linux,
# no emulator — the firmware boots the record, the record
# loads Cardnull's loader, and the loader brings up
# Cardnull, natively, as a USB hard disc.
#
# Output: dist/cardnull-stick.img, beside the ISO.
#
# Tooling: as for build-iso.sh (which this runs first);
# the bench's xorriso and mtools live in ~/qemu-root on
# Tyler's bench and are put on the PATH when present.

set -e
cd "$(dirname "$0")"

if [ -d "$HOME/qemu-root/usr/bin" ]; then
    PATH="$HOME/qemu-root/usr/bin:$PATH"
    export PATH
fi

# The disc first: the stick is its bytes.
./build-iso.sh

ISO=dist/cardnull-os-2.iso
IMG=dist/cardnull-stick.img

# The bootloader, assembled exactly as at the disc's
# BIOS door and padded to whole 512-byte sectors. It
# must fit the system area after the record: sectors
# 1..15.
mkdir -p build
as --32 -o build/boot-stick.o boot/cardnull-boot.asm
ld -m elf_i386 -Ttext 0x7C00 --oformat binary -o build/boot.img build/boot-stick.o
BOOT_SIZE=$(wc -c < build/boot.img)
BOOT_SECTORS=$(( (BOOT_SIZE + 511) / 512 ))
if [ "$BOOT_SECTORS" -gt 15 ]; then
    echo "FAIL: the bootloader takes $BOOT_SECTORS sectors; the stick's system area holds 15" >&2
    exit 1
fi
truncate -s $(( BOOT_SECTORS * 512 )) build/boot.img

# The record, with the two counts baked in: how many
# sectors of bootloader follow it, and how long the
# whole image runs, in 512-byte sectors.
ISO_SIZE=$(wc -c < "$ISO")
STICK_SECTORS=$(( ISO_SIZE / 512 ))
as --32 --defsym BOOT_SECTORS="$BOOT_SECTORS" --defsym STICK_SECTORS="$STICK_SECTORS" \
    -o build/mbr.o boot/cardnull-mbr.asm
ld -m elf_i386 -Ttext 0x600 --oformat binary -o build/mbr.bin build/mbr.o
MBR_SIZE=$(wc -c < build/mbr.bin)
if [ "$MBR_SIZE" -ne 512 ]; then
    echo "FAIL: the master boot record is $MBR_SIZE bytes, not 512" >&2
    exit 1
fi

# Lay the image: the disc's bytes, with the record at
# its head and the bootloader in the sectors after it.
cp "$ISO" "$IMG"
dd if=build/mbr.bin of="$IMG" bs=512 seek=0 conv=notrunc 2>/dev/null
dd if=build/boot.img of="$IMG" bs=512 seek=1 conv=notrunc 2>/dev/null

IMG_SIZE=$(wc -c < "$IMG")
echo "Built $IMG ($IMG_SIZE bytes)"
sha256sum "$IMG" | sed 's/^/sha256: /; s/  .*//'
