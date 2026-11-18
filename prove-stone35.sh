#!/bin/sh
# Stone 35 proof: painting no longer flickers the
# other windows — the second of the four glitches
# Tyler witnessed in UTM (Nov 16, 2026): "when i paint
# with multiple windows, all the windows flicker."
#
# The mechanism, as Stones 26–33 left it: every
# feather visit ended in a whole-desktop repaint, and
# a pointer press on a feather's window repainted the
# whole desktop once as it landed and again as the
# visit was received — so while a person painted,
# every other window on the desktop was washed and
# redrawn twice per press, and that shimmer was the
# flicker. Stone 35 lays Stone 34's region road over
# the visited window alone (and over the window it
# took the forward place from, whose title bar the
# coming-forward changes; and over the files window
# too when a disk is keeping the picture, whose list
# the keeping can change): the press's own repaint in
# the pointer's reckoning, and the receiving's
# repaint after the visit, for the paint, calculator,
# and welcome feathers alike.
#
# The shipped disc is booted at the BIOS door (the
# face of light), no disk fitted, in two boots — on
# this bench a second pointer press after a
# feather-visit press is not reliable (the emulated
# pointer's button keeping desyncs across a long
# visit), so each boot makes one press. Boot 1 opens
# every window, then presses the calculator's 7 key;
# boot 2 opens every window, then presses the paint
# canvas. The visited windows work as they always
# have, the welcome window's every pixel stands
# hashed and exactly as it stood after each press,
# and each press's cost is read out of the guest in
# the runtime's loop passes and reckoned against the
# old road's measures (proofs/stone35-boot1.py and
# proofs/stone35-boot2.py).
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
./build-iso.sh >/dev/null || { echo "FAIL: build-iso.sh failed"; exit 1; }

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

echo "--- boot 1 (no disk: a calculator press, the far window hashed) ---"
python3 proofs/stone35-boot1.py "$SOCK" "$DUMP" || exit 1
kill $QEMU_PID 2>/dev/null || true
QEMU_PID=""

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
fi

echo "--- boot 2 (no disk: a paint press on a full desktop, the far window hashed, the passes reckoned) ---"
python3 proofs/stone35-boot2.py "$SOCK" "$DUMP" || exit 1

echo "PASS"
