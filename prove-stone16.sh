#!/bin/sh
# Stone 16 proof: our own EFI doorman. The shipped disc
# is audited and booted both ways:
#
#   The audit: the disc's own file list and its EFI
#     system partition's list are read — no GRUB stands
#     anywhere on the disc (no /boot/grub, no GRUB file
#     in the partition), and the \EFI\BOOT\BOOTX64.EFI
#     that stands there is Cardnull's own loader, known
#     by its own plain-words failure line inside it.
#   Boot 1 (the EFI door, OVMF firmware): the shipped
#     disc, Stone 9's own scenario — the desktop drawn
#     in light, the clock's hand moving, the feather's
#     visit in its green — now through Cardnull's own
#     EFI loader where GRUB stood before.
#   Boot 2 (the BIOS door, the same disc): the same
#     scenario again — Cardnull's own BIOS doorman
#     (Stone 11) unregressed on the disc whose other
#     door changed.
#
# Prints PASS or FAIL.

set -u
cd "$(dirname "$0")"

WORK=$(mktemp -d)
QEMU_PID=""
cleanup() {
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    rm -rf "$WORK"
}
trap cleanup EXIT

echo "--- building the shipped disc ---"
./build-iso.sh || { echo "FAIL: build-iso.sh failed"; exit 1; }

echo "--- the audit: no GRUB anywhere on the disc ---"
mkdir -p "$WORK/tree"
xorriso -osirrox on -indev dist/cardnull-os-2.iso -extract / "$WORK/tree" >/dev/null 2>&1 \
    || { echo "FAIL: the disc could not be read back"; exit 1; }
if find "$WORK/tree" | grep -qi grub; then
    echo "FAIL: something named for GRUB stands on the disc"
    find "$WORK/tree" | grep -i grub
    exit 1
fi
echo "ok: no file or folder on the disc is named for GRUB"
[ -f "$WORK/tree/boot/cardnull.elf" ] && [ -f "$WORK/tree/boot/efi.img" ] \
    || { echo "FAIL: the disc does not carry the system and its EFI partition"; exit 1; }
ESP_LIST=$(mdir -i "$WORK/tree/boot/efi.img" -s -b :: 2>/dev/null)
echo "$ESP_LIST" | grep -q "EFI/BOOT/BOOTX64.EFI" \
    || { echo "FAIL: no BOOTX64.EFI stands in the EFI partition"; exit 1; }
if echo "$ESP_LIST" | grep -qi grub; then
    echo "FAIL: something named for GRUB stands in the EFI partition"
    exit 1
fi
echo "ok: the EFI partition holds BOOTX64.EFI and nothing named for GRUB"
mcopy -i "$WORK/tree/boot/efi.img" ::/EFI/BOOT/BOOTX64.EFI "$WORK/BOOTX64.EFI" >/dev/null 2>&1 \
    || { echo "FAIL: BOOTX64.EFI could not be read out of the partition"; exit 1; }
# The loader's words stand inside it as the firmware's
# own text kind (two bytes a letter), so they are looked
# for in that shape.
if python3 -c "
import sys
data = open('$WORK/BOOTX64.EFI', 'rb').read()
sys.exit(0 if 'Cardnull could not start'.encode('utf-16-le') in data else 1)
"; then
    echo "ok: the BOOTX64.EFI is Cardnull's own loader (its failure words stand inside it)"
else
    echo "FAIL: the BOOTX64.EFI does not carry the loader's own words"
    exit 1
fi

# Boots an ISO as the machine's only drive under OVMF
# (UEFI firmware) and runs a PIXEL scenario against it —
# prove-stone9.sh's boot_iso_efi, kept in the same shape.
boot_iso_efi() {
    ISO="$1"
    SCENARIO="$2"
    SOCK="$WORK/monitor-$3.sock"
    DUMP="$WORK/dump-$3.ppm"
    OVMF_DIR="$HOME/qemu10-root/usr/share/OVMF"
    if [ -n "${QEMU:-}" ]; then
        echo "FAIL: the EFI boot needs the bench QEMU's OVMF firmware; unset QEMU" >&2
        exit 1
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ] && [ -f "$OVMF_DIR/OVMF_CODE_4M.fd" ]; then
        cp "$OVMF_DIR/OVMF_VARS_4M.fd" "$WORK/vars-$3.fd"
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
            -drive "file=$ISO,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -drive "if=pflash,format=raw,readonly=on,file=$OVMF_DIR/OVMF_CODE_4M.fd" \
            -drive "if=pflash,format=raw,file=$WORK/vars-$3.fd" \
            -monitor "unix:$SOCK,server,nowait" \
            -L "$HOME/qemu10-root/usr/share/qemu" \
            -L "$HOME/qemu10-root/usr/share/seabios" \
            >/dev/null 2>&1 &
        QEMU_PID=$!
    else
        echo "FAIL: no bench QEMU / OVMF found (looked for ~/qemu10-root)" >&2
        exit 1
    fi
    python3 tools/pixels.py "$SCENARIO" "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

# Boots an ISO as the machine's only drive under the
# BIOS firmware and runs a PIXEL scenario against it —
# prove-stone9.sh's boot_iso_pixels, kept in the same
# shape.
boot_iso_pixels() {
    ISO="$1"
    SCENARIO="$2"
    SOCK="$WORK/monitor-$3.sock"
    DUMP="$WORK/dump-$3.ppm"
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=$ISO,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
            -drive "file=$ISO,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" \
            -L "$HOME/qemu10-root/usr/share/qemu" \
            -L "$HOME/qemu10-root/usr/share/seabios" \
            >/dev/null 2>&1 &
        QEMU_PID=$!
    else
        echo "FAIL: no QEMU found (looked for ~/qemu10-root; set QEMU to a qemu-system-x86_64 command)" >&2
        exit 1
    fi
    python3 tools/pixels.py "$SCENARIO" "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

echo "--- boot 1 (the EFI door: our own loader under OVMF) ---"
boot_iso_efi dist/cardnull-os-2.iso proofs/stone9-boot1.py 1 || exit 1

echo "--- boot 2 (the BIOS door: the same disc, unregressed) ---"
boot_iso_pixels dist/cardnull-os-2.iso proofs/stone9-boot1.py 2 || exit 1

echo "PASS"
