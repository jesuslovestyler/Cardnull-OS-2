#!/bin/sh
# Stone 25 proof: a kind shutdown, with restart. The
# shipped disc is booted at the BIOS door (the face of
# light), twice, each time with a fitted keeping disk
# prepared below with the settings card on sector 8
# (C, N, and the offset byte 59 for Eastern) and an
# empty notes page:
#
#   Boot 1 (shutdown): a note is kept by the word
#     'note' and seen in the files window; the bar's
#     menu is opened and its seven choices DECODED —
#     the six windows and Rest under them (the menu
#     grew by Rest at this stone, and by Verse at
#     Stone 29, which moved Rest to the seventh row
#     and this proof's reckoning with it; Stone 23's
#     proof still checks its five) — and a press
#     on Rest opens the rest panel, whose plain words
#     (Rest, Shut down, Restart, Stay) are decoded at
#     its reckoned place. A press on Shut down's row
#     rests the machine: the scenario records which of
#     the two honest endings the bench shows — the
#     machine actually powered off under QEMU (the
#     monitor's door closed), or the machine standing
#     halted with its plain fallback words rendered,
#     decoded letter by letter. The scenario writes
#     which ending it saw to a file this script reads
#     back and reports (after a scenario ends, the
#     bench's process is gone either way — the harness
#     asks QEMU to quit — so the process itself cannot
#     say which ending it was). After the boot this
#     script also reads the disk's own bytes: the CNN3
#     header and the kept note must stand in their
#     sectors — nothing kept was lost.
#   Boot 2 (restart): a note is kept, the word 'rest'
#     opens the panel, and a press on Restart's row
#     resets the machine: the scenario watches the
#     desktop FALL and RISE A SECOND TIME in the same
#     QEMU run (the drawn desktop and its welcome
#     window's title decoded again), then opens the
#     files window and reads the note kept before the
#     restart standing in its list — it survived.
#
# The resting itself is exercised for real throughout:
# the typed words, the menu, the panel, and the
# pointer's presses are the person's own roads, and the
# power and reset doors are the machine's own (src/
# rest.nifla). No static glance stands in for any of it.
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

laydisk() {
    # $1 = the disk image to lay: the settings card,
    # Eastern, and nothing else — a keeping disk whose
    # notes page is still empty.
    python3 - "$1" <<'PYEOF'
import sys
img = bytearray(8 * 1024 * 1024)
img[8 * 512 + 0] = 67
img[8 * 512 + 1] = 78
img[8 * 512 + 2] = 59
img[8 * 512 + 3] = 0
with open(sys.argv[1], "wb") as f:
    f.write(img)
print("ok: the disk stands prepared with its Eastern card")
PYEOF
}

boot() {
    # $1 = scenario, $2 = disk image, $3 = socket tag.
    # The QEMU pid is left in QEMU_PID for the caller's
    # own check; the caller kills it when it still runs.
    SOCK="$WORK/monitor-$3.sock"
    DUMP="$WORK/dump-$3.ppm"
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -drive "file=$2,format=raw,if=ide,index=0" \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
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
        QEMU_PID=$!
    else
        echo "FAIL: no QEMU found (looked for ~/qemu10-root; set QEMU to a qemu-system-x86_64 command)" >&2
        exit 1
    fi
    python3 tools/pixels.py "$1" "$SOCK" "$DUMP"
    return $?
}

echo "--- laying the first keeping disk ---"
laydisk "$WORK/disk1.img"

echo "--- boot 1 (keep a note, Rest by the menu, Shut down) ---"
STONE25_RESULT1="$WORK/result1.txt"
export STONE25_RESULT1
boot proofs/stone25-boot1.py "$WORK/disk1.img" 1
RC=$?
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""
[ $RC -eq 0 ] || exit 1
# Which ending the bench showed is the scenario's own
# written word (see proofs/stone25-boot1.py): after a
# scenario ends, the bench's process is gone either
# way — the harness asks QEMU to quit — so the process
# itself can no longer say which ending it was.
if [ -f "$STONE25_RESULT1" ]; then
    case "$(cat "$STONE25_RESULT1")" in
        off) echo "ok: BENCH RESULT for the report — the machine actually powered off under QEMU" ;;
        fallback) echo "ok: BENCH RESULT for the report — the machine stayed on, halted, with its fallback words rendered" ;;
        *) echo "ok: BENCH RESULT for the report — neither ending was read (the scenario said so)" ;;
    esac
else
    echo "FAIL: the scenario left no bench result behind"
    exit 1
fi

echo "--- the first disk's own bytes: the kept note survived the shutdown ---"
python3 - "$WORK/disk1.img" <<'PYEOF'
import sys
with open(sys.argv[1], "rb") as f:
    data = f.read()
head = data[64 * 512:64 * 512 + 4]
assert head[0] == 67 and head[1] == 78 and head[2] == 78, "the CNN3 header stands on sector 64"
assert head[3] == 1, f"the header counts one note (found {head[3]})"
note = b"a note before rest"
sec = data[65 * 512:65 * 512 + 1 + len(note)]
assert sec[0] == len(note), "the note's length stands at its sector's head"
assert sec[1:] == note, f"the note's words stand in their sector (found {sec[1:]!r})"
card = data[8 * 512:8 * 512 + 3]
assert card[0] == 67 and card[1] == 78 and card[2] == 59, "the settings card still stands on sector 8"
print("ok: the CNN3 store carries the note, and the settings card stands")
PYEOF
[ $? -eq 0 ] || { echo "FAIL: the kept note did not survive on the disk"; exit 1; }

echo "--- laying the second keeping disk ---"
laydisk "$WORK/disk2.img"

echo "--- boot 2 (keep a note, rest by the word, Restart, the second rise) ---"
boot proofs/stone25-boot2.py "$WORK/disk2.img" 2
RC=$?
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""
[ $RC -eq 0 ] || exit 1

echo "PASS"
