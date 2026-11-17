#!/bin/sh
# Stone 33 proof: the glass face. The shipped disc is
# booted at the BIOS door (the face of light), twice:
#
#   Boot 1 (no disk fitted, the usual size): the bar
#     stands at the screen's foot, two rows tall, its
#     sheen bands and tint sampled pixel by pixel, and
#     the round start button at its left carries the
#     cardinal — its deep red, gold wing, orange beak,
#     lead divisions, and white eye checked in the
#     bird's own shape (proofs/stone33-boot1.py, through
#     tools/pixels.py). A press on the button opens the
#     menu RISEN from it — its nine choices DECODED
#     letter by letter, Rest last — and a press on the
#     Files choice opens the files window at its new
#     first place above the bar. The windows' glass is
#     checked: a rounded corner's missing pixel is the
#     desktop's, the soft shadow stands along a window's
#     right edge and under its foot where the glass
#     shape promises (and is clipped at the bar's top).
#     The files window is dragged by its title bar and
#     decoded at its new place, the ground it vacated —
#     its shadow's reach with it — plain again; its
#     close mark closes it. The pointer is then carried
#     across the glass — over the bar, the button, and
#     a window's shadow — and home, and the whole
#     desktop must stand pixel for pixel as it was. Rest
#     is opened from the risen menu and its panel
#     decoded; Stay puts it away; Escape dismisses the
#     menu and closes nothing.
#   Boot 2 (a fitted keeping disk whose card carries
#     the size byte 2): the desktop rises at large
#     print, the bar and its button standing large at
#     the foot — the cardinal checked on the large
#     button — the menu rises there too, its nine
#     choices decoded at the large scale, and the Files
#     choice opens the files window at its large first
#     place above the bar.
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

boot() {
    # $1 = scenario, $2 = disk image (may be empty),
    # $3 = socket tag
    SOCK="$WORK/monitor-$3.sock"
    DUMP="$WORK/dump-$3.ppm"
    DRIVE=""
    if [ -n "$2" ]; then
        DRIVE="-drive file=$2,format=raw,if=ide,index=0"
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
    python3 tools/pixels.py "$1" "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

echo "--- boot 1 (no disk: the glass bar, the button's cardinal, the risen menu, a dragged glass window, the pointer's discipline, Rest) ---"
boot proofs/stone33-boot1.py "" 1 || exit 1

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

echo "--- boot 2 (the large size: the glass bar and button large, the menu risen large, the files window above the bar) ---"
boot proofs/stone33-boot2.py "$WORK/disk.img" 2 || exit 1

echo "PASS"
