#!/bin/sh
# Stone 20 proof: the settings window. The shipped disc
# is booted at the BIOS door (the face of light), three
# times:
#
#   Boot 1 (a fitted keeping disk, prepared below with
#     the settings card on sector 8 — C, N, and the
#     offset byte 59 for Eastern, its chime byte 0 as a
#     card laid before this stone carries): the word
#     'settings' opens the window, and its rendered
#     choices are DECODED letter by letter against the
#     system's own letter shapes (proofs/stone20-boot1.py,
#     through tools/pixels.py). The bench clock stands at
#     2026-11-15T00:00:00 on the world's standard time,
#     so the bar clock reads 19 under Eastern and 00
#     under the world's standard: the typed word
#     'eastern' is answered as before, a press of the
#     pointer on the world's-standard row moves the bar
#     clock's own rendered figures to 00, and a press on
#     the chime-off row stands the chime off in the
#     window. Tab cycles through all four windows, and
#     Escape closes the settings window. Between the
#     boots the disk's own bytes are checked: the card
#     must now carry the clicked choices — the offset
#     byte 64 and the chime byte 2.
#   Boot 2 (the SAME disk): nothing is chosen again —
#     the bar clock must already stand at 00 and the
#     window must show both choices as boot 1 left them:
#     the choices persisted from the settings card.
#   Boot 3 (no disk at all): the window says plainly
#     that the choices last only for this sitting, and a
#     click still moves the clock for the sitting.
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

echo "--- laying the keeping disk: the settings card, Eastern, the chime unchosen ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
img = bytearray(8 * 1024 * 1024)
# The settings card (sector 8): C, N, and the offset
# byte — Eastern, 59 — so the disk stands as the
# system's own keeping disk at boot. The chime byte
# (the card's fourth) stands 0, as every card laid
# before Stone 20 carries it: the chime stands on.
img[8 * 512 + 0] = 67
img[8 * 512 + 1] = 78
img[8 * 512 + 2] = 59
img[8 * 512 + 3] = 0
with open(sys.argv[1], "wb") as f:
    f.write(img)
print("ok: the disk stands prepared with its Eastern card")
PYEOF

boot() {
    # $1 = scenario, $2 = disk image ("" for none), $3 = socket tag
    SOCK="$WORK/monitor-$3.sock"
    DUMP="$WORK/dump-$3.ppm"
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        if [ -n "$2" ]; then
            $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
                -drive "file=$2,format=raw,if=ide,index=0" \
                -boot order=d -display none -m 4096 -nic none \
                -rtc base=2026-11-15T00:00:00 \
                -monitor "unix:$SOCK,server,nowait" &
        else
            $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
                -boot order=d -display none -m 4096 -nic none \
                -rtc base=2026-11-15T00:00:00 \
                -monitor "unix:$SOCK,server,nowait" &
        fi
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        if [ -n "$2" ]; then
            "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
                --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
                "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
                -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
                -drive "file=$2,format=raw,if=ide,index=0" \
                -boot order=d -display none -m 4096 -nic none \
                -rtc base=2026-11-15T00:00:00 \
                -monitor "unix:$SOCK,server,nowait" \
                -L "$HOME/qemu10-root/usr/share/qemu" \
                -L "$HOME/qemu10-root/usr/share/seabios" \
                >/dev/null 2>&1 &
        else
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
        fi
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

echo "--- boot 1 (the keeping disk: open, type, click, cycle, close) ---"
boot proofs/stone20-boot1.py "$WORK/disk.img" 1 || exit 1

echo "--- the disk's own bytes: the card carries the clicked choices ---"
python3 - "$WORK/disk.img" <<'PYEOF'
import sys
with open(sys.argv[1], "rb") as f:
    data = f.read()
card = data[8 * 512:8 * 512 + 4]
assert card[0] == 67 and card[1] == 78, "the card's letters stand on sector 8"
assert card[2] == 64, f"the offset byte is the world's standard 64 (found {card[2]})"
assert card[3] == 2, f"the chime byte stands off, 2 (found {card[3]})"
print("ok: the settings card carries the clicked choices (offset 64, chime 2)")
PYEOF
[ $? -eq 0 ] || { echo "FAIL: the settings card does not carry the clicked choices"; exit 1; }

echo "--- boot 2 (the same disk: the choices persisted) ---"
boot proofs/stone20-boot2.py "$WORK/disk.img" 2 || exit 1

echo "--- boot 3 (no disk: the choices last only for this sitting) ---"
boot proofs/stone20-boot3.py "" 3 || exit 1

echo "PASS"
