#!/bin/sh
# Stone 32 proof: ears on the modern USB road. The kernel
# is booted with the modules that ride its disc (QEMU's
# -initrd is the bench form of the bootloader's multiboot
# handoff), and a USB host controller of the kind the new
# driver speaks — an xHCI controller, the USB 3.0
# arrangement:
#
#   Boot 1 (controller + a USB keyboard): the system says
#     a USB keyboard is ready on the modern USB road,
#     typing is answered — shifted letters and Caps Lock
#     among it, as Stone 12 requires of any road — and
#     the 'usb' word's own count for the modern road
#     proves that road carried the keys.
#   Boot 2 (controller, no keyboard): no ready word, the
#     PS/2 road answers as always, and 'usb' answers
#     plainly that no USB keyboard is plugged in.
#   Boot 3 (no modern controller at all): the same script
#     as boot 2 — the road's absence changes nothing.
#
# tools/launch.sh takes no USB devices, so this proof
# launches the bench's QEMU itself, in launch.sh's own
# shape (as prove-stone6.sh does). Prints PASS or FAIL.

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
    SOCK="$1"
    shift
    "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
        --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
        "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
        -kernel build/cardnull.elf -display none -m 128 -nic none \
        -initrd build/settings.bin,build/welcome.feather \
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

echo "--- boot 1 (xHCI controller + USB keyboard) ---"
boot "$WORK/monitor1.sock" -device qemu-xhci -device usb-kbd
python3 tools/screen.py proofs/stone32-boot1.py "$WORK/monitor1.sock" || exit 1
stop

echo "--- boot 2 (xHCI controller, no keyboard) ---"
boot "$WORK/monitor2.sock" -device qemu-xhci
python3 tools/screen.py proofs/stone32-boot2.py "$WORK/monitor2.sock" || exit 1
stop

echo "--- boot 3 (no xHCI controller at all) ---"
boot "$WORK/monitor3.sock"
python3 tools/screen.py proofs/stone32-boot2.py "$WORK/monitor3.sock"
