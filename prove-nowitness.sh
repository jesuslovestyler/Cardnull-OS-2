#!/bin/sh
# The witness-fix proof: the face paints with NO input.
#
# On November 15, 2026, Tyler booted the Stone 20 disc
# in UTM on his Mac and witnessed: at the SeaBIOS door,
# a black screen until he typed, then the text face
# instead of the drawn desktop; at the UEFI door, a
# black screen no key could wake. The fifteen standing
# proofs had all passed on that build — they drive the
# machine with injected keys and read its memory or its
# screen afterwards, so a fault in the first paint, or
# in the road before it, is invisible to them.
#
# This proof is the correction, and it joins the
# standing set. It boots the shipped images and sends
# NO key and NO mouse movement at all — it only waits
# and looks at the screen (tools/pixels.py running
# proofs/nowitness.py), and the drawn desktop must
# stand on it: the blue bar, the gray welcome panel,
# the panel's words, the invitation.
#
# Five boots:
#   1. the ISO at the BIOS door (SeaBIOS), the bench's
#      ordinary machine shape;
#   2. the ISO at the BIOS door on the q35 machine
#      shape — the shape whose firmware lays memory
#      differently, and the shape UTM's own default
#      follows;
#   3. the ISO at the EFI door (OVMF), ordinary shape;
#   4. the ISO at the EFI door on q35 — the bench's
#      own reproduction of the witnessed dead door:
#      before the fix, this boot's screen stayed pure
#      black forever (the firmware had laid the EFI
#      doorman's image above the four-billion line,
#      and the handover's step down was cut in half
#      there); now the desktop must paint;
#   5. the stick image at the BIOS door — the stick
#      walks the same doorman's code as the disc.
#
# The stick's file is read once through before its
# boot: during the witness investigation the bench's
# own serving of a cold image file proved unsteady
# (boots failing at the disc-services step until the
# host held the file in hand), while the standing
# stick proof, which always boots a just-built image,
# never saw it. The reading keeps this proof measuring
# the no-input paint, its own question; the disc reads
# themselves are the Stone 17 proof's question.
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

QEMU_BIN="$HOME/qemu10-root/usr/bin/qemu-system-x86_64"
QEMU_LD="$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2"
QEMU_LIBPATH="$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu"
OVMF_DIR="$HOME/qemu10-root/usr/share/OVMF"

# Boots an ISO as the machine's only drive at the BIOS
# door, on the machine shape named, and runs the
# no-input pixel scenario against it.
boot_iso_bios() {
    ISO="$1"
    MACHINE="$2"
    SOCK="$WORK/monitor-$3.sock"
    DUMP="$WORK/dump-$3.ppm"
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -machine "$MACHINE" \
            -drive "file=$ISO,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$QEMU_BIN" ]; then
        "$QEMU_LD" --library-path "$QEMU_LIBPATH" "$QEMU_BIN" \
            -machine "$MACHINE" \
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
    python3 tools/pixels.py proofs/nowitness.py "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

# Boots an ISO as the machine's only drive at the EFI
# door (OVMF), on the machine shape named, and runs the
# no-input pixel scenario against it.
boot_iso_efi() {
    ISO="$1"
    MACHINE="$2"
    SOCK="$WORK/monitor-$3.sock"
    DUMP="$WORK/dump-$3.ppm"
    if [ -n "${QEMU:-}" ]; then
        echo "FAIL: the EFI boot needs the bench QEMU's OVMF firmware; unset QEMU" >&2
        exit 1
    elif [ -x "$QEMU_BIN" ] && [ -f "$OVMF_DIR/OVMF_CODE_4M.fd" ]; then
        cp "$OVMF_DIR/OVMF_VARS_4M.fd" "$WORK/vars-$3.fd"
        "$QEMU_LD" --library-path "$QEMU_LIBPATH" "$QEMU_BIN" \
            -machine "$MACHINE" \
            -drive "file=$ISO,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
            -boot order=d -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -drive "if=pflash,format=raw,readonly=on,file=$OVMF_DIR/OVMF_CODE_4M.fd" \
            -drive "if=pflash,format=raw,file=$WORK/vars-$3.fd" \
            -monitor "unix:$SOCK,server,nowait" \
            -L "$HOME/qemu10-root/usr/share/qemu" \
            -L "$HOME/qemu10-root/usr/share/seabios" \
            >/dev/null 2>&1 &
        QEMU_PID=$!
    else
        echo "FAIL: no bench QEMU / OVMF found (looked for ~/qemu10-root)" >&2
        exit 1
    fi
    python3 tools/pixels.py proofs/nowitness.py "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

# Boots the stick image as the machine's hard disc at
# the BIOS door and runs the no-input pixel scenario.
boot_stick_bios() {
    IMG="$1"
    SOCK="$WORK/monitor-$2.sock"
    DUMP="$WORK/dump-$2.ppm"
    # The bench's cold-file unsteadiness, named in this
    # script's header: read the image once through.
    cat "$IMG" > /dev/null
    if [ -n "${QEMU:-}" ]; then
        # shellcheck disable=SC2086
        $QEMU -drive "file=$IMG,format=raw,if=ide,index=0,media=disk" \
            -boot order=c -display none -m 4096 -nic none \
            -rtc base=2026-11-15T00:00:00 \
            -monitor "unix:$SOCK,server,nowait" &
        QEMU_PID=$!
    elif [ -x "$QEMU_BIN" ]; then
        "$QEMU_LD" --library-path "$QEMU_LIBPATH" "$QEMU_BIN" \
            -drive "file=$IMG,format=raw,if=ide,index=0,media=disk" \
            -boot order=c -display none -m 4096 -nic none \
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
    python3 tools/pixels.py proofs/nowitness.py "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

echo "--- building the shipped disc and stick ---"
./build-iso.sh || { echo "FAIL: build-iso.sh failed"; exit 1; }
./build-stick.sh >/dev/null || { echo "FAIL: build-stick.sh failed"; exit 1; }

echo "--- boot 1 (the disc at the BIOS door, no input) ---"
boot_iso_bios dist/cardnull-os-2.iso pc 1 || exit 1

echo "--- boot 2 (the disc at the BIOS door on q35, no input) ---"
boot_iso_bios dist/cardnull-os-2.iso q35 2 || exit 1

echo "--- boot 3 (the disc at the EFI door, no input) ---"
boot_iso_efi dist/cardnull-os-2.iso pc 3 || exit 1

echo "--- boot 4 (the disc at the EFI door on q35, no input) ---"
boot_iso_efi dist/cardnull-os-2.iso q35 4 || exit 1

echo "--- boot 5 (the stick at the BIOS door, no input) ---"
boot_stick_bios dist/cardnull-stick.img 5 || exit 1

echo "PASS"
