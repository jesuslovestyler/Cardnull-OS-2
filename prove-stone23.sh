#!/bin/sh
# Stone 23 proof: the bar's menu. The shipped disc is
# booted at the BIOS door (the face of light), once,
# with no disk fitted:
#
#   A press of the pointer on the top bar opens the
#   menu, and its five rendered choices — Welcome,
#   Feather, Files, Settings, Editor — are DECODED
#   letter by letter against the system's own letter
#   shapes (proofs/stone23-boot1.py, through
#   tools/pixels.py). A press on the Files choice opens
#   the files window, exactly as the typed word does —
#   its title and its plain heading decoded at the
#   window's own place — and Escape closes it again, as
#   it always has. The menu is reopened and dismissed
#   by a press on the plain desktop elsewhere: the
#   menu's ground must stand plain desktop again, no
#   window may have opened, and the welcome window's
#   title must still decode — the desktop whole. The
#   typed word 'files' opens the files window again,
#   exactly as before. Finally the menu is opened once
#   more and Escape puts the menu away and no window
#   with it — the files window's title still decodes —
#   and the bar's clock still stands at its right end.
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

echo "--- boot 1 (no disk: the bar's menu opens, chooses, dismisses) ---"
boot proofs/stone23-boot1.py 1 || exit 1

echo "PASS"
