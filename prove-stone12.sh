#!/bin/sh
# Stone 12 proof: real typing. The shift keys and Caps
# Lock speak on both keyboard roads, and a typed line may
# hold more than one word — its first word the command
# word, the rest kept whole.
#
#   Boot 1 (the PS/2 road): a shifted sentence read back
#     off the typing line exactly, a two-word line answered
#     by its first word, Caps Lock's capitals and their
#     turning off, a figure and its shifted mark, and a
#     single-word command answered as it always was.
#   Boot 2 (the USB road): the same grammar from the USB
#     keyboard's reports — the modifier byte for the
#     shifts, the Caps Lock usage for the caps — with the
#     'usb' word's own count as the evidence of the road,
#     as at Stone 6. tools/launch.sh takes no USB devices,
#     so this boot launches the bench's QEMU itself, in
#     launch.sh's own shape (as prove-stone6.sh does).
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

echo "--- boot 1 (the PS/2 road: shift, caps, and many words) ---"
SOCK="$WORK/monitor-1.sock"
QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96 "" "build/settings.bin,build/card.bin,build/feather.bin")
python3 tools/screen.py proofs/stone12-boot1.py "$SOCK" || exit 1
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""
sleep 1

echo "--- boot 2 (the USB road: the same grammar) ---"
"$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
    --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
    "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
    -kernel build/cardnull.elf -display none -m 128 -nic none \
    -initrd build/settings.bin,build/card.bin,build/feather.bin \
    -monitor "unix:$WORK/monitor-2.sock,server,nowait" \
    -L "$HOME/qemu10-root/usr/share/qemu" \
    -L "$HOME/qemu10-root/usr/share/seabios" \
    -pidfile "$WORK/qemu.pid" -daemonize \
    -device piix3-usb-uhci -device usb-kbd
QEMU_PID=$(cat "$WORK/qemu.pid")
python3 tools/screen.py proofs/stone12-boot2.py "$WORK/monitor-2.sock" || exit 1

echo "PASS"
