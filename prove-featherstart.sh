#!/bin/sh
# Feather-start proof: the word "feather" at STARTUP,
# read back as writing, with NO input at all.
#
# The shipped disc is booted at the BIOS door (the
# face of light) and no key is sent and no mouse is
# moved — the scenario (proofs/featherstart-boot1.py,
# through tools/pixels.py) only waits and looks, as
# the witness proof does, and DECODES letter by letter
# against the system's own letter shapes every place
# the word "feather" stands in the startup view: the
# feather window's title, its body's plain sentence
# before any visit, and the word in the invitation
# line.
#
# This proof stands because the feather-paint proof
# could not see the fault it watches for: that proof
# types 'feather' first and decodes the visit's panel,
# and the visit repaints the window — while the title
# the desktop rises with is painted once, at the
# rising, by a span that named five letters for a
# seven-letter word, so the title stood as "Feath"
# from the first moment. Tyler witnessed exactly that
# on his own machine, booting the delivered disc of
# November 16, 2026: "feather still say feath by the
# way when the operating system starts." This proof
# starts the machine and reads, with empty hands.
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
./build-iso.sh || { echo "FAIL: build-iso.sh failed"; exit 1; }

SOCK="$WORK/monitor.sock"
DUMP="$WORK/dump.ppm"
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
python3 tools/pixels.py proofs/featherstart-boot1.py "$SOCK" "$DUMP" || exit 1

echo "PASS"
