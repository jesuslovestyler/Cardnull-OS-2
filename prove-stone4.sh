#!/bin/sh
# Stone 4 proof: remembers. The script makes one scratch
# disk (8 MiB, all blank) and boots Cardnull OS 2 on it
# twice, reading the bar's clock back both times:
#
#   Boot 1: nothing saved — the clock must start on Eastern
#     time (hour 19 against a count near zero). The word
#     'utc' must move the hour to 00, and the machine must
#     say it will remember.
#   Boot 2: the same disk, untouched by hand — the clock
#     must come up at hour 00 on its own, and 'eastern'
#     must move it back to 19.
#
# SAFETY: the only disk ever attached is the scratch image
# this script creates in its own scratch folder.
#
# Prints PASS or FAIL.

set -u
cd "$(dirname "$0")"

./build.sh >/dev/null || { echo "FAIL: build.sh failed"; exit 1; }

WORK=$(mktemp -d)
QEMU_PID=""
cleanup() {
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    rm -rf "$WORK"
}
trap cleanup EXIT

IMG="$WORK/scratch-disk.img"
python3 - "$IMG" <<'PYEOF'
import sys
open(sys.argv[1], "wb").write(bytes(8 * 1024 * 1024))
print("Made the scratch disk: 8 MiB, blank.")
PYEOF

echo "--- boot 1 (fresh disk) ---"
SOCK="$WORK/monitor.sock"
QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96 "$IMG")
python3 tools/screen.py proofs/stone4-boot1.py "$SOCK" || exit 1
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""
sleep 1

echo "--- boot 2 (same disk) ---"
SOCK="$WORK/monitor2.sock"
QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96 "$IMG")
python3 tools/screen.py proofs/stone4-boot2.py "$SOCK"
