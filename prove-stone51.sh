#!/bin/sh
# prove-stone51.sh — the proof of Stone 51: the
# Tunes Window.
#
# Stone 51 gives the desktop a fourteenth window:
# the tunes window, opened by the word 'tunes' and
# by the bar menu's new Tunes choice (Rest standing
# last still, one row lower). Three hymn tunes stand
# in it by name — Amazing Grace, Jesus Loves Me, Joy
# to the World — the picked one standing white on
# blue. A press on a tune's row picks it and it
# sings through the PC speaker (speaker.nifla's
# road, Stone 18), the desktop waiting while it
# sings, as it waits for the welcome chime. The
# window drags by its title bar and closes by its
# close mark like any other, and its chip stands on
# the bar while it stands open.
#
# The bench cannot hear the singing: what it proves
# is everything the glass can show — the window
# opening by word and by menu, its words and the
# three names standing in it, the pick moving to
# the pressed tune and standing while the tune's
# length runs out (the scenario waits the tune's
# whole reckoned length before it trusts the
# desktop again), the drag carrying the window, and
# the close mark putting it away. The singing
# itself is the speaker's proven road (Stone 18's
# chime sounds on this same bench's boots, and the
# notes here are that road's own playnote), and its
# hearing waits for Tyler's witness, as the drag's
# healing does.
#
# Two boots:
#   boot 1  the word 'tunes' opens the window
#           forward, its chip on the bar; a press on
#           Jesus Loves Me's row moves the pick; the
#           window drags; its close mark closes it.
#   boot 2  the bar menu — grown to fifteen rows,
#           Tunes at the thirteenth choice and Rest
#           last — opens the window by its Tunes
#           choice; a press on Amazing Grace's row
#           sings it, and the window stands whole
#           after the singing.
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
    # $1 = scenario, $2 = socket tag.
    SOCK="$WORK/monitor-$2.sock"
    DUMP="$WORK/dump-$2.ppm"
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -device qemu-xhci -device usb-kbd \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
            -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -device qemu-xhci -device usb-kbd \
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

echo "--- boot 1 (the word opens it; the pick, the drag, the close) ---"
boot proofs/stone51-boot1.py 1 || exit 1

echo "--- boot 2 (the menu's Tunes choice; Amazing Grace sings) ---"
sleep 5
boot proofs/stone51-boot2.py 2 || exit 1

echo "PASS"
