#!/bin/sh
# Stone 31 proof: the help window. The shipped disc
# is booted at the BIOS door (the face of light),
# twice, with no disk fitted:
#
#   Boot 1 (the usual size): the word 'help' opens
#     the window; every one of its five pages is
#     DECODED letter by letter against the system's
#     own letter shapes (proofs/stone31-boot1.py,
#     through tools/pixels.py) and compared against
#     the kept help words in src/helpwords.nifla —
#     the pages turned by the down arrow key and by
#     presses on the window's foot (its More word,
#     and First page on the last page), its foot's
#     standing decoded as it changes. Tab brings the
#     welcome window forward, the word brings the
#     help window forward again, Escape closes it;
#     the bar's menu — its nine choices decoded, Help
#     among them, Rest last — opens it by a press on
#     the Help choice, and a press on its close mark
#     closes it.
#   Boot 2 (the large size): the settings window's
#     Large row is pressed, Escape closes it, and the
#     word opens the help window on the narrow large
#     face, its first two pages whole in it — every
#     line at most thirty-six letters, the window's
#     inner width at that size, so none is cut —
#     decoded letter by letter at the large scale;
#     Escape closes it.
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
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
            -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
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

echo "--- boot 1 (no disk: the help window by its word, its pages, the menu, and the close mark) ---"
boot proofs/stone31-boot1.py 1 || exit 1

echo "--- boot 2 (no disk: the help window at the large size) ---"
boot proofs/stone31-boot2.py 2 || exit 1

echo "PASS"
