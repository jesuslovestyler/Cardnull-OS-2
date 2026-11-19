#!/bin/sh
# Stone 38 proof: the desktop itself — Tyler's word
# (Nov 18, 2026): "make a real desktop gui like
# windows 7 or Mac OS for cardnull instead of being
# in shell at start up I want a desktop for this
# computer." The boot arrives at the graphical
# desktop, as it has since the face of light rose —
# but the console that stood on the desktop's ground
# (the typing line below the windows, its answers
# strip above it) lives in a window of its own now:
# the terminal, the tenth window, standing open from
# the rising, its answers kept in a block of cells so
# any repaint lays them again. And the desktop
# carries its windows' icons down its left edge —
# Files, Editor, Paint, Calculator, Verse, Help,
# Settings, Terminal, each with its plain name — and
# a press on an icon opens its window, exactly as
# the icon's typed word and the menu's choice open
# it. The terminal closes by its close mark like any
# window, and the first key of a typed line raises
# it again.
#
# The shipped disc is booted at the BIOS door (the
# face of light), no disk fitted, in four boots — on
# this bench a second pointer press after a
# feather-visit press is not reliable (Stone 35's
# note), so each boot makes at most one press. Boot
# 1: the icons and the open terminal stand at the
# rising, and the Files icon is pressed. Boot 2: the
# Calculator icon is pressed, and the feather's
# opening visit runs. Boot 3: no press — a typed
# word's answer stands inside the terminal window,
# and 'files' typed there opens its window. Boot 4:
# the terminal's close mark is pressed, and typing
# raises the window again with its keeping whole
# (proofs/stone38-boot1.py to stone38-boot4.py).
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
}

for n in 1 2 3 4; do
    launch
    echo "--- boot $n ---"
    python3 "proofs/stone38-boot$n.py" "$SOCK" "$DUMP" || exit 1
    kill $QEMU_PID 2>/dev/null || true
    QEMU_PID=""
    sleep 1
done

echo "PASS"
