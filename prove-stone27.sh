#!/bin/sh
# Stone 27 proof: letting a note go. The shipped disc
# is booted at the BIOS door (the face of light), three
# times:
#
#   Boot 1 (a fitted keeping disk, prepared below with
#     three known notes in the CNN3 store — the settings
#     card on sector 8, the notes header on sector 64,
#     one sector to a note from sector 65): in the files
#     window, a press on "Let this note go" opens the
#     asking — "Let this note go for good?", the note's
#     words, "Yes, let it go", "Keep it" standing picked
#     — DECODED letter by letter against the system's
#     own letter shapes (proofs/stone27-boot1.py, through
#     tools/pixels.py). The cancel paths are proven: a
#     press on "Keep it" and Escape after Enter each
#     leave the note whole. Enter, up, Enter then lets
#     the first note go; in the editor window the third
#     note is picked, its asking opened by a press, and
#     a press on the yes lets it go. Between the boots
#     the disk's own bytes are checked: the CNN3 header
#     counts one note, its sector carries the remaining
#     note whole, and the two let-go notes' sectors are
#     wiped — the removal truly went through the store.
#   Boot 2 (the same disk, a fresh boot): the files
#     window and the editor window both list the one
#     remaining note and neither let-go one.
#   Boot 3 (no disk at all): two notes are kept for the
#     sitting by the word 'note'; the files window lists
#     them under their honest heading, and the second is
#     let go by keyboard with the same asking — a
#     session-only note is removable too.
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

echo "--- boot 1 (ask, cancel twice, let go in Files, let go in Editor) ---"
boot proofs/stone27-boot1.py "$WORK/disk.img" 1 || exit 1

echo "--- the disk's own bytes: the store carries the letting go ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
with open(sys.argv[1], "rb") as f:
    data = f.read()
card = data[8 * 512:8 * 512 + 3]
assert card[0] == 67 and card[1] == 78 and card[2] == 59, \
    "the settings card still stands on sector 8"
head = data[64 * 512:64 * 512 + 4]
assert head[0] == 67 and head[1] == 78 and head[2] == 78, \
    "the notes header's letters stand on sector 64"
assert head[3] == 1, f"the header counts one note (found {head[3]})"
def note(i):
    base = (65 + i) * 512
    n = data[base]
    return data[base + 1:base + 1 + n]
assert note(0) == b"call billy about the roof", \
    f"the remaining note stands whole, first on the page (found {note(0)!r})"
for i in (1, 2):
    base = (65 + i) * 512
    assert data[base:base + 64] == bytes(64), \
        f"sector {65 + i} is wiped — a let-go note no longer reads as kept"
print("ok: the CNN3 store counts one note, whole, and the let-go sectors are wiped")
PYEOF
[ $? -eq 0 ] || { echo "FAIL: the CNN3 store does not carry the letting go"; exit 1; }

echo "--- boot 2 (a fresh boot on the same disk: the removals survived) ---"
boot proofs/stone27-boot2.py "$WORK/disk.img" 2 || exit 1

echo "--- boot 3 (no disk: a sitting's note let go, with the same asking) ---"
boot proofs/stone27-boot3.py "" 3 || exit 1

echo "PASS"
