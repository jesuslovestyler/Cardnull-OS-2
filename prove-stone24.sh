#!/bin/sh
# Stone 24 proof: the paint feather. The shipped disc
# is booted at the BIOS door (the face of light), the
# word 'paint' is typed, and the paint feather must be
# received through the feather door — its card checked
# first, as its plain-words answer line says — and must
# then DRAW, on the real pointer road: a press on its
# canvas paints a cell in the chosen color, a held drag
# paints along its path, a press on a swatch chooses
# that color (its own words in the window name it, and
# the star moves), the next press paints in the new
# color, and a press on its Clear word empties the
# canvas again (proofs/stone24-boot1.py, through
# tools/pixels.py, reading pixels and decoding letters
# the featherpaint way).
#
# A feather owns no machine — the compiler refuses it
# the mouse — so the presses travel the contract the
# door honestly carries: the host carries each press
# across the desk as another checked visit (gift 1000
# plus the press's row times 100 plus its column), and
# the feather itself reckons what each press means and
# lays every mark. This proof drives the bench's PS/2
# mouse and reads the painted pixels back; no static
# glance stands in for any of it.
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
python3 tools/pixels.py proofs/stone24-boot1.py "$SOCK" "$DUMP" || exit 1

echo "PASS"
