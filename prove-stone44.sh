#!/bin/sh
# Stone 44 proof: a second screen. The shipped disc
# is booted at the BIOS door (the face of light) two
# times:
#
#   Boot 1 (a second display adapter fitted, QEMU's
#     -device secondary-vga,id=vga2; the bench's clock
#     pinned to a known morning): the main desktop
#     stands untouched, and the second head — read
#     through the monitor's screendump for that device
#     (tools/pixels.py's dump2, added for this stone) —
#     stands at 1024 by 768 wearing the companion
#     page, every line decoded against the system's
#     own letter shapes (proofs/stone44-boot1.py):
#     the name, the day and date in plain words, the
#     clock's face, and the Psalm 127 lines. When the
#     minute turns, the page is painted again.
#   Boot 2 (no second adapter): the desktop stands
#     exactly as before, and there is no second head
#     to read (proofs/stone44-boot2.py).
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
    # $1 = scenario, $2 = socket tag, $3.. = extra QEMU arguments
    SCEN="$1"
    SOCK="$WORK/monitor-$2.sock"
    DUMP="$WORK/dump-$2.ppm"
    shift 2
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-24T12:00:00 \
            -monitor "unix:$SOCK,server,nowait" "$@" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
            -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-24T12:00:00 \
            -monitor "unix:$SOCK,server,nowait" \
            -L "$HOME/qemu10-root/usr/share/qemu" \
            -L "$HOME/qemu10-root/usr/share/seabios" \
            "$@" >/dev/null 2>&1 &
        QEMU_PID=$!
    else
        echo "FAIL: no QEMU found (looked for ~/qemu10-root; set QEMU to a qemu-system-x86_64 command)" >&2
        exit 1
    fi
    python3 tools/pixels.py "$SCEN" "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

echo "--- boot 1 (a second adapter fitted: the companion page stands, and turns with the minute) ---"
boot proofs/stone44-boot1.py one -device secondary-vga,id=vga2 || exit 1

echo "--- boot 2 (no second adapter: the desktop as before, no second head) ---"
boot proofs/stone44-boot2.py two || exit 1

echo "PASS"
