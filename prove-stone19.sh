#!/bin/sh
# Stone 19 proof: the files window. The shipped disc is
# booted at the BIOS door (the face of light), twice:
#
#   Boot 1 (a fitted keeping disk, prepared below with
#     three known notes in the CNN3 store — the settings
#     card on sector 8, the notes header "CNN3" on sector
#     64, one sector to a note from sector 65, the shape
#     prove-stone15.sh checks byte for byte): the word
#     'files' opens the window, and its rendered list is
#     DECODED letter by letter against the system's own
#     letter shapes (proofs/stone19-boot1.py, through
#     tools/pixels.py) and compared against the known
#     notes. The down arrow moves the pick; a press of
#     the pointer on an entry's row picks that one; the
#     picked note's whole words must stand at the
#     window's foot each time. Tab cycles through all
#     three windows, and Escape closes the files window
#     back to the desktop.
#   Boot 2 (no disk at all): the window says plainly
#     that there is no disk fitted and nothing is saved,
#     and shows no entry — nothing is invented.
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

echo "--- laying the keeping disk: three known notes in the CNN3 store ---"
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
notes = (b"remember the garden",
         b"call billy about the roof",
         b"pray for quinton")
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
print("ok: the disk stands prepared with the three known notes")
PYEOF

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

echo "--- boot 1 (the prepared keeping disk: list, pick, cycle, close) ---"
boot proofs/stone19-boot1.py "$WORK/disk.img" 1 || exit 1

echo "--- boot 2 (no disk: the window says so, plainly) ---"
boot proofs/stone19-boot2.py "" 2 || exit 1

echo "PASS"
