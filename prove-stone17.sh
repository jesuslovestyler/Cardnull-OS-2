#!/bin/sh
# Stone 17 proof: the stick.
#
# build-stick.sh lays dist/cardnull-stick.img — the
# disc's own bytes with a master boot record at its head
# and Cardnull's BIOS bootloader in the sectors after
# it, inside the ISO's unused system area.
#
#   Structure: the image is exactly the ISO's length;
#     sector 0 carries the boot signature and one
#     bootable partition spanning the whole image;
#     sectors 1..N are the bootloader, byte for byte;
#     the ISO's volume descriptor stands untouched at
#     byte 32768, and the image past the system area is
#     the ISO, byte for byte.
#   Boot: QEMU presents the image as a USB storage
#     device and SeaBIOS boots it as a hard disc — the
#     record loads the loader, the loader (told in
#     512-byte sectors now) walks the ISO filesystem and
#     brings up the drawn desktop, and the feather
#     visits (proofs/stone9-boot1.py, the drawn-desktop
#     scenario: desktop, the clock's advance, the visit).
#
# The physical witness — a real stick in a real machine —
# is NOT covered here and the README says so plainly.
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

echo "--- building the stick image ---"
./build-stick.sh >/dev/null || { echo "FAIL: build-stick.sh failed"; exit 1; }

echo "--- the image's shape ---"
python3 - <<'PYEOF' || exit 1
import struct, sys

img = open("dist/cardnull-stick.img", "rb").read()
iso = open("dist/cardnull-os-2.iso", "rb").read()
boot = open("build/boot.img", "rb").read()

def check(cond, what):
    print(("ok: " if cond else "FAIL: ") + what)
    if not cond:
        sys.exit(1)

check(len(img) == len(iso), "the stick image is the disc's own length")
check(img[510:512] == b"\x55\xaa", "the record carries the boot signature")
entry = img[446:462]
check(entry[0] == 0x80, "the one partition is marked bootable")
start, count = struct.unpack_from("<II", entry, 8)
check(start == 0 and count * 512 == len(img),
      "the partition spans the whole image")
n = len(boot)
check(img[512:512 + n] == boot,
      "the bootloader stands in the sectors after the record")
check(img[32768] == 1 and img[32769:32774] == b"CD001",
      "the ISO's volume descriptor stands untouched at byte 32768")
check(img[32768:] == iso[32768:],
      "past the system area the image is the disc, byte for byte")
PYEOF

echo "--- booting the stick as a USB hard disc ---"
SOCK="$WORK/monitor.sock"
DUMP="$WORK/dump.ppm"
IMG="$PWD/dist/cardnull-stick.img"
if [ -n "${QEMU:-}" ]; then
    # shellcheck disable=SC2086
    $QEMU -drive "file=$IMG,format=raw,if=none,id=usbstick" \
        -device usb-storage,drive=usbstick \
        -usb -boot order=c -display none -m 4096 -nic none \
        -rtc base=2026-11-15T00:00:00 \
        -monitor "unix:$SOCK,server,nowait" &
    QEMU_PID=$!
elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
    "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
        --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
        "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
        -drive "file=$IMG,format=raw,if=none,id=usbstick" \
        -device usb-storage,drive=usbstick \
        -usb -boot order=c -display none -m 4096 -nic none \
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
python3 tools/pixels.py proofs/stone9-boot1.py "$SOCK" "$DUMP" || exit 1
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""

echo "PASS"
