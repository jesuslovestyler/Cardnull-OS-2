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
#   /boot/grub/eltorito.img  the boot image (see below)
#
# The loader on the disc is GRUB, used honestly as a means
# to boot the multiboot kernel on a BIOS machine (UTM's
# standard x86_64 machine among them): Cardnull's own
# bootloader remains future work, as it was in the first
# Cardnull OS's early doors. The boot image is GRUB's
# cdboot.img + a core image made by grub-mkimage carrying
# the modules the boot needs (biosdisk, iso9660, multiboot,
# configfile, normal), and the disc is laid with xorriso's
# El Torito support. (The bench's grub-mkrescue was tried
# first and, from its relocated tree, silently produced a
# disc with no boot image at all; the explicit route below
# is the one that is proven — see prove-iso.sh.)
#
# Tooling: grub-mkimage and its i386-pc module tree are
# taken from a system install when present, else from the
# bench's own tree at ~/qemu-root; xorriso from the PATH.
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
elif [ -x "$HOME/qemu-root/usr/bin/grub-mkimage" ]; then
    GRUB_MKIMAGE="$HOME/qemu-root/usr/bin/grub-mkimage"
    GRUB_PC="$HOME/qemu-root/usr/lib/grub/i386-pc"
    export LD_LIBRARY_PATH="$HOME/qemu-root/usr/lib/x86_64-linux-gnu:$HOME/qemu-root/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
else
    echo "FAIL: no grub-mkimage found (system or ~/qemu-root)" >&2
    exit 1
fi
command -v xorriso >/dev/null 2>&1 || { echo "FAIL: no xorriso found" >&2; exit 1; }

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

xorriso -as mkisofs -o "$ISO_OUT" \
    -b boot/grub/eltorito.img -no-emul-boot -boot-load-size 4 \
    -boot-info-table "$WORK/root" 2>/dev/null

SIZE=$(wc -c < "$ISO_OUT")
SHA=$(sha256sum "$ISO_OUT" | awk '{print $1}')
echo "Built $ISO_OUT ($SIZE bytes)"
echo "sha256: $SHA"
