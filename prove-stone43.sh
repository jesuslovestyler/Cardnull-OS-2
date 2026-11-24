#!/bin/sh
# Stone 43 proof: the USB stick in the running system.
# The bench's QEMU is launched in prove-stone32.sh's own
# shape (tools/launch.sh takes no USB devices), with an
# xHCI controller carrying a USB keyboard and a USB
# mass-storage device backed by a raw image — and no
# hard disk at all, unless a boot says otherwise:
#
#   Boot 1 (a blank stick, no hard disk): the stick is
#     offered in plain words at the rising, the 'usb'
#     word reports it with its sector count (and the
#     keyboard on the same bus still stands ready), the
#     setup gate's yes gives it the keeping, and two
#     notes are kept on it — the stick image's own bytes
#     then prove the card and the notes page stand on
#     the stick, in diskkeep's layout.
#   Boot 2 (the same stick, booted again): the notes
#     are read back from the stick at the rising, and a
#     third note joins them; the image's bytes prove
#     the page grew.
#   Boot 3 (no stick): the 'usb' word names no stick,
#     and nothing is offered.
#   Boot 4 (a blank stick AND a blank hard disk): the
#     hard disk keeps its place — it is offered, not
#     the stick — and the stick's image stands
#     byte-identical after, never written.
#
# Prints PASS or FAIL.

set -u
cd "$(dirname "$0")"

./build.sh >/dev/null || { echo "FAIL: build.sh failed"; exit 1; }

WORK=$(mktemp -d)
QEMU_PID=""
cleanup() {
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    rm -rf "$WORK"
}
trap cleanup EXIT

python3 - "$WORK" <<'PYEOF'
import sys
work = sys.argv[1]
for name in ("stick.img", "disk.img"):
    with open(work + "/" + name, "wb") as f:
        f.write(bytes(8 * 1024 * 1024))
print("A blank 8 MB stick image and a blank 8 MB disk image laid.")
PYEOF
STICK4_BEFORE=$(sha256sum "$WORK/stick.img" | cut -d' ' -f1)

boot() {
    # $1 = the monitor socket, $2.. = extra QEMU arguments.
    SOCK="$1"
    shift
    "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
        --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
        "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
        -kernel build/cardnull.elf -display none -m 128 -nic none \
        -initrd build/settings.bin,build/welcome.feather \
        -monitor "unix:$SOCK,server,nowait" \
        -L "$HOME/qemu10-root/usr/share/qemu" \
        -L "$HOME/qemu10-root/usr/share/seabios" \
        -pidfile "$WORK/qemu.pid" -daemonize "$@"
    QEMU_PID=$(cat "$WORK/qemu.pid")
}

stop() {
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
}

STICKARGS="-device qemu-xhci -device usb-kbd -device usb-storage,drive=stickd -drive if=none,id=stickd,file=$WORK/stick.img,format=raw"

echo "--- boot 1 (blank stick, no hard disk: gate, yes, two notes kept on the stick) ---"
# Word splitting is intended: the stick's device arguments.
# shellcheck disable=SC2086
boot "$WORK/monitor1.sock" $STICKARGS
python3 tools/screen.py proofs/stone43-boot1.py "$WORK/monitor1.sock" || exit 1
stop

echo "--- the stick's own bytes after boot 1: the card and the notes page ---"
python3 - "$WORK/stick.img" <<'PYEOF' || exit 1
import sys
data = open(sys.argv[1], "rb").read()
def sector(n):
    return data[n * 512:(n + 1) * 512]
fails = []
def expect(cond, label):
    print(("ok: " if cond else "NOT OK: ") + label)
    if not cond:
        fails.append(label)
card = sector(8)
expect(card[0] == 67 and card[1] == 78, "the settings card stands on the stick's sector 8")
expect(card[2] == 59, "the card carries the settings' offset byte (59), as the disk road writes it")
head = sector(64)
expect(head[0] == 67 and head[1] == 78 and head[2] == 78, "the notes header stands on the stick's sector 64")
expect(head[3] == 2, "the header keeps two notes")
n1 = sector(65)
expect(n1[0] == 19 and n1[1:20] == b"remember the garden", "the first note stands on the stick")
n2 = sector(66)
expect(n2[0] == 25 and n2[1:26] == b"call billy about the roof", "the second note stands on the stick")
if fails:
    print(f"FAIL ({len(fails)} check(s) failed)")
    sys.exit(1)
print("PASS")
PYEOF

echo "--- boot 2 (the same stick: the notes read back, a third kept) ---"
# shellcheck disable=SC2086
boot "$WORK/monitor2.sock" $STICKARGS
python3 tools/screen.py proofs/stone43-boot2.py "$WORK/monitor2.sock" || exit 1
stop

echo "--- the stick's own bytes after boot 2: three notes ---"
python3 - "$WORK/stick.img" <<'PYEOF' || exit 1
import sys
data = open(sys.argv[1], "rb").read()
def sector(n):
    return data[n * 512:(n + 1) * 512]
fails = []
def expect(cond, label):
    print(("ok: " if cond else "NOT OK: ") + label)
    if not cond:
        fails.append(label)
head = sector(64)
expect(head[3] == 3, "the header now keeps three notes")
n3 = sector(67)
expect(n3[0] == 16 and n3[1:17] == b"pray for quinton", "the third note stands on the stick")
if fails:
    print(f"FAIL ({len(fails)} check(s) failed)")
    sys.exit(1)
print("PASS")
PYEOF

echo "--- boot 3 (no stick: nothing offered, no stick named) ---"
boot "$WORK/monitor3.sock" -device qemu-xhci -device usb-kbd
python3 tools/screen.py proofs/stone43-boot3.py "$WORK/monitor3.sock" || exit 1
stop

echo "--- boot 4 (blank stick AND blank hard disk: the disk keeps its place) ---"
# A fresh stick image, so this boot's stick stands blank
# as boot 1's did.
python3 - "$WORK" <<'PYEOF'
import sys
with open(sys.argv[1] + "/stick.img", "wb") as f:
    f.write(bytes(8 * 1024 * 1024))
print("The stick image laid blank again for boot 4.")
PYEOF
STICK4_BEFORE=$(sha256sum "$WORK/stick.img" | cut -d' ' -f1)
# shellcheck disable=SC2086
boot "$WORK/monitor4.sock" $STICKARGS -drive file="$WORK/disk.img",format=raw,if=ide
python3 tools/screen.py proofs/stone43-boot4.py "$WORK/monitor4.sock" || exit 1
stop
STICK4_AFTER=$(sha256sum "$WORK/stick.img" | cut -d' ' -f1)
if [ "$STICK4_BEFORE" = "$STICK4_AFTER" ]; then
    echo "ok: the stick's bytes stand untouched — the hard disk kept its place"
else
    echo "NOT OK: the stick was written though a hard disk stands fitted"
    exit 1
fi
python3 - "$WORK/disk.img" <<'PYEOF' || exit 1
import sys
data = open(sys.argv[1], "rb").read()
card = data[8 * 512:9 * 512]
if card[0] == 67 and card[1] == 78:
    print("ok: the settings card stands on the hard disk, as it always has")
else:
    print("NOT OK: the hard disk carries no card after the gate's yes")
    sys.exit(1)
print("PASS")
PYEOF
