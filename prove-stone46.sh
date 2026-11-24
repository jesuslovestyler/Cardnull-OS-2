#!/bin/sh
# Stone 46 proof: all the programs in the start menu.
# The shipped disc is booted at the BIOS door (the
# face of light), no disk fitted:
#
#   The start button opens the bar's menu and all
#   thirteen of its choices are decoded at their
#   reckoned rows — Welcome, Feather, Files, Editor,
#   Paint, Calculator, Verse, Help, Settings,
#   Terminal, Bible, Shield, Rest, the desktop
#   icons' own order (Paint and Terminal new to the
#   menu at this stone, standing where they stand
#   among their neighbors). Then the new choices and
#   a moved one are pressed: Paint opens the paint
#   window with its feather's opening visit standing
#   in it; Terminal brings the terminal window
#   forward; Bible — ninth before this stone,
#   eleventh now — opens the Bible window on its
#   contents page; and Rest, last as always, opens
#   the rest panel, which Stay then puts away
#   (proofs/stone46-boot1.py).
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
if [ -n "${QEMU:-}" ]; then
    # shellcheck disable=SC2086
    $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
        -boot order=d -display none -m 4096 -nic none \
        -rtc base=2026-11-24T12:00:00 \
        -monitor "unix:$SOCK,server,nowait" &
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
        >/dev/null 2>&1 &
    QEMU_PID=$!
else
    echo "FAIL: no QEMU found (looked for ~/qemu10-root; set QEMU to a qemu-system-x86_64 command)" >&2
    exit 1
fi

echo "--- boot 1 (no disk: the menu's thirteen choices, and the new and moved ones pressed) ---"
python3 tools/pixels.py proofs/stone46-boot1.py "$SOCK" "$DUMP" || exit 1

echo "PASS"
