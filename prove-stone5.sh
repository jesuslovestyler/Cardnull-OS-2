#!/bin/sh
# Stone 5 proof: first feather. The system is booted with the
# two modules that ride its disc — the settings, and the
# feather itself, its card at its own head (QEMU's -initrd
# is the bench form of the bootloader's multiboot handoff):
#
#   Boot 1 (the feather as laid): the word 'feather' must bring
#     the feather through the door — its panel in its own
#     color inside the desktop, and the system's own line
#     afterwards saying it has gone home.
#   Boot 2 (a copy of the feather with one byte flipped in its
#     program; its card still promises the true checksum): the
#     reckoning no longer matches the card; the system must
#     refuse in plain words, the feather must never appear,
#     and the desktop must stand unharmed.
#
# No disk is attached in either boot: the system ships as
# one disc and nothing else. Prints PASS or FAIL.

set -u
cd "$(dirname "$0")"

./build.sh >/dev/null || { echo "FAIL: build.sh failed"; exit 1; }
[ -f build/welcome.feather ] || { echo "FAIL: the feather did not build"; exit 1; }

WORK=$(mktemp -d)
QEMU_PID=""
cleanup() {
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    rm -rf "$WORK"
}
trap cleanup EXIT

cp build/welcome.feather "$WORK/welcome.feather"
python3 - "$WORK" <<'PYEOF'
import sys
work = sys.argv[1]
feather = bytearray(open(work + "/welcome.feather", "rb").read())
start = feather.index(b"\n\n") + 2
feather[start + 100] ^= 0xFF
open(work + "/feather-tampered.feather", "wb").write(feather)
print(f"The feather as laid: {len(feather)} bytes, card and all (and a tampered twin, one program byte flipped).")
PYEOF

echo "--- boot 1 (the feather as laid) ---"
SOCK="$WORK/monitor.sock"
QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96 "" "build/settings.bin,build/welcome.feather")
python3 tools/screen.py proofs/stone5-boot1.py "$SOCK" || exit 1
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""
sleep 1

echo "--- boot 2 (one byte flipped) ---"
SOCK="$WORK/monitor2.sock"
QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96 "" "build/settings.bin,$WORK/feather-tampered.feather")
python3 tools/screen.py proofs/stone5-boot2.py "$SOCK"
