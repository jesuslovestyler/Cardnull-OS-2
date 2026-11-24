#!/bin/sh
# Stone 40 proof: names in the files window — a kept
# note renamed, a kept note copied under a new name,
# and the kept picture renamed, in plain words on the
# window itself. The shipped disc is booted at the
# BIOS door (the face of light), two times:
#
#   Boot 1 (a fitted keeping disk, prepared below with
#     three known notes in the CNN3 store and one kept
#     picture in the CNP store — the settings card on
#     sector 8, the notes header on sector 64, one
#     sector to a note from sector 65, the picture
#     header on sector 80 and its bytes on sectors 81
#     to 83): in the files window, "Rename" and "Copy"
#     stand at the foot beside "Let this note go" —
#     DECODED letter by letter against the system's own
#     letter shapes (proofs/stone40-boot1.py, through
#     tools/pixels.py). A press on "Rename" opens the
#     naming way; Enter on an empty name is refused in
#     plain words in the window, and a name that
#     already stands ("pray for quinton", the third
#     note's own words) is refused the same way, with
#     nothing changed — Escape then puts the naming
#     away and the list stands as it was. Renamed to
#     "garden notes", the first note stands under its
#     new name in the list with its words whole at the
#     foot. A press on "Copy" and the name "garden
#     copy" lay a second keeping on the page, picked,
#     its words the first note's whole words; the
#     first note is then let go through Stone 27's
#     asking, and the copy still stands whole — picked
#     afterwards, its words stand at the foot. The
#     kept picture is renamed to "garden picture" the
#     same way. Between the boots the disk's own bytes
#     are checked: the CNN3 header counts three notes
#     (the copy standing in the let-go note's place's
#     stead as the page's third, on its own sector,
#     carrying its name in its slot's tail and the
#     first note's words whole; the wiped fourth
#     sector; the refused and renamed names nowhere
#     left behind), and the CNP header carries the
#     picture's name in its spare bytes with the
#     picture's own bytes untouched.
#   Boot 2 (the same disk, a fresh boot): the files
#     window lists the copy under its name and the
#     picture under its name, the copy's words stand
#     whole at the foot, and the editor lists the
#     copy's words on the page — the names and the
#     copy truly went through the stores.
#
# The picture is renamed but never copied, and the
# proof asks for no copy of it: the disk's picture
# store holds one picture (sectors 80 to 83, one
# header), and a copy would need a second picture's
# place that does not stand there — the honest limit
# the README's Stone 40 section records.
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

echo "--- laying the keeping disk: three known notes and one kept picture ---"
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
# The kept picture: its header on sector 80 — C, N, P,
# the kept byte 1, the chosen-color figure 48 ('0') —
# and its bytes on sectors 81 to 83, a known pattern
# across the painted region's 1144 bytes.
img[80 * 512 + 0] = 67
img[80 * 512 + 1] = 78
img[80 * 512 + 2] = 80
img[80 * 512 + 3] = 1
img[80 * 512 + 4] = 48
for i in range(1144):
    img[81 * 512 + i] = (i * 7 + 3) % 256
with open(sys.argv[1], "wb") as f:
    f.write(img)
print("ok: the disk stands prepared with the three known notes and the kept picture")
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

echo "--- boot 1 (rename refused twice, rename, copy, let the first go, rename the picture) ---"
boot proofs/stone40-boot1.py "$WORK/disk.img" 1 || exit 1

echo "--- the disk's own bytes: the stores carry the names and the copy ---"
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
assert head[3] == 3, f"the header counts three notes (found {head[3]})"
def slot(i):
    base = (65 + i) * 512
    return data[base:base + 64]
def textof(s):
    return s[1:1 + s[0]]
def nameof(s):
    return s[45:45 + s[44]] if s[44] else b""
assert textof(slot(0)) == b"call billy about the roof" and nameof(slot(0)) == b"", \
    f"the second note stands first now, unnamed (found {textof(slot(0))!r} / {nameof(slot(0))!r})"
assert textof(slot(1)) == b"pray for quinton" and nameof(slot(1)) == b"", \
    f"the third note stands second, unnamed (found {textof(slot(1))!r} / {nameof(slot(1))!r})"
assert textof(slot(2)) == b"remember the garden", \
    f"the copy carries the first note's words whole (found {textof(slot(2))!r})"
assert nameof(slot(2)) == b"garden copy", \
    f"the copy carries its name in its own slot's tail (found {nameof(slot(2))!r})"
base = 68 * 512
assert data[base:base + 64] == bytes(64), \
    "sector 68 is wiped — the page's fourth place was let go with the old count"
assert b"garden notes" not in data[65 * 512:69 * 512], \
    "the renamed-then-let-go note's name is nowhere left on the page"
phead = data[80 * 512:80 * 512 + 20]
assert phead[0] == 67 and phead[1] == 78 and phead[2] == 80, \
    "the picture header's letters stand on sector 80"
assert phead[3] == 1, "the picture still stands kept"
assert phead[4] == 48, "the picture's chosen-color figure stands as it was"
assert phead[5] == len(b"garden picture") and phead[6:20] == b"garden picture", \
    f"the picture's name stands in its header's spare bytes (found {phead[5:20]!r})"
pic = data[81 * 512:81 * 512 + 1144]
assert pic == bytes((i * 7 + 3) % 256 for i in range(1144)), \
    "the picture's own bytes are untouched by its renaming"
print("ok: the CNN3 store counts three notes — the copy on its own sector, named, whole — and the CNP header carries the picture's name with the picture untouched")
PYEOF
[ $? -eq 0 ] || { echo "FAIL: the stores do not carry the naming"; exit 1; }

echo "--- boot 2 (a fresh boot on the same disk: the names and the copy survived) ---"
boot proofs/stone40-boot2.py "$WORK/disk.img" 2 || exit 1

echo "PASS"
