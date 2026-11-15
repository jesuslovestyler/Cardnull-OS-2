#!/bin/sh
# Witness-disc proof: Cardnull OS 2 booted FROM ITS ISO.
#
# Every boot here is a CD-ROM boot of an ISO file — no
# -kernel shortcut, no other drive attached — at 4096 MB,
# the standing witness size, on the bench QEMU. Three discs
# are booted:
#
#   Boot 1: the shipped disc (dist/cardnull-os-2.iso, built
#     fresh by build-iso.sh) — the desktop on the disc's
#     Eastern choice, the guest's visit, and 'utc' moving
#     the clock for the session.
#   Boot 2: a variant disc whose settings carry the world's
#     standard time — the clock must come up at hour 00 on
#     its own, proving the choice rides the disc.
#   Boot 3: a variant disc with one byte of the guest
#     flipped — the refusal in plain words, the guest never
#     appearing, the desktop unharmed.
#
# Since Stone 9 the shipped kernel asks the loader for a
# picture screen, and on this bench the disc's own loaders
# grant it — so the shipped disc's face is light, and its
# words cannot be read back from the text screen's memory. The three discs
# below are therefore laid down with the same kernel built
# WITHOUT the asking (build/cardnull-text.elf): the same
# sources, the same disc layout, the same modules — the
# kernel's own fallback text face carries the words, and
# this proof reads them as it always has. The picture face
# itself, booting the very dist file, is prove-stone9.sh's
# charge.
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

# Boots an ISO as the machine's only drive (a CD-ROM on the
# second IDE channel) and runs a screen scenario against it.
boot_iso() {
    ISO="$1"
    SCENARIO="$2"
    SOCK="$WORK/monitor-$3.sock"
    # The bench clock is pinned to midnight UTC (Stone 7:
    # the system reads the machine's real clock), so the
    # discs' carried time choices show the expected hours.
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=$ISO,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
            -drive "file=$ISO,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
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
    python3 tools/screen.py "$SCENARIO" "$SOCK"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

echo "--- building the shipped disc ---"
./build-iso.sh || { echo "FAIL: build-iso.sh failed"; exit 1; }

echo "--- boot 1 (the shipped disc's layout, the text face) ---"
ISO_OUT="$WORK/cardnull-text.iso" KERNEL_FILE=build/cardnull-text.elf ./build-iso.sh >/dev/null || { echo "FAIL: text-face disc build failed"; exit 1; }
boot_iso "$WORK/cardnull-text.iso" proofs/iso-boot1.py 1 || exit 1

echo "--- boot 2 (a disc carrying the world's time) ---"
python3 tools/make-modules.py build/guest.bin "$WORK/settings-utc.bin" "$WORK/card.bin" 64 >/dev/null
ISO_OUT="$WORK/cardnull-utc.iso" KERNEL_FILE=build/cardnull-text.elf SETTINGS_FILE="$WORK/settings-utc.bin" ./build-iso.sh >/dev/null || { echo "FAIL: variant build failed"; exit 1; }
boot_iso "$WORK/cardnull-utc.iso" proofs/iso-boot2.py 2 || exit 1

echo "--- boot 3 (a disc carrying a tampered guest) ---"
python3 - "$WORK" <<'PYEOF'
import sys
work = sys.argv[1]
guest = bytearray(open("build/guest.bin", "rb").read())
guest[100] ^= 0xFF
open(work + "/guest-tampered.bin", "wb").write(guest)
PYEOF
ISO_OUT="$WORK/cardnull-tampered.iso" KERNEL_FILE=build/cardnull-text.elf GUEST_FILE="$WORK/guest-tampered.bin" ./build-iso.sh >/dev/null || { echo "FAIL: variant build failed"; exit 1; }
boot_iso "$WORK/cardnull-tampered.iso" proofs/iso-boot3.py 3
