#!/bin/sh
# Stone 42 proof: the Shield showing itself — the
# feather door's guard, at work since Stone 5 in the
# dark, standing in a window of its own with its
# reckoning since the rising. The shipped disc is
# booted at the BIOS door (the face of light), two
# times, with no disk fitted:
#
#   Boot 1: the tenth desktop icon (a blue shield with
#     a gold cross); the word 'shield' opens the
#     window and every one of its plain lines is
#     DECODED against the system's own letter shapes
#     (proofs/stone42-boot1.py, through
#     tools/pixels.py) — what the Shield does, the
#     reckoning at none and none, and its two standing
#     truths. Escape closes it; a press on its icon
#     opens it again; a press on its close mark closes
#     it; the bar's menu — risen one row higher for
#     its eleven choices, decoded, Shield the tenth
#     window choice and Rest last — opens it by a
#     press on the Shield choice; a press on its chip
#     on the bar raises it from behind the files
#     window; and after a feather's visit stands, the
#     window's reckoning has moved to one let in.
#   Boot 2: a disc whose welcome feather has been
#     tampered with (one byte of its program turned
#     after its card was written, the disc proof's own
#     tampering) — the word 'feather' asks, the door
#     turns the feather away, no visit stands, and the
#     Shield window's reckoning tells it: none let in,
#     one turned away (proofs/stone42-boot2.py).
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
    # $1 = scenario, $2 = socket tag, $3 = the disc image
    SOCK="$WORK/monitor-$2.sock"
    DUMP="$WORK/dump-$2.ppm"
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=$3,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -boot order=d -display none -m 4096 -nic none \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
            -drive "file=$3,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -boot order=d -display none -m 4096 -nic none \
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

echo "--- boot 1 (the icon, the word 'shield', the window's lines, the menu, the chip, and the reckoning of a visit) ---"
boot proofs/stone42-boot1.py 1 dist/cardnull-os-2.iso || exit 1

echo "--- building the tampered-feather disc ---"
python3 - "$WORK" <<'PYEOF' || { echo "FAIL: tampered feather build failed"; exit 1; }
import sys
work = sys.argv[1]
feather = bytearray(open("build/welcome.feather", "rb").read())
start = feather.index(b"\n\n") + 2
feather[start + 100] ^= 0xFF
open(work + "/feather-tampered.feather", "wb").write(feather)
PYEOF
ISO_OUT="$WORK/cardnull-tampered.iso" FEATHER_FILE="$WORK/feather-tampered.feather" ./build-iso.sh >/dev/null || { echo "FAIL: variant build failed"; exit 1; }

echo "--- boot 2 (the tampered feather, turned away, and the Shield's reckoning of it) ---"
boot proofs/stone42-boot2.py 2 "$WORK/cardnull-tampered.iso" || exit 1

echo "PASS"
