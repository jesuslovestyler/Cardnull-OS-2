#!/bin/sh
# Stone 48 proof: the picture window — the kept
# picture standing open big in a window of its own.
# The shipped disc is booted at the BIOS door (the
# face of light):
#
#   Boot 1 (a keeping disk prepared below with the
#     settings card and one known note, as Stone 26's
#     proof prepares): the word 'paint' opens the
#     paint feather and the bench's mouse draws a Red
#     cell and a Blue cell, as Stone 26's proof draws
#     them, so a picture stands kept; the word 'files'
#     lists it; the down arrow picks it, and the
#     window's foot carries the new word "Look at it"
#     beside "Rename" (DECODED); a press on "Look at
#     it" opens the picture window forward, its title
#     decoded, and the picture itself standing in it —
#     the Red cell's block, the Blue cell's block, and
#     an untouched cell's ground, each sampled in the
#     window's own big measure (sixteen pixels wide,
#     thirty-two tall, to a cell). A press on its
#     close mark closes it (proofs/stone48-boot1.py,
#     through tools/pixels.py).
#   Boot 2 (no disk fitted): the word 'picture' opens
#     the window with no picture kept — its body's
#     plain lines decoded, saying so and how one
#     comes to stand there. The bar's menu — risen
#     one row higher for its fourteen choices, all
#     decoded, Picture the thirteenth choice and Rest
#     last — is read; and with the files window
#     forward the picture window's bar stands gray
#     until a press on its chip on the bar raises it,
#     its bar blue again (proofs/stone48-boot2.py).
#   Boot 3 (boot 1's disk again, the picture standing
#     kept on it): the word 'picture' opens the
#     window on the picture the disk alone kept
#     through the reboot — the same cells standing —
#     and the window is dragged by its title bar
#     three cells right and two rows up: the picture
#     follows whole to the new place, and a press on
#     the close mark at the new place closes it
#     (proofs/stone48-boot3.py). The bench's emulated
#     PS/2 mouse has refused held drags before, on
#     unmodified trees as readily as on new ones
#     (Stones 45 and 47 record it); if it refuses
#     here, this boot's drag checks fail on the bench
#     and the stone's record says so plainly — the
#     drag is Tyler's to witness in UTM, as every
#     drag has been.
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

echo "--- laying the keeping disk: the Eastern card and one known note ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
img = bytearray(8 * 1024 * 1024)
# The settings card (sector 8): C, N, and the offset
# byte — Eastern, 59 — so the disk stands as the
# system's own keeping disk at boot.
img[8 * 512 + 0] = 67
img[8 * 512 + 1] = 78
img[8 * 512 + 2] = 59
# The notes page: its header on sector 64 and the one
# known note at sector 65.
note = b"remember the garden"
img[64 * 512 + 0] = 67
img[64 * 512 + 1] = 78
img[64 * 512 + 2] = 78
img[64 * 512 + 3] = 1
img[65 * 512] = len(note)
img[65 * 512 + 1:65 * 512 + 1 + len(note)] = note
with open(sys.argv[1], "wb") as f:
    f.write(img)
print("ok: the disk stands prepared with its card and its note")
PYEOF

boot() {
    # $1 = scenario, $2 = socket tag, $3 = "disk" or "nodisk"
    SOCK="$WORK/monitor-$2.sock"
    DUMP="$WORK/dump-$2.ppm"
    DISKARGS=""
    if [ "$3" = "disk" ]; then
        DISKARGS="-drive file=$WORK/disk.img,format=raw,if=ide,index=0"
    fi
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            $DISKARGS \
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
            $DISKARGS \
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

echo "--- boot 1 (draw and keep, Files' new word, the window and its picture) ---"
boot proofs/stone48-boot1.py 1 disk || exit 1

echo "--- boot 2 (no disk: the word 'picture', the empty window's words, the menu, the chip) ---"
boot proofs/stone48-boot2.py 2 nodisk || exit 1

echo "--- boot 3 (the kept picture across a reboot, and the drag) ---"
boot proofs/stone48-boot3.py 3 disk || exit 1

echo "PASS"
