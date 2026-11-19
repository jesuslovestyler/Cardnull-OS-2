#!/bin/sh
# Stone 39 proof: the bar shows the open windows —
# GUI completeness II, in the ladder planned
# November 18, 2026. The bottom bar (the glass face
# of Stone 33, with its round cardinal start button)
# carries one plain-words presence chip to each of
# the eight windows a person opens and closes —
# Files, Editor, Paint, Calculator, Verse, Help,
# Settings, Terminal, the names the desktop already
# uses, in the icons' order — the front window's
# chip white on the bar's blue, a window behind
# white on light gray, as their title bars stand.
# The chips are laid along the bar's upper row and,
# when it fills (at large print, whose bar is
# narrower), on its lower row's middle ground,
# clear of the bar's name and its clock; they track
# every opening and closing, and a press on a chip
# raises its window by the region road of Stones 34
# and 35.
#
# The shipped disc is booted at the BIOS door (the
# face of light), in four boots — on this bench a
# second pointer press after a feather-visit press
# is not reliable (Stone 35's note), so each boot
# makes at most one press, and the openings are
# made by typed words. Boot 1 (no disk): the chips
# at the rising and as 'files' and 'verse' open,
# and one press on the files chip raises the files
# window (its title bar's color and its chip's
# color both turn). Boot 2 (no disk, no press): six
# windows opened by their words, their seven chips
# standing with the terminal's, then Escape closes
# the front window and the chips pack again. Boot 3
# (no disk): the calculator opened last, covering
# the terminal at their shared first place, and one
# press on the terminal's chip raises the terminal.
# Boot 4 (a fitted keeping disk whose card carries
# the large size): the chips at large print, the
# terminal's chip on the lower row, the bar's name
# and clock whole beside it (proofs/stone39-boot1.py
# to stone39-boot4.py).
#
# One honest limit, recorded in the README: on the
# Stone 38 baseline, in this bench's present build,
# the help window and the calculator's opening
# visit together reset the machine, in either
# order — reproduced on a pristine Stone 38 tree
# with this toolchain. It is a latent fault of the
# baseline, not of this stone, and no boot here
# asks the two to stand together: the help window's
# chip is proved in boots 2 and 4, the calculator's
# in boot 3.
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

SOCK="$WORK/monitor.sock"
DUMP="$WORK/dump.ppm"

launch() {
    # $1 = disk image (may be empty)
    DRIVE=""
    if [ -n "$1" ]; then
        DRIVE="-drive file=$1,format=raw,if=ide,index=0"
    fi
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            $DRIVE \
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
            $DRIVE \
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
}

for n in 1 2 3; do
    launch ""
    echo "--- boot $n ---"
    python3 "proofs/stone39-boot$n.py" "$SOCK" "$DUMP" || exit 1
    kill $QEMU_PID 2>/dev/null || true
    QEMU_PID=""
    sleep 1
done

echo "--- laying the keeping disk: a card carrying the large size ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
img = bytearray(8 * 1024 * 1024)
# The settings card (sector 8): C, N, the offset byte
# 59 for Eastern, the chime byte 0, and the size byte
# 2 — large print stands chosen on the card.
img[8 * 512 + 0] = 67
img[8 * 512 + 1] = 78
img[8 * 512 + 2] = 59
img[8 * 512 + 3] = 0
img[8 * 512 + 4] = 2
with open(sys.argv[1], "wb") as f:
    f.write(img)
print("ok: the disk stands prepared with its large-size card")
PYEOF

launch "$WORK/disk.img"
echo "--- boot 4 (the large size: the chips large, the terminal's on the lower row) ---"
python3 proofs/stone39-boot4.py "$SOCK" "$DUMP" || exit 1
kill $QEMU_PID 2>/dev/null || true
QEMU_PID=""

echo "PASS"
