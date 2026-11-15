#!/bin/sh
# Stone 6 proof: ears on the USB road. The kernel is booted
# with the three modules that ride its disc (QEMU's -initrd
# is the bench form of the bootloader's multiboot handoff),
# and a USB host controller of the kind the driver speaks —
# a UHCI controller, the USB 1.1 companion road:
#
#   Boot 1 (controller + a USB keyboard): the system says
#     a USB keyboard is ready, typing is answered, and the
#     'usb' word's own count proves the USB road carried
#     the keys.
#   Boot 2 (controller, no keyboard): no ready word, the
#     PS/2 road answers as always, and 'usb' answers
#     plainly that no USB keyboard is plugged in.
#   Boot 3 (no controller at all): the same script as
#     boot 2 — the road's absence changes nothing.
#
# tools/launch.sh takes no USB devices, so this proof
# launches the bench's QEMU itself, in launch.sh's own
# shape. Prints PASS or FAIL.

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

boot() {
    # $1 = the monitor socket, $2.. = extra QEMU arguments.
    # The launch mirrors tools/launch.sh's own shape: the
    # extracted QEMU 10, run through its own loader.
    SOCK="$1"
    shift
    "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
        --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
        "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
        -kernel build/cardnull.elf -display none -m 128 -nic none \
        -initrd build/settings.bin,build/card.bin,build/feather.bin \
        -monitor "unix:$SOCK,server,nowait" \
        -L "$HOME/qemu10-root/usr/share/qemu" \
        -L "$HOME/qemu10-root/usr/share/seabios" \
        -pidfile "$WORK/qemu.pid" -daemonize "$@"
    QEMU_PID=$(cat "$WORK/qemu.pid")
}

stop() {
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
}

echo "--- boot 1 (UHCI controller + USB keyboard) ---"
boot "$WORK/monitor1.sock" -device piix3-usb-uhci -device usb-kbd
python3 tools/screen.py proofs/stone6-boot1.py "$WORK/monitor1.sock" || exit 1
stop

echo "--- boot 2 (UHCI controller, no keyboard) ---"
boot "$WORK/monitor2.sock" -device piix3-usb-uhci
python3 tools/screen.py proofs/stone6-boot2.py "$WORK/monitor2.sock" || exit 1
stop

echo "--- boot 3 (no USB controller at all) ---"
boot "$WORK/monitor3.sock"
python3 tools/screen.py proofs/stone6-boot2.py "$WORK/monitor3.sock"
