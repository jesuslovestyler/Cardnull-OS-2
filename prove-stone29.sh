#!/bin/sh
# Stone 29 proof: the verse window. The shipped disc
# is booted at the BIOS door (the face of light),
# twice, with no disk fitted, the bench clock pinned
# at 2026-11-15T00:00:00 on the world's standard time
# — with the disc's Eastern choice, the date the
# desktop shows is November 14, 2026, whose day count
# around the kept set of twelve verses stands at the
# twelfth verse, 1 John 5:13:
#
#   Boot 1 (the usual size): the word 'verse' opens
#     the window; the verse standing in it is DECODED
#     letter by letter against the system's own letter
#     shapes (proofs/stone29-boot1.py, through
#     tools/pixels.py) and joins back into its exact
#     World English Bible wording, its reference under
#     it. Tab brings the welcome window forward, the
#     word brings the verse window forward again,
#     Escape closes it; the bar's menu — its seven
#     choices decoded, Verse among them, Rest last —
#     opens it by a press on the Verse choice, and a
#     press on its close mark closes it.
#   Boot 2 (the large size): the settings window's
#     Large row is pressed, Escape closes it, and the
#     word opens the verse window on the narrow large
#     face, the same verse whole in it, wrapped at the
#     narrower width, decoded letter by letter at the
#     large scale; Escape closes it.
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
    # $1 = scenario, $2 = socket tag
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
    python3 tools/pixels.py "$1" "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

echo "--- boot 1 (no disk: the verse window by its word, the menu, and the close mark) ---"
boot proofs/stone29-boot1.py 1 || exit 1

echo "--- boot 2 (no disk: the verse window at the large size) ---"
boot proofs/stone29-boot2.py 2 || exit 1

echo "PASS"
