#!/bin/sh
# Stone 50 proof: make this computer a Cardinal — the
# files window's new last row installs the system from
# the running stick onto a hard disk inside the
# computer, and the machine afterwards boots as a
# Cardinal on its own. The bench shape for the
# installing boots is Stone 49's (the shipped disc at
# the BIOS door, a fitted keeping disk, a USB stick on
# the xHCI bus); the disk-alone boots carry nothing
# but the disk. Scratch stands under
# ~/workspace/os2-scratch, as the bench's /tmp is
# cleaned too eagerly for a long proof.
#
#   Boot 1 (a prepared disk — the Eastern card, two
#     notes, one of them named, and a kept picture —
#     and the shipped stick): the files window's new
#     last row carries "Make this computer a Cardinal"
#     (DECODED); a press opens the asking, "Not yet"
#     standing picked; a press on "Yes, make it a
#     Cardinal" runs the making, and the window answers
#     "This computer is a Cardinal now." The disk's own
#     bytes then prove the installing: its boot record
#     stands as the stick's own record with the table's
#     beginning set to 2048, the whole system image
#     stands at sector 2048 byte for byte the stick's,
#     the keeping's ground (the card, the notes page,
#     the picture) stands byte for byte as prepared,
#     and the stick's file stands untouched
#     (proofs/stone50-boot1.py).
#   Boot 2 (boot 1's disk ALONE — no disc, no stick):
#     the desktop rises from the disk itself; the files
#     window lists the two notes and the kept picture
#     that stood before the installing; a new note is
#     typed and kept on the disk's own boot
#     (proofs/stone50-boot2.py).
#   Boot 3 (the disk alone again): the note typed on
#     the disk's own boot stands in the list — keeping
#     written after the installing survives the disk's
#     reboot (proofs/stone50-boot3.py).
#   Boot 4 (the disc and the stick again, the installed
#     disk fitted): a second making is refused in plain
#     words — "This disk already carries a Cardinal." —
#     and the disk's bytes stand byte for byte as they
#     stood before the boot: nothing overwritten
#     (proofs/stone50-boot4.py).
#   Boot 5 (no hard disk fitted; the stick stands): the
#     making is answered "No hard disk stands in this
#     computer." (proofs/stone50-boot5.py).
#   Boot 6 (a prepared disk; NO stick on the bus): the
#     making is answered "No stick stands in this
#     computer.", and the disk's bytes stand as
#     prepared — no record laid, no image copied
#     (proofs/stone50-boot6.py).
#   Boot 7 (a prepared disk; a keeping stick — its card
#     and notes, no system on it): the making is
#     answered "The stick does not carry Cardnull.",
#     and the disk stands as prepared
#     (proofs/stone50-boot7.py).
#   Boot 8 (the shipped stick ALONE, Stone 17's own
#     shape and scenario): the stick still boots the
#     system whole, exactly as before — the installing
#     is an addition, not a replacement.
#
# Prints PASS or FAIL.

set -u
cd "$(dirname "$0")"

WORK="$HOME/workspace/os2-scratch/stone50-proof"
rm -rf "$WORK"
mkdir -p "$WORK"
QEMU_PID=""
cleanup() {
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
}
trap cleanup EXIT

echo "--- building the shipped disc and stick ---"
./build-stick.sh >/dev/null || { echo "FAIL: build-stick.sh failed"; exit 1; }
cp dist/cardnull-stick.img "$WORK/stick.img"
STICK_SHA_BEFORE=$(sha256sum "$WORK/stick.img" | cut -d' ' -f1)

echo "--- laying the keeping disk: the Eastern card, two notes (one named), a kept picture ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
img = bytearray(32 * 1024 * 1024)
# The settings card (sector 8): C, N, and the offset
# byte — Eastern, 59 — so the disk stands as the
# system's own keeping disk at boot.
img[8 * 512 + 0] = 67
img[8 * 512 + 1] = 78
img[8 * 512 + 2] = 59
# The notes page: its header on sector 64, the first
# note at sector 65 standing under its own words, and
# the second at sector 66 carrying a name in its
# slot's tail (Stone 40).
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
# The kept picture: its header on sector 80 (a picture
# kept, the chosen-color figure '2', and its name in
# the header's spare bytes, Stone 40), and its body —
# the canvas ground throughout (a space on light gray,
# attribute 112) with one red cell at the block's
# row 5, column 10 (attribute 64: red ground).
pname = b"kept picture"
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
print("ok: the disk stands prepared with its card, its two notes, and its picture")
PYEOF
cp "$WORK/disk.img" "$WORK/disk-prepared.bin"

run_qemu() {
    # $1 = the monitor socket tag; the rest is the
    # machine's shape, in the caller's words below.
    SOCK="$WORK/monitor-$1.sock"
    DUMP="$WORK/dump-$1.ppm"
    shift
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU "$@" \
            -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        # shellcheck disable=SC2086
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
            "$@" \
            -display none -m 4096 -nic none \
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
}

boot_cd() {
    # $1 = scenario, $2 = socket tag, $3 = "disk" or
    # "nodisk", $4 = "stick", "stickless", or
    # "keepstick" (the keeping stick laid below).
    DISKARGS=""
    if [ "$3" = "disk" ]; then
        DISKARGS="-drive file=$WORK/disk.img,format=raw,if=ide,index=0"
    fi
    STICKARGS="-device qemu-xhci -device usb-kbd"
    if [ "$4" = "stick" ]; then
        STICKARGS="$STICKARGS -device usb-storage,drive=stickd -drive if=none,id=stickd,file=$WORK/stick.img,format=raw"
    elif [ "$4" = "keepstick" ]; then
        STICKARGS="$STICKARGS -device usb-storage,drive=stickd -drive if=none,id=stickd,file=$WORK/keepstick.img,format=raw"
    fi
    # shellcheck disable=SC2086
    run_qemu "$2" -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
        $DISKARGS $STICKARGS -boot order=d
    python3 tools/pixels.py "$1" "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

boot_disk_alone() {
    # $1 = scenario, $2 = socket tag: the installed
    # disk, and nothing else in the machine.
    run_qemu "$2" -drive "file=$WORK/disk.img,format=raw,if=ide,index=0" -boot order=c
    python3 tools/pixels.py "$1" "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

echo "--- boot 1 (the making: install from the stick onto the prepared disk) ---"
boot_cd proofs/stone50-boot1.py 1 disk stick || exit 1

echo "--- the disk's own bytes after boot 1: the record, the image, the keeping untouched ---"
python3 - "$WORK/disk.img" "$WORK/stick.img" "$WORK/disk-prepared.bin" <<'PYEOF' || exit 1
import sys
disk = open(sys.argv[1], "rb").read()
stick = open(sys.argv[2], "rb").read()
prep = open(sys.argv[3], "rb").read()
fails = []
def expect(cond, label):
    print(("ok: " if cond else "NOT OK: ") + label)
    if not cond:
        fails.append(label)
def sector(data, n):
    return data[n * 512:(n + 1) * 512]
imglen = len(stick) // 512
rec = sector(disk, 0)
srec = sector(stick, 0)
expect(rec[510] == 85 and rec[511] == 170,
       "the disk's boot record carries the boot signature")
expect(int.from_bytes(rec[454:458], "little") == 2048,
       "the record's table names sector 2048 as the image's beginning")
expect(rec[:454] == srec[:454] and rec[458:] == srec[458:],
       "the record stands byte for byte the stick's own, apart from the beginning it names")
expect(disk[2048 * 512:(2048 + imglen) * 512] == stick,
       "the whole system image stands on the disk at sector 2048, byte for byte the stick's")
for n in [8] + list(range(64, 73)) + list(range(80, 84)):
    expect(sector(disk, n) == sector(prep, n),
           f"keeping sector {n} stands byte for byte as prepared")
if fails:
    print(f"FAIL ({len(fails)} check(s) failed)")
    sys.exit(1)
print("PASS")
PYEOF
STICK_SHA_AFTER=$(sha256sum "$WORK/stick.img" | cut -d' ' -f1)
if [ "$STICK_SHA_BEFORE" = "$STICK_SHA_AFTER" ]; then
    echo "ok: the stick's file stands untouched — the installing only read it"
else
    echo "NOT OK: the stick was written while the system was installed from it"
    exit 1
fi

echo "--- boot 2 (the installed disk ALONE: the desktop rises, the keeping stands, a new note is kept) ---"
boot_disk_alone proofs/stone50-boot2.py 2 || exit 1

echo "--- boot 3 (the disk alone again: the new note survived the reboot) ---"
boot_disk_alone proofs/stone50-boot3.py 3 || exit 1

cp "$WORK/disk.img" "$WORK/disk-before-boot4.bin"

echo "--- boot 4 (a second making over an existing Cardinal: refused plainly, nothing overwritten) ---"
boot_cd proofs/stone50-boot4.py 4 disk stick || exit 1
if cmp -s "$WORK/disk.img" "$WORK/disk-before-boot4.bin"; then
    echo "ok: the disk's bytes stand byte for byte as before boot 4 — the refusal overwrote nothing"
else
    echo "NOT OK: the disk changed under a refused second making"
    exit 1
fi

echo "--- boot 5 (no hard disk fitted: the making answered plainly) ---"
boot_cd proofs/stone50-boot5.py 5 nodisk stick || exit 1

echo "--- boot 6 (no stick on the bus: the making answered plainly; the disk untouched) ---"
cp "$WORK/disk-prepared.bin" "$WORK/disk.img"
boot_cd proofs/stone50-boot6.py 6 disk stickless || exit 1
if cmp -s "$WORK/disk.img" "$WORK/disk-prepared.bin"; then
    echo "ok: the disk stands byte for byte as prepared — no record laid, no image copied"
else
    echo "NOT OK: the disk changed under a making that had no stick to copy from"
    exit 1
fi

echo "--- laying a keeping stick for boot 7: its card and two notes, no system ---"
python3 - "$WORK/keepstick.img" <<'PYEOF'
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
print("ok: the keeping stick stands prepared")
PYEOF

echo "--- boot 7 (a stick that does not carry Cardnull: the making answered plainly) ---"
boot_cd proofs/stone50-boot7.py 7 disk keepstick || exit 1
if cmp -s "$WORK/disk.img" "$WORK/disk-prepared.bin"; then
    echo "ok: the disk stands byte for byte as prepared — nothing was copied from a stick with no system"
else
    echo "NOT OK: the disk changed under a making from a stick that carries no system"
    exit 1
fi

echo "--- boot 8 (the shipped stick ALONE, Stone 17's shape: the stick still boots whole) ---"
run_qemu 8 -drive "if=none,id=usbstick,file=$WORK/stick.img,format=raw" \
    -device usb-storage,drive=usbstick -usb -boot order=c
python3 tools/pixels.py proofs/stone9-boot1.py "$SOCK" "$DUMP" || exit 1
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""

echo "PASS"
