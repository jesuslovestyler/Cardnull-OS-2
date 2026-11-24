#!/bin/sh
# Stone 34 proof: the region repaint — the first of the
# four glitches Tyler witnessed in UTM (Nov 16, 2026),
# "when i move windows it flickers the windows," fixed
# at its root. The shipped disc is booted at the BIOS
# door (the face of light), no disk fitted:
#
#   The files and verse windows stand open low on the
#   desktop and the welcome window high. The welcome
#   window is dragged by its title bar, six small
#   steps right, across empty desktop: after every
#   step — the button still held — the whole populated
#   desktop below must hash exactly as before the drag
#   (no repaint writes a bystander, at any instant;
#   the wash-and-redraw of bystanders was the flicker),
#   and after the drop the dragged window's body must
#   stand whole — a census of its interior and all
#   five of its lines decoding (Stone 45's
#   body-always-lands check, added when this proof was
#   restored: its loop-pass counter read a compiler
#   cell, __guard_passes, that the compiler no longer
#   lays in the kernel, and the per-step hash now
#   checks directly what the counter stood for). Then
#   the files window is dragged across the verse
#   window and back: the crossed window stands
#   repainted in its behind colors under the drag's
#   road, the vacated ground stands plain, and both
#   windows decode whole at the end
#   (proofs/stone34-boot1.py).
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

echo "--- boot 1 (no disk: a drag across one window, the far window untouched, the passes reckoned) ---"
python3 proofs/stone34-boot1.py "$SOCK" "$DUMP" || exit 1

echo "PASS"
