#!/bin/sh
# Stone 22 proof: window dragging. The shipped disc is
# booted at the BIOS door (the face of light), once,
# with a fitted keeping disk prepared below with two
# known notes in the CNN3 store (the settings card on
# sector 8, the notes header on sector 64, one sector
# to a note from sector 65):
#
#   The word 'files' opens the files window at the
#   place its measures have always reckoned, and its
#   rendered list is DECODED letter by letter against
#   the system's own letter shapes
#   (proofs/stone22-boot1.py, through tools/pixels.py).
#   The pointer is laid on the window's title bar, the
#   button pressed, and the pointer carried — button
#   held, in small steps — to a new place; on release
#   the window renders THERE (title and list decoded at
#   the new coordinates), and every pixel of the ground
#   it stood on that neither its new place nor the
#   feather window behind it covers is plain desktop
#   again — no remnants, compared the way
#   prove-pointertrail.sh compares the whole desktop.
#   A press on a note's row in the dragged window picks
#   that note, its whole words standing at the window's
#   foot — the press reckoned from the same place the
#   painter painted — and a press on the close mark at
#   the dragged place closes the window.
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

echo "--- laying the keeping disk: two known notes in the CNN3 store ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
img = bytearray(8 * 1024 * 1024)
# The settings card (sector 8): C, N, and the offset
# byte — Eastern, 59 — so the disk stands as the
# system's own keeping disk at boot.
img[8 * 512 + 0] = 67
img[8 * 512 + 1] = 78
img[8 * 512 + 2] = 59
# The notes page: its header on sector 64 — C, N, N
# ("CNN3" with the count) — and one sector to a note.
notes = (b"remember the garden", b"pray for mother")
img[64 * 512 + 0] = 67
img[64 * 512 + 1] = 78
img[64 * 512 + 2] = 78
img[64 * 512 + 3] = len(notes)
for i, text in enumerate(notes):
    base = (65 + i) * 512
    img[base] = len(text)
    img[base + 1:base + 1 + len(text)] = text
with open(sys.argv[1], "wb") as f:
    f.write(img)
print("ok: the disk stands prepared with the two known notes")
PYEOF

boot() {
    # $1 = scenario, $2 = disk image, $3 = socket tag
    SOCK="$WORK/monitor-$3.sock"
    DUMP="$WORK/dump-$3.ppm"
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -drive "file=$2,format=raw,if=ide,index=0" \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
            -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -drive "file=$2,format=raw,if=ide,index=0" \
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
    python3 tools/pixels.py "$1" "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

echo "--- boot 1 (the keeping disk: drag the files window, click in it, close it) ---"
boot proofs/stone22-boot1.py "$WORK/disk.img" 1 || exit 1

echo "PASS"
