#!/bin/sh
# Stone 5 proof: first guest. The system is booted with the
# three modules that ride its disc — the settings, the
# guest's card, and the guest image itself (QEMU's -initrd
# is the bench form of the bootloader's multiboot handoff):
#
#   Boot 1 (the guest as laid): the word 'guest' must bring
#     the guest through the door — its panel in its own
#     color inside the desktop, and the system's own line
#     afterwards saying it has gone home.
#   Boot 2 (a copy of the guest with one byte flipped; the
#     card still describes the true guest): the checksum no
#     longer matches the card; the system must refuse in
#     plain words, the guest must never appear, and the
#     desktop must stand unharmed.
#
# No disk is attached in either boot: the system ships as
# one disc and nothing else. Prints PASS or FAIL.

set -u
cd "$(dirname "$0")"

./build.sh >/dev/null || { echo "FAIL: build.sh failed"; exit 1; }
[ -f build/guest.bin ] || { echo "FAIL: the guest did not build"; exit 1; }

WORK=$(mktemp -d)
QEMU_PID=""
cleanup() {
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    rm -rf "$WORK"
}
trap cleanup EXIT

cp build/guest.bin "$WORK/guest.bin"
python3 - "$WORK" <<'PYEOF'
import sys
work = sys.argv[1]
guest = bytearray(open(work + "/guest.bin", "rb").read())
guest[100] ^= 0xFF
open(work + "/guest-tampered.bin", "wb").write(guest)
print(f"The guest as laid: {len(guest)} bytes (and a tampered twin, one byte flipped).")
PYEOF

echo "--- boot 1 (the guest as laid) ---"
SOCK="$WORK/monitor.sock"
QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96 "" "build/settings.bin,build/card.bin,build/guest.bin")
python3 tools/screen.py proofs/stone5-boot1.py "$SOCK" || exit 1
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""
sleep 1

echo "--- boot 2 (one byte flipped) ---"
SOCK="$WORK/monitor2.sock"
QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96 "" "build/settings.bin,build/card.bin,$WORK/guest-tampered.bin")
python3 tools/screen.py proofs/stone5-boot2.py "$SOCK"
