#!/bin/sh
# Builds the Cardnull OS 2 witness disc: dist/cardnull-os-2.iso.
#
# The disc carries everything, and nothing else is needed:
#
#   /boot/cardnull.elf    the system itself
#   /boot/settings.bin    the settings module (Stone 4)
#   /boot/card.bin        the guest's card module (Stone 5)
#   /boot/guest.bin       the welcome guest (Stone 5)
#   /boot/grub/grub.cfg   the loader's directions
#   /boot/grub/eltorito.img  the BIOS boot image (see below)
#   /boot/efi.img         the EFI system partition image:
#                         \EFI\BOOT\BOOTX64.EFI and its own
#                         copies of the kernel and modules
#
# The disc boots BOTH ways (the EFI door was healed by
# Stone 9 — see the README): on a BIOS machine through the
# El Torito boot image, and on a UEFI machine through the
# EFI system partition. The loader on the disc is GRUB at
# both doors, used honestly as a means to boot the
# multiboot kernel: Cardnull's own bootloader remains
# future work, as it was in the first Cardnull OS's early
# doors. The BIOS boot image is GRUB's cdboot.img + a core
# image made by grub-mkimage carrying the modules the boot
# needs (biosdisk, iso9660, multiboot, configfile, normal);
# the EFI image carries a grub-mkimage x86_64-efi build
# whose modules add the picture-screen drivers (all_video,
# video, efi_gop) the framebuffer handoff needs, and the
# disc is laid with xorriso's El Torito support for both
# entries. (The bench's grub-mkrescue was tried first and,
# from its relocated tree, silently produced a disc with
# no boot image at all; the explicit route below is the
# one that is proven — see prove-iso.sh.)
#
# The EFI partition is formed with mtools at its own
# default reckoning for a small image (which lays down
# FAT12): forcing FAT32 at this size was measured on the
# bench to make a partition the firmware would not boot.
#
# Tooling: grub-mkimage and its module trees are taken
# from a system install when present, else from the
# bench's own tree at ~/qemu-root; xorriso and mtools from
# the PATH.
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

if command -v grub-mkimage >/dev/null 2>&1 && [ -d /usr/lib/grub/i386-pc ]; then
    GRUB_MKIMAGE=grub-mkimage
    GRUB_PC=/usr/lib/grub/i386-pc
    GRUB_EFI=/usr/lib/grub/x86_64-efi
elif [ -x "$HOME/qemu-root/usr/bin/grub-mkimage" ]; then
    GRUB_MKIMAGE="$HOME/qemu-root/usr/bin/grub-mkimage"
    GRUB_PC="$HOME/qemu-root/usr/lib/grub/i386-pc"
    GRUB_EFI="$HOME/qemu-root/usr/lib/grub/x86_64-efi"
    export LD_LIBRARY_PATH="$HOME/qemu-root/usr/lib/x86_64-linux-gnu:$HOME/qemu-root/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
else
    echo "FAIL: no grub-mkimage found (system or ~/qemu-root)" >&2
    exit 1
fi
[ -d "$GRUB_EFI" ] || { echo "FAIL: no x86_64-efi GRUB tree found at $GRUB_EFI" >&2; exit 1; }
command -v xorriso >/dev/null 2>&1 || { echo "FAIL: no xorriso found" >&2; exit 1; }
command -v mformat >/dev/null 2>&1 || { echo "FAIL: no mtools found (mformat)" >&2; exit 1; }
command -v mcopy >/dev/null 2>&1 || { echo "FAIL: no mtools found (mcopy)" >&2; exit 1; }

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/root/boot/grub" "$(dirname "$ISO_OUT")"

cp "$KERNEL_FILE" "$WORK/root/boot/cardnull.elf"
cp "$SETTINGS_FILE" "$WORK/root/boot/settings.bin"
cp "$CARD_FILE" "$WORK/root/boot/card.bin"
cp "$GUEST_FILE" "$WORK/root/boot/guest.bin"
cat > "$WORK/root/boot/grub/grub.cfg" <<'EOF'
set timeout=0
set default=0
menuentry "Cardnull" {
    multiboot /boot/cardnull.elf
    module /boot/settings.bin
    module /boot/card.bin
    module /boot/guest.bin
}
EOF

"$GRUB_MKIMAGE" -d "$GRUB_PC" -O i386-pc -o "$WORK/core.img" \
    -p /boot/grub biosdisk iso9660 multiboot configfile normal
cat "$GRUB_PC/cdboot.img" "$WORK/core.img" > "$WORK/root/boot/grub/eltorito.img"

# The EFI door: an 8 MiB system partition holding the EFI
# GRUB and its own copies of the kernel and the modules
# (its GRUB reads them from the partition it stands on).
mkdir -p "$WORK/esp/EFI/BOOT" "$WORK/esp/boot/grub"
"$GRUB_MKIMAGE" -d "$GRUB_EFI" -O x86_64-efi -o "$WORK/esp/EFI/BOOT/BOOTX64.EFI" \
    -p /boot/grub fat part_gpt part_msdos iso9660 multiboot configfile normal \
    all_video video efi_gop
cp "$KERNEL_FILE" "$WORK/esp/boot/cardnull.elf"
cp "$SETTINGS_FILE" "$WORK/esp/boot/settings.bin"
cp "$CARD_FILE" "$WORK/esp/boot/card.bin"
cp "$GUEST_FILE" "$WORK/esp/boot/guest.bin"
cp "$WORK/root/boot/grub/grub.cfg" "$WORK/esp/boot/grub/grub.cfg"
dd if=/dev/zero of="$WORK/root/boot/efi.img" bs=1M count=8 2>/dev/null
mformat -i "$WORK/root/boot/efi.img" ::
mcopy -i "$WORK/root/boot/efi.img" -s "$WORK/esp/EFI" ::
mcopy -i "$WORK/root/boot/efi.img" -s "$WORK/esp/boot" ::

xorriso -as mkisofs -o "$ISO_OUT" \
    -b boot/grub/eltorito.img -no-emul-boot -boot-load-size 4 \
    -boot-info-table \
    -eltorito-alt-boot -e boot/efi.img -no-emul-boot \
    "$WORK/root" 2>/dev/null

SIZE=$(wc -c < "$ISO_OUT")
SHA=$(sha256sum "$ISO_OUT" | awk '{print $1}')
echo "Built $ISO_OUT ($SIZE bytes)"
echo "sha256: $SHA"
