#!/bin/sh
# Feather-paint proof: the feather's visit, read back as
# writing. The shipped disc is booted at the BIOS door
# (the face of light), the word 'feather' is typed, and
# the feather window's painted pixels are DECODED letter
# by letter against the system's own letter shapes
# (proofs/featherpaint-boot1.py, through tools/pixels.py):
# the feather's three lines must read exactly as the
# feather wrote them, the panel must stand solid with no
# unpainted band, and the system's own line below the
# window must read whole too.
#
# This proof stands because the earlier ones could not
# see the fault it watches for: the visit's first
# painting scaled each of the feather's cells from the
# text face's grid onto the face of light's grid, one
# letter in five was overwritten by its neighbor, and
# the panel stood banded — garbled letters carry the
# same colors as whole ones, so the band-and-count
# checks of Stones 9 and 14 passed while Tyler, on his
# own machine, read "A fetheris vsitig" for "A feather
# is visiting" (November 15, 2026). Counting colors is
# not reading; this proof reads.
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

SOCK="$WORK/monitor.sock"
DUMP="$WORK/dump.ppm"
if [ -n "${QEMU:-}" ]; then
    # shellcheck disable=SC2086
    $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
        -boot order=d -display none -m 4096 -nic none \
        -rtc base=2026-11-15T00:00:00 \
        -monitor "unix:$SOCK,server,nowait" &
    QEMU_PID=$!
elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
    "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
        --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
        "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
        -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
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
python3 tools/pixels.py proofs/featherpaint-boot1.py "$SOCK" "$DUMP" || exit 1

echo "PASS"
