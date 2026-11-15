#!/bin/sh
# Stone 3 proof: a face. Builds Cardnull OS 2 (now with its
# screen library), boots it headless in QEMU (-m 96), and
# reads the emulated screen back: the bar and its colors, the
# welcome panel and its colors, a clock that advances between
# two readings, and the Stone 2 commands answering in their
# region of the faced screen.
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

python3 tools/screen.py proofs/stone3.py "$SOCK"
