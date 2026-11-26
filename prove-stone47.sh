#!/bin/sh
# Stone 47 proof: the drag heal — the second
# diagnosis's four repaint roads, healed at their
# roots. The shipped disc is booted at the BIOS door
# (the face of light):
#
#   Boot 1 (no disk): the terminal-drag census. The
#   terminal is dragged up five rows and dropped: its
#   answers and its typing line stand inside its new
#   place, nothing spilled below its foot, and the
#   drag back down restores the first place's rows
#   (proofs/stone47-boot1.py).
#
#   Boot 2 (no disk): the icon labels keep their
#   paper. The Files and Settings name bands are read
#   at the rising — the ground's black dominant, no
#   blue — then the word 'hello' is typed and the
#   terminal dragged up two rows and dropped (the
#   second diagnosis's frame B5 sequence), and the
#   bands are read again, unchanged
#   (proofs/stone47-boot2.py).
#
#   Boot 3 (no disk): the ground's invitation is
#   whole. The welcome window is dragged down across
#   both invitation lines and back, and dropped; then
#   a fresh press in the paint window's cells runs a
#   region road crossing both lines; after each, both
#   lines read whole again (proofs/stone47-boot3.py).
#
#   Boot 4 (no disk): a press visit writes only in
#   its own window. A held paint stroke and a
#   calculator key press are sampled frame by frame:
#   the band around the window never changes, the
#   window's title never leaves, the stroke lands and
#   the sum reckons (proofs/stone47-boot4.py).
#
#   Boot 5 (a keeping disk standing empty): the files
#   window's list is paid at the stroke's end. A
#   stroke is painted with the files window open
#   below: mid-stroke the list still shows no picture
#   row, though the keeping has saved the picture;
#   when the button is let go, the row stands
#   (proofs/stone47-boot5.py).
#
# The disk for boot 5 stands prepared by this script:
# the settings card on sector 8 (C, N, and the offset
# byte 59, Eastern), the notes header on sector 64
# (C, N, N, count 0), and the picture header on
# sector 80 (C, N, P, the kept byte 0, the
# chosen-color figure 48).
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

boot_nodisk() {
    # $1 = scenario file, $2 = tag
    SOCK="$WORK/monitor-$2.sock"
    DUMP="$WORK/dump-$2.ppm"
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
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
        QEMU_PID=$!
    else
        echo "FAIL: no QEMU found (looked for ~/qemu10-root; set QEMU to a qemu-system-x86_64 command)" >&2
        exit 1
    fi
    python3 "$1" "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

boot_disk() {
    # $1 = scenario file, $2 = disk image, $3 = tag
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
    python3 "$1" "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

echo "--- boot 1 (no disk: the terminal-drag census) ---"
boot_nodisk proofs/stone47-boot1.py 1 || exit 1

echo "--- boot 2 (no disk: the icon labels keep their paper) ---"
boot_nodisk proofs/stone47-boot2.py 2 || exit 1

echo "--- boot 3 (no disk: the ground's invitation is whole) ---"
boot_nodisk proofs/stone47-boot3.py 3 || exit 1

echo "--- boot 4 (no disk: a press visit writes only in its own window) ---"
boot_nodisk proofs/stone47-boot4.py 4 || exit 1

echo "--- the keeping disk for boot 5, standing empty ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
img = bytearray(8 * 1024 * 1024)
# The settings card (sector 8): C, N, and the offset
# byte — Eastern, 59 — so the disk stands as the
# system's own keeping disk at boot.
img[8 * 512 + 0] = 67
img[8 * 512 + 1] = 78
img[8 * 512 + 2] = 59
# The notes page's header (sector 64): C, N, N, and
# a count of none.
img[64 * 512 + 0] = 67
img[64 * 512 + 1] = 78
img[64 * 512 + 2] = 78
img[64 * 512 + 3] = 0
# The picture's header (sector 80): C, N, P, the
# kept byte 0 — no picture stands kept — and the
# chosen-color figure 48.
img[80 * 512 + 0] = 67
img[80 * 512 + 1] = 78
img[80 * 512 + 2] = 80
img[80 * 512 + 3] = 0
img[80 * 512 + 4] = 48
with open(sys.argv[1], "wb") as f:
    f.write(img)
print("ok: the disk stands prepared, empty")
PYEOF

echo "--- boot 5 (the keeping disk: the list is paid at the stroke's end) ---"
boot_disk proofs/stone47-boot5.py "$WORK/disk.img" 5 || exit 1

echo "PASS"
