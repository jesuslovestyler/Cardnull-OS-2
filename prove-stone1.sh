#!/bin/sh
# Stone 1 proof: first boot. Builds Cardnull OS 2, boots it
# headless in QEMU with a distinctive memory size (-m 96),
# and reads the emulated screen back through the monitor:
# the welcome lines must be there, in plain words, and the
# memory figure must match the machine it was given.
#
# Prints PASS or FAIL. The bench pattern is the Nifla
# language's own (see tools/launch.sh and tools/screen.py).

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

SOCK="$WORK/monitor.sock"
QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96)

python3 tools/screen.py proofs/stone1.py "$SOCK"
