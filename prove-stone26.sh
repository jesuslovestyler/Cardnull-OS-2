#!/bin/sh
# Stone 26 proof: paint keeps its pictures. The shipped
# disc is booted at the BIOS door (the face of light),
# twice, on ONE keeping disk prepared below with the
# settings card on sector 8 (C, N, and the offset byte
# 59 for Eastern) and one known note in the CNN3 store
# (the header on sector 64, the note at sector 65 —
# the shape prove-stone15.sh checks byte for byte):
#
#   Boot 1 (draw and keep): the word 'paint' opens the
#     paint feather (Stone 24); the bench's PS/2 mouse
#     draws on the real pointer road — a Red cell, the
#     Blue swatch, a Blue cell — and the word 'files'
#     lists the kept picture beside the known note
#     ("A picture you painted", DECODED letter by
#     letter); a press on the picture's row opens it
#     again in the paint window (proofs/stone26-boot1.py,
#     through tools/pixels.py).
#   The disk's own bytes are then read: the picture
#     store's header stands on sector 80 (C, N, P, kept,
#     and the chosen-color figure for Blue), and the
#     painted region on sectors 81 to 83 carries the
#     two drawn cells' color bytes and an untouched
#     cell's canvas ground — the picture truly stands
#     on the disk, and the settings card and the notes
#     page stand unharmed beside it.
#   Boot 2 (the picture survived): the same disk is
#     booted again; 'files' lists the note and the
#     picture before anything has drawn; the down arrow
#     picks the picture, and Enter opens it in the
#     paint window with its cells decoded back against
#     what was drawn — Red, Blue, the untouched ground,
#     and "Color: Blue" with its star (proofs/
#     stone26-boot2.py).
#
# The keeping is the host's, as the stone is built: the
# feather is checked at the door on every visit exactly
# as always (runfeather reckons its card first), and
# the host — which already holds the painted cells
# between visits — writes them through. No static
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
./build-iso.sh >/dev/null || { echo "FAIL: build-iso.sh failed"; exit 1; }

echo "--- laying the keeping disk: the Eastern card and one known note ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
img = bytearray(8 * 1024 * 1024)
# The settings card (sector 8): C, N, and the offset
# byte — Eastern, 59 — so the disk stands as the
# system's own keeping disk at boot.
img[8 * 512 + 0] = 67
img[8 * 512 + 1] = 78
img[8 * 512 + 2] = 59
# The notes page: its header on sector 64 and the one
# known note at sector 65.
note = b"remember the garden"
img[64 * 512 + 0] = 67
img[64 * 512 + 1] = 78
img[64 * 512 + 2] = 78
img[64 * 512 + 3] = 1
img[65 * 512] = len(note)
img[65 * 512 + 1:65 * 512 + 1 + len(note)] = note
with open(sys.argv[1], "wb") as f:
    f.write(img)
print("ok: the disk stands prepared with its card and its note")
PYEOF

boot() {
    # $1 = scenario, $2 = socket tag
    SOCK="$WORK/monitor-$2.sock"
    DUMP="$WORK/dump-$2.ppm"
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -drive "file=$WORK/disk.img,format=raw,if=ide,index=0" \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
            -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -drive "file=$WORK/disk.img,format=raw,if=ide,index=0" \
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

echo "--- boot 1 (draw in Paint, see it listed in Files, open it by its row) ---"
boot proofs/stone26-boot1.py 1 || exit 1

echo "--- the disk's own bytes: the picture store stands, its neighbours unharmed ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
with open(sys.argv[1], "rb") as f:
    data = f.read()
head = data[80 * 512:80 * 512 + 5]
assert head[0] == 67 and head[1] == 78 and head[2] == 80, \
    "the picture header's letters C, N, P stand on sector 80"
assert head[3] == 1, f"the header says a picture stands kept (found {head[3]})"
assert head[4] == 50, \
    f"the header carries the chosen-color figure for Blue, '2' (found {head[4]})"

def cellattr(row, col):
    # The painted region (rows 10 to 20, columns 14 to
    # 65) laid row by row from sector 81: a letter byte
    # and a color byte to a cell.
    off = ((row - 10) * 52 + (col - 14)) * 2
    return data[81 * 512 + off], data[81 * 512 + off + 1]

letter, attr = cellattr(16, 30)
assert letter == 32 and attr == 68, \
    f"the Red cell stands in the region (letter {letter}, color {attr}; want 32, 68)"
letter, attr = cellattr(15, 20)
assert letter == 32 and attr == 17, \
    f"the Blue cell stands in the region (letter {letter}, color {attr}; want 32, 17)"
letter, attr = cellattr(18, 40)
assert attr == 119, \
    f"an untouched cell stands on the canvas ground (color {attr}; want 119)"
card = data[8 * 512:8 * 512 + 3]
assert card[0] == 67 and card[1] == 78 and card[2] == 59, \
    "the settings card still stands on sector 8"
nhead = data[64 * 512:64 * 512 + 4]
assert nhead[0] == 67 and nhead[1] == 78 and nhead[2] == 78 and nhead[3] == 1, \
    "the CNN3 header still counts its one note on sector 64"
print("ok: the picture store carries the drawing, and its neighbours stand")
PYEOF
[ $? -eq 0 ] || { echo "FAIL: the kept picture does not stand on the disk as drawn"; exit 1; }

echo "--- boot 2 (a fresh boot on the same disk: the picture survived, Files opens it) ---"
boot proofs/stone26-boot2.py 2 || exit 1

echo "PASS"
