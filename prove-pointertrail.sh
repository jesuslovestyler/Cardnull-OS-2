#!/bin/sh
# Pointer-trail proof: the pointer is dragged across
# the desktop, and afterwards the desktop must stand
# exactly as it stood before. The shipped disc is
# booted at the BIOS door (the face of light), a
# reference picture is taken with the arrow at the
# screen's middle, the bench's mouse carries the arrow
# through wide moves and a small-step drag and home
# again (proofs/pointertrail-boot1.py, through
# tools/pixels.py), and the final picture must agree
# with the reference at every pixel but the bottom
# bar's clock ground (the bar stands at the foot since
# Stone 33) — the bar's clock being the one honest
# difference time makes.
#
# This proof stands because the earlier pointer proof
# could not see the fault it watches for: the arrow's
# white edge paints one row below the sixteen-by-
# sixteen square the pointer's save kept (at y + 16),
# that row was never saved or laid back, and every
# place the arrow had stood kept five white pixels of
# it — the dotted trail Tyler witnessed dragging the
# pointer in UTM (November 15, 2026). Stone 13's proof
# checked the square the arrow left, sixteen rows of
# it, and passed; the trail stood in the seventeenth
# row. Comparing the whole desktop leaves no row out.
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
python3 tools/pixels.py proofs/pointertrail-boot1.py "$SOCK" "$DUMP" || exit 1

echo "PASS"
