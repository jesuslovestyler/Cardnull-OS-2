#!/bin/sh
# Stone 2 proof: ears. Builds Cardnull OS 2, boots it headless
# in QEMU (-m 96), types on the emulated keyboard through the
# monitor, and reads the screen back: the typing line echoes
# (with a Backspace correction), each known word is answered
# in plain words, an unknown word gets the kind answer, and
# 'clear' wipes the screen while the machine keeps listening.
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

SOCK="$WORK/monitor.sock"
QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96)

python3 tools/screen.py proofs/stone2.py "$SOCK"
