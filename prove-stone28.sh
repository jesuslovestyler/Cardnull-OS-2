#!/bin/sh
# Stone 28 proof: large print. The shipped disc is
# booted at the BIOS door (the face of light), four
# times:
#
#   Boot 1 (a fitted keeping disk whose settings card
#     is of the OLD shape — C, N, the offset byte 59 for
#     Eastern, the chime byte 0, and the size byte 0, as
#     every card laid before this stone carries): the
#     desktop rises at the usual size, the word
#     'settings' opens the window and its new third
#     choice is DECODED letter by letter against the
#     system's own letter shapes ("Words:", 'Usual size'
#     picked, 'Large' unpicked). A press of the pointer
#     on the Large row repaints the whole desktop at
#     the large size at once — the bar, the window's
#     title and choices, and the keeping word all
#     decoded letter by letter AT THE NEW SCALE
#     (twenty-four-pixel cells; the bar itself stands
#     twenty-four pixels tall where it stood sixteen).
#     The welcome window is DRAGGED at the large size
#     and decoded at its new place; a press on the
#     chime-off row at the large size stands the chime
#     off; and the typing line's echo and an answer are
#     decoded at the large size. Between the boots the
#     disk's own bytes are checked: the card must carry
#     the clicked choices — offset 59, chime byte 2,
#     size byte 2.
#   Boot 2 (the SAME disk): nothing is chosen again —
#     the desktop rises LARGE from the card, and the
#     window shows both choices as boot 1 left them. A
#     press on the 'Usual size' row at the large size
#     brings the usual size back at once, and the card
#     is checked again: the size byte stands 1 (usual),
#     the chime byte still 2.
#   Boot 3 (a FRESH old-shape disk): the desktop rises
#     at the usual size — a card with no size byte
#     chosen behaves exactly as it always has.
#   Boot 4 (no disk at all): the window says plainly
#     that the choices last only for this sitting, and
#     clicking 'Large' still stands the words large for
#     the sitting, the sitting-only words decoded at
#     the large size too.
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

lay_old_disk() {
    # $1 = the image to lay: the settings card of the
    # old shape (sector 8): C, N, the offset byte 59
    # for Eastern, the chime byte 0, and the size byte
    # 0 — no size ever chosen there.
    python3 - "$1" <<'PYEOF'
import sys
img = bytearray(8 * 1024 * 1024)
img[8 * 512 + 0] = 67
img[8 * 512 + 1] = 78
img[8 * 512 + 2] = 59
img[8 * 512 + 3] = 0
img[8 * 512 + 4] = 0
with open(sys.argv[1], "wb") as f:
    f.write(img)
print("ok: the disk stands prepared with its old-shape card")
PYEOF
}

boot() {
    # $1 = scenario, $2 = disk image ("" for none), $3 = socket tag
    SOCK="$WORK/monitor-$3.sock"
    DUMP="$WORK/dump-$3.ppm"
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        if [ -n "$2" ]; then
            $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
                -drive "file=$2,format=raw,if=ide,index=0" \
                -boot order=d -display none -m 4096 -nic none \
                -rtc base=2026-11-15T00:00:00 \
                -monitor "unix:$SOCK,server,nowait" &
        else
            $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
                -boot order=d -display none -m 4096 -nic none \
                -rtc base=2026-11-15T00:00:00 \
                -monitor "unix:$SOCK,server,nowait" &
        fi
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        if [ -n "$2" ]; then
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
        else
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
        fi
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

echo "--- laying the keeping disk: the settings card of the old shape ---"
lay_old_disk "$WORK/disk.img"

echo "--- boot 1 (the old-shape disk: choose large, drag, click, type — all at the new size) ---"
boot proofs/stone28-boot1.py "$WORK/disk.img" 1 || exit 1

echo "--- the disk's own bytes: the card carries the clicked choices ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
with open(sys.argv[1], "rb") as f:
    data = f.read()
card = data[8 * 512:8 * 512 + 5]
assert card[0] == 67 and card[1] == 78, "the card's letters stand on sector 8"
assert card[2] == 59, f"the offset byte is still Eastern 59 (found {card[2]})"
assert card[3] == 2, f"the chime byte stands off, 2 (found {card[3]})"
assert card[4] == 2, f"the size byte stands large, 2 (found {card[4]})"
print("ok: the settings card carries the clicked choices (offset 59, chime 2, size 2)")
PYEOF
[ $? -eq 0 ] || { echo "FAIL: the settings card does not carry the clicked choices"; exit 1; }

echo "--- boot 2 (the same disk: large print persisted; click back to usual) ---"
boot proofs/stone28-boot2.py "$WORK/disk.img" 2 || exit 1

echo "--- the disk's own bytes: the size byte now stands usual ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
with open(sys.argv[1], "rb") as f:
    data = f.read()
card = data[8 * 512:8 * 512 + 5]
assert card[2] == 59, f"the offset byte is still Eastern 59 (found {card[2]})"
assert card[3] == 2, f"the chime byte still stands off, 2 (found {card[3]})"
assert card[4] == 1, f"the size byte stands usual, 1 (found {card[4]})"
print("ok: the settings card carries the size byte back at usual (offset 59, chime 2, size 1)")
PYEOF
[ $? -eq 0 ] || { echo "FAIL: the settings card does not carry the restored size"; exit 1; }

echo "--- laying a fresh old-shape disk ---"
lay_old_disk "$WORK/disk3.img"

echo "--- boot 3 (the fresh old-shape disk: the usual size, as always) ---"
boot proofs/stone28-boot3.py "$WORK/disk3.img" 3 || exit 1

echo "--- boot 4 (no disk: the choice lasts only for this sitting, and still works) ---"
boot proofs/stone28-boot4.py "" 4 || exit 1

echo "PASS"
