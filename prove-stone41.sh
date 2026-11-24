#!/bin/sh
# Stone 41 proof: the Bible reading window — the whole
# book of Jonah in the World English Bible's wording,
# read at length in a window of its own. The shipped
# disc is booted at the BIOS door (the face of light),
# two times, with no disk fitted:
#
#   Boot 1: the word 'bible' opens the window on its
#     contents page — DECODED line by line against the
#     system's own letter shapes (proofs/stone41-boot1.py,
#     through tools/pixels.py): the page names the book
#     and its translation and lists its four chapters,
#     the picked chapter standing white on blue. The
#     pick moves with the arrow keys; Enter reads Jonah
#     1, whose pages are decoded line by line against
#     the bundled text's own words (src/bibletext.nifla,
#     wrapped as the window wraps it) — turned forward
#     by the down arrow and by a press on the foot's
#     More word, and back by the up arrow and by a press
#     on the foot's Back word, the earlier words standing
#     again exactly. Jonah 4 is read the same way and
#     turned to the book's last page; a press on First
#     page returns to the contents page, and Escape
#     closes the window.
#   Boot 2: the window's other two roads in — the ninth
#     desktop icon (a blue book with a gold cross, its
#     name 'Bible' beside it), a press on which opens
#     the window, and a press on its close mark closes
#     it; and the bar's menu, risen one row higher for
#     its ten choices — decoded, Bible the ninth and
#     Rest last — a press on whose Bible choice opens
#     the window again (proofs/stone41-boot2.py).
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

echo "--- boot 1 (the word 'bible', the contents page, Jonah read forward and back) ---"
boot proofs/stone41-boot1.py 1 || exit 1

echo "--- boot 2 (the icon, the close mark, and the menu's Bible choice) ---"
boot proofs/stone41-boot2.py 2 || exit 1

echo "PASS"
