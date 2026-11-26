#!/bin/sh
# Stone 49 proof: the stick and disk exchange — the
# files window copies a picked kept thing between the
# keeping disk and a plugged-in USB stick, in both
# directions, in plain words. The shipped disc is
# booted at the BIOS door (the face of light), with a
# fitted keeping disk and a USB stick on the xHCI bus
# (Stone 43's bench shape, carried to the disc's own
# boot as Stone 48's proof boots it):
#
#   Boot 1 (a prepared disk — the Eastern card, two
#     notes, one of them named — and a BLANK stick):
#     the files window's last row carries "To the
#     stick" and "From the stick" while a note stands
#     picked (DECODED); a press on "To the stick"
#     copies the first note and is answered "Copied to
#     the stick." in the window; the second note
#     follows; a picture is painted and kept the bench's
#     way (Stone 26's drawing) and copied likewise;
#     and the refusals stand in plain words — the
#     picture copied again ("A picture already stands
#     on the stick.") and the first note copied again
#     ("That name already stands on the stick."). The
#     stick's own bytes then prove the copies: its
#     notes page holds the disk's two slots entire,
#     name tail and all, and its picture sectors stand
#     byte for byte the disk's — while the disk's notes
#     page stands byte for byte as it was laid, the
#     source untouched (proofs/stone49-boot1.py).
#   Boot 2 (boot 1's disk again; the stick now
#     prepared with a page of its own — one note
#     standing under the second note's name with other
#     words, and a kept picture of its own with its
#     own name): "From the stick" on the second note
#     is answered "Brought in from the stick." and the
#     note's words at the window's foot are the stick's
#     words now; "From the stick" on the picture
#     brings the stick's picture in, and it stands in
#     the picture window in its big measure, at its
#     own cell, where the disk's red cell stood ground
#     again; and "From the stick" on the first note is
#     refused — "The stick holds no note of that
#     name." The disk's bytes then prove what was
#     brought in stands on the disk, and the stick's
#     image stands byte-identical across the boot —
#     bringing in never writes the source
#     (proofs/stone49-boot2.py).
#   Boot 3 (boot 1's disk, NO stick on the bus): both
#     exchange presses are answered in the window —
#     "No stick stands in this computer."
#     (proofs/stone49-boot3.py).
#   Boot 4 (NO hard disk; a prepared stick carrying
#     its card and two notes, so the stick is itself
#     the keeping, Stone 43's road): both exchange
#     presses are answered in the window — "The stick
#     is this computer's keeping."
#     (proofs/stone49-boot4.py).
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

echo "--- laying the keeping disk: the Eastern card and two notes, one named ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
img = bytearray(8 * 1024 * 1024)
# The settings card (sector 8): C, N, and the offset
# byte — Eastern, 59 — so the disk stands as the
# system's own keeping disk at boot.
img[8 * 512 + 0] = 67
img[8 * 512 + 1] = 78
img[8 * 512 + 2] = 59
# The notes page: its header on sector 64, the first
# note at sector 65 standing under its own words, and
# the second at sector 66 carrying a name in its
# slot's tail (Stone 40: the name's length at the
# slot's forty-fifth byte, its letters after it).
a = b"remember the garden"
b = b"call billy about the roof"
name = b"roof note"
img[64 * 512 + 0] = 67
img[64 * 512 + 1] = 78
img[64 * 512 + 2] = 78
img[64 * 512 + 3] = 2
img[65 * 512] = len(a)
img[65 * 512 + 1:65 * 512 + 1 + len(a)] = a
img[66 * 512] = len(b)
img[66 * 512 + 1:66 * 512 + 1 + len(b)] = b
img[66 * 512 + 44] = len(name)
img[66 * 512 + 45:66 * 512 + 45 + len(name)] = name
with open(sys.argv[1], "wb") as f:
    f.write(img)
print("ok: the disk stands prepared with its card and its two notes")
PYEOF
# A copy of the disk's notes ground as laid, for the
# source-untouched check after boot 1.
python3 - "$WORK/disk.img" "$WORK/disk-notes-before.bin" <<'PYEOF'
import sys
data = open(sys.argv[1], "rb").read()
with open(sys.argv[2], "wb") as f:
    f.write(data[64 * 512:67 * 512])
print("ok: the disk's notes ground kept aside for the untouched check")
PYEOF

echo "--- laying a blank stick ---"
python3 - "$WORK/stick.img" <<'PYEOF'
import sys
with open(sys.argv[1], "wb") as f:
    f.write(bytes(8 * 1024 * 1024))
print("ok: the stick stands blank")
PYEOF

boot() {
    # $1 = scenario, $2 = socket tag, $3 = "disk" or
    # "nodisk", $4 = "stick", "stickless", or
    # "stickonly" (boot 4: the stick, and no hard disk).
    SOCK="$WORK/monitor-$2.sock"
    DUMP="$WORK/dump-$2.ppm"
    DISKARGS=""
    if [ "$3" = "disk" ]; then
        DISKARGS="-drive file=$WORK/disk.img,format=raw,if=ide,index=0"
    fi
    STICKARGS="-device qemu-xhci -device usb-kbd"
    if [ "$4" != "stickless" ]; then
        STICKARGS="$STICKARGS -device usb-storage,drive=stickd -drive if=none,id=stickd,file=$WORK/stick.img,format=raw"
    fi
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            $DISKARGS $STICKARGS \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        # shellcheck disable=SC2086
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
            -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            $DISKARGS $STICKARGS \
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

echo "--- boot 1 (two notes and a painted picture copied to a blank stick; the refusals) ---"
boot proofs/stone49-boot1.py 1 disk stick || exit 1

echo "--- the stick's own bytes after boot 1: the copies stand there; the disk's notes untouched ---"
python3 - "$WORK/stick.img" "$WORK/disk.img" "$WORK/disk-notes-before.bin" <<'PYEOF' || exit 1
import sys
stick = open(sys.argv[1], "rb").read()
disk = open(sys.argv[2], "rb").read()
before = open(sys.argv[3], "rb").read()
fails = []
def expect(cond, label):
    print(("ok: " if cond else "NOT OK: ") + label)
    if not cond:
        fails.append(label)
def sector(data, n):
    return data[n * 512:(n + 1) * 512]
head = sector(stick, 64)
expect(head[0] == 67 and head[1] == 78 and head[2] == 78,
       "the notes header stands on the stick's sector 64")
expect(head[3] == 2, "the stick's page keeps two notes now")
expect(sector(stick, 65)[:64] == sector(disk, 65)[:64],
       "the first note's slot stands on the stick, byte for byte the disk's")
expect(sector(stick, 66)[:64] == sector(disk, 66)[:64],
       "the second note's slot stands on the stick, its name in its tail")
pic = sector(stick, 80)
expect(pic[0] == 67 and pic[1] == 78 and pic[2] == 80 and pic[3] == 1,
       "the picture's header stands on the stick, a picture kept")
expect(all(sector(stick, 81 + s) == sector(disk, 81 + s) for s in range(3)),
       "the picture's three sectors stand on the stick, byte for byte the disk's")
expect(disk[64 * 512:67 * 512] == before,
       "the disk's notes ground stands byte for byte as laid — the source untouched")
if fails:
    print(f"FAIL ({len(fails)} check(s) failed)")
    sys.exit(1)
print("PASS")
PYEOF

echo "--- preparing the stick's own keeping for boot 2 ---"
python3 - "$WORK/stick.img" <<'PYEOF'
import sys
img = bytearray(8 * 1024 * 1024)
# The stick's notes page: one note standing under the
# name "roof note" — the disk's second note's name —
# with other words, as a twin kept on another machine
# would stand.
words = b"the roof is fixed now"
name = b"roof note"
img[64 * 512 + 0] = 67
img[64 * 512 + 1] = 78
img[64 * 512 + 2] = 78
img[64 * 512 + 3] = 1
img[65 * 512] = len(words)
img[65 * 512 + 1:65 * 512 + 1 + len(words)] = words
img[65 * 512 + 44] = len(name)
img[65 * 512 + 45:65 * 512 + 45 + len(name)] = name
# The stick's kept picture: its header (a picture
# kept, the chosen-color figure '2', and its name in
# the header's spare bytes, Stone 40), and its body —
# the canvas ground throughout (a space on light
# gray, attribute 112) with one red cell at the
# block's row 5, column 10 (attribute 64: red ground),
# a place the disk's picture leaves ground.
pname = b"stick picture"
img[80 * 512 + 0] = 67
img[80 * 512 + 1] = 78
img[80 * 512 + 2] = 80
img[80 * 512 + 3] = 1
img[80 * 512 + 4] = 50
img[80 * 512 + 5] = len(pname)
img[80 * 512 + 6:80 * 512 + 6 + len(pname)] = pname
body = bytearray()
for i in range(1144 // 2):
    body += bytes((32, 112))
off = (5 * 52 + 10) * 2
body[off] = 32
body[off + 1] = 64
for s in range(3):
    chunk = bytes(body[s * 512:(s + 1) * 512])
    img[(81 + s) * 512:(81 + s) * 512 + len(chunk)] = chunk
with open(sys.argv[1], "wb") as f:
    f.write(img)
print("ok: the stick stands prepared with its own note and picture")
PYEOF
STICK2_BEFORE=$(sha256sum "$WORK/stick.img" | cut -d' ' -f1)

echo "--- boot 2 (the stick's note and picture brought in; the name the stick does not hold) ---"
boot proofs/stone49-boot2.py 2 disk stick || exit 1

echo "--- the disk's bytes after boot 2: what was brought in stands there; the stick untouched ---"
STICK2_AFTER=$(sha256sum "$WORK/stick.img" | cut -d' ' -f1)
if [ "$STICK2_BEFORE" = "$STICK2_AFTER" ]; then
    echo "ok: the stick's bytes stand untouched — bringing in never writes the source"
else
    echo "NOT OK: the stick was written while things were brought in from it"
    exit 1
fi
python3 - "$WORK/disk.img" "$WORK/stick.img" <<'PYEOF' || exit 1
import sys
disk = open(sys.argv[1], "rb").read()
stick = open(sys.argv[2], "rb").read()
fails = []
def expect(cond, label):
    print(("ok: " if cond else "NOT OK: ") + label)
    if not cond:
        fails.append(label)
def sector(data, n):
    return data[n * 512:(n + 1) * 512]
expect(sector(disk, 66)[:64] == sector(stick, 65)[:64],
       "the brought-in note's slot stands on the disk, byte for byte the stick's")
expect(all(sector(disk, 81 + s) == sector(stick, 81 + s) for s in range(3)),
       "the brought-in picture's sectors stand on the disk, byte for byte the stick's")
head = sector(disk, 80)
expect(head[0] == 67 and head[1] == 78 and head[2] == 80 and head[3] == 1,
       "the disk's picture header stands, a picture kept")
expect(head[5] == 13 and head[6:19] == b"stick picture",
       "the brought-in picture's name stands in the disk's header")
if fails:
    print(f"FAIL ({len(fails)} check(s) failed)")
    sys.exit(1)
print("PASS")
PYEOF

echo "--- boot 3 (no stick on the bus: both presses answered plainly) ---"
boot proofs/stone49-boot3.py 3 disk stickless || exit 1

echo "--- preparing a keeper stick for boot 4: its card and two notes ---"
python3 - "$WORK/stick.img" <<'PYEOF'
import sys
img = bytearray(8 * 1024 * 1024)
img[8 * 512 + 0] = 67
img[8 * 512 + 1] = 78
img[8 * 512 + 2] = 59
a = b"water the greenhouse"
b = b"feed the bluegill"
img[64 * 512 + 0] = 67
img[64 * 512 + 1] = 78
img[64 * 512 + 2] = 78
img[64 * 512 + 3] = 2
img[65 * 512] = len(a)
img[65 * 512 + 1:65 * 512 + 1 + len(a)] = a
img[66 * 512] = len(b)
img[66 * 512 + 1:66 * 512 + 1 + len(b)] = b
with open(sys.argv[1], "wb") as f:
    f.write(img)
print("ok: the stick stands prepared as a keeping stick")
PYEOF

echo "--- boot 4 (the stick is itself the keeping: both presses answered plainly) ---"
boot proofs/stone49-boot4.py 4 nodisk stickonly || exit 1

echo "PASS"
