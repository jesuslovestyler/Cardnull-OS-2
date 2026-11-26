#!/bin/sh
# Mend proof (found by Stone 49): the carried-press
# road reaches the paint feather only while the
# paint window stands forward. Stone 49's
# verification found the road's old shape — any
# press landing inside the paint window's shown
# region was carried to the feather whenever the
# window stood open and visited, whichever window
# stood forward — corrupting the stone's picture
# exchange: the files window's exchange press, made
# with the files window forward and the paint
# window open behind, painted a cell and re-kept
# the canvas over the exchange's own work. The
# shipped disc is booted at the BIOS door (the face
# of light), twice, on two keeping disks laid byte
# for byte the same (the Eastern card and two
# notes, as Stone 49's proof lays them), with the
# xHCI keyboard the bench's stick shape carries and
# NO stick on the bus:
#
#   Boot 1 (the press): a picture is painted and
#     kept the bench's way (Stone 26's drawing: a
#     Red cell and a Blue cell) — carried presses
#     with the paint window forward, painting as
#     they must — and the files window picks the
#     picture, the paint window standing open
#     behind it; then the exchange press of Stone
#     49's first boot is made at the same point of
#     the screen, and the files window answers it
#     alone, in plain words: "No stick stands in
#     this computer." (proofs/mend49-boot1.py).
#   Boot 2 (the control): every step the same, and
#     the exchange press never made
#     (proofs/mend49-boot2.py).
#
# After the boots, the two disks' picture keepings
# — the header sector and the body's three sectors
# — are compared byte for byte. Under the road's
# old shape the press boot's keeping differed from
# the control's by the carried cell and its
# re-keeping (Stone 49's first boot failed by
# exactly one such byte); under the mend they must
# stand identical, and the header must show a
# picture truly kept, so the comparison is not
# empty.
#
# The boots wait long for the desktop (a 20s
# unwatched settle, then a 300s watch, in the
# scenarios): on this bench, under load, the
# harness's own watching — a screendump and a
# full-frame count at every poll — can starve the
# very rise it waits for. In this proof's first
# runs, boots watched from the first second timed
# out at 150s and again at 300s, while the same
# scenarios run alone, and a hand-sampled rise,
# stood drawn in seconds. The settle and the long
# wait are patience, not weaker checks: the
# desktop must still stand drawn, blue and all,
# before anything else is believed, and every
# later check stands exactly as written.
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

echo "--- laying two keeping disks, byte for byte the same: the Eastern card and two notes ---"
for D in a b; do
python3 - "$WORK/disk-$D.img" <<'PYEOF'
import sys
img = bytearray(8 * 1024 * 1024)
# The settings card (sector 8): C, N, and the offset
# byte — Eastern, 59 — so the disk stands as the
# system's own keeping disk at boot.
img[8 * 512 + 0] = 67
img[8 * 512 + 1] = 78
img[8 * 512 + 2] = 59
# The notes page, as Stone 49's proof lays it: its
# header on sector 64, the first note at sector 65
# standing under its own words, and the second at
# sector 66 carrying a name in its slot's tail.
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
print("ok: a disk stands prepared with its card and its two notes")
PYEOF
done

boot() {
    # $1 = scenario, $2 = socket tag, $3 = disk image.
    SOCK="$WORK/monitor-$2.sock"
    DUMP="$WORK/dump-$2.ppm"
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -drive "file=$3,format=raw,if=ide,index=0" \
            -device qemu-xhci -device usb-kbd \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
            -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -drive "file=$3,format=raw,if=ide,index=0" \
            -device qemu-xhci -device usb-kbd \
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

echo "--- boot 1 (the picture painted and picked; the exchange press, files forward) ---"
boot proofs/mend49-boot1.py 1 "$WORK/disk-a.img" || exit 1

echo "--- boot 2 (the control: every step the same, the press never made) ---"
sleep 5
boot proofs/mend49-boot2.py 2 "$WORK/disk-b.img" || exit 1

echo "--- the two disks' picture keepings, compared byte for byte ---"
python3 - "$WORK/disk-a.img" "$WORK/disk-b.img" <<'PYEOF' || exit 1
import sys
press = open(sys.argv[1], "rb").read()
control = open(sys.argv[2], "rb").read()
fails = []
def expect(cond, label):
    print(("ok: " if cond else "NOT OK: ") + label)
    if not cond:
        fails.append(label)
def sector(data, n):
    return data[n * 512:(n + 1) * 512]
head = sector(control, 80)
expect(head[0] == 67 and head[1] == 78 and head[2] == 80 and head[3] == 1,
       "the control disk's picture header stands, a picture kept — the comparison is not empty")
body = b"".join(sector(control, 81 + s) for s in range(3))
ground = bytes((32, 112)) * (len(body) // 2)
expect(body != ground,
       "the control disk's picture body holds the painting, not the untouched ground")
expect(sector(press, 80) == head,
       "the press boot's picture header stands byte for byte the control's")
expect(all(sector(press, 81 + s) == sector(control, 81 + s) for s in range(3)),
       "the press boot's picture body stands byte for byte the control's — the press laid no cell and re-kept nothing")
if fails:
    print(f"FAIL ({len(fails)} check(s) failed)")
    sys.exit(1)
print("PASS")
PYEOF

echo "PASS"
