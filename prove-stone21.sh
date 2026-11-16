#!/bin/sh
# Stone 21 proof: the editor window. The shipped disc
# is booted at the BIOS door (the face of light), twice:
#
#   Boot 1 (a fitted keeping disk, prepared below with
#     one known note in the CNN3 store — the settings
#     card on sector 8, the notes header on sector 64,
#     one sector to a note from sector 65): the word
#     'editor' opens the window, and its rendered list
#     is DECODED letter by letter against the system's
#     own letter shapes (proofs/stone21-boot1.py, through
#     tools/pixels.py). A press of the pointer picks the
#     kept note; Enter opens the writing way over its
#     whole words; Escape closes the window untouched. A
#     new note is typed with the desktop's own typing and
#     kept by Enter; forty-six letters typed at a fresh
#     note stop at the measure of forty-three the window
#     names, and that draft is thrown away by Escape.
#     The kept note is then changed in the window — its
#     last word rubbed out, another typed — and kept
#     back to the same place; the files window, opened
#     between, lists the same notes from the same store;
#     Tab brings the editor forward among the five
#     windows and Escape closes it. Between the boots
#     the disk's own bytes are checked: the CNN3 header
#     counts two notes, the first stands as it was laid,
#     and the second carries the changed words — the
#     window truly wrote through the store.
#   Boot 2 (no disk at all): both of the window's ways
#     say plainly that a note is kept only for this
#     sitting; a note written and kept in the window
#     stands in its list, and in the reckoning of the
#     word 'notes' besides.
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

echo "--- laying the keeping disk: one known note in the CNN3 store ---"
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
notes = (b"remember the garden",)
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
print("ok: the disk stands prepared with the one known note")
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

echo "--- boot 1 (the keeping disk: pick, write, change, share the store) ---"
boot proofs/stone21-boot1.py "$WORK/disk.img" 1 || exit 1

echo "--- the disk's own bytes: the window wrote through the CNN3 store ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
with open(sys.argv[1], "rb") as f:
    data = f.read()
head = data[64 * 512:64 * 512 + 4]
assert head[0] == 67 and head[1] == 78 and head[2] == 78, \
    "the notes header's letters stand on sector 64"
assert head[3] == 2, f"the header counts two notes (found {head[3]})"
def note(i):
    base = (65 + i) * 512
    n = data[base]
    return data[base + 1:base + 1 + n]
assert note(0) == b"remember the garden", \
    f"the first note stands as it was laid (found {note(0)!r})"
assert note(1) == b"pray for father", \
    f"the second note carries the changed words (found {note(1)!r})"
print("ok: the CNN3 store carries both notes, the second with its changed words")
PYEOF
[ $? -eq 0 ] || { echo "FAIL: the CNN3 store does not carry the window's keeping"; exit 1; }

echo "--- boot 2 (no disk: the sitting-only words, honestly said) ---"
boot proofs/stone21-boot2.py "" 2 || exit 1

echo "PASS"
