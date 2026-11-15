#!/bin/sh
# Stone 9 proof: a face with light.
#
# Three boots of ISO files as CD-ROMs, no other drive
# attached, at 4096 MB, the bench clock pinned to midnight
# UTC:
#
#   Boot 1: the shipped disc (dist/cardnull-os-2.iso, built
#     fresh by build-iso.sh) — GRUB grants the asked-for
#     picture screen, and the desktop, the answers, the
#     clock's advance, and the guest's visit are all DRAWN,
#     verified by pixel sampling (proofs/stone9-boot1.py).
#   Boot 2: a variant disc with one byte of the guest
#     flipped — the refusal drawn in light, no green
#     anywhere (proofs/stone9-boot2.py).
#   Boot 3: a variant disc laid down with the kernel built
#     without the video asking — no picture is granted, and
#     the text face carries the desktop, saying in plain
#     words why (proofs/stone9-boot3.py, read back through
#     the text screen by tools/screen.py).
#   Boot 4: the shipped disc again, through the EFI door
#     (OVMF firmware) — the same scenario as boot 1, with
#     the same expectations: the framebuffer kernel is what
#     the UEFI handoff needed (with the text kernel this
#     door could load the system but never show it).
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

# Boots an ISO as the machine's only drive and runs a
# PIXEL scenario against it (tools/pixels.py).
boot_iso_pixels() {
    ISO="$1"
    SCENARIO="$2"
    SOCK="$WORK/monitor-$3.sock"
    DUMP="$WORK/dump-$3.ppm"
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
    python3 tools/pixels.py "$SCENARIO" "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

# Boots an ISO as the machine's only drive and runs a TEXT
# scenario against it (tools/screen.py).
boot_iso_text() {
    ISO="$1"
    SCENARIO="$2"
    SOCK="$WORK/monitor-$3.sock"
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

# Boots an ISO as the machine's only drive under OVMF
# (UEFI firmware) and runs a PIXEL scenario against it.
boot_iso_efi() {
    ISO="$1"
    SCENARIO="$2"
    SOCK="$WORK/monitor-$3.sock"
    DUMP="$WORK/dump-$3.ppm"
    OVMF_DIR="$HOME/qemu10-root/usr/share/OVMF"
    if [ -n "${QEMU:-}" ]; then
        echo "FAIL: the EFI boot needs the bench QEMU's OVMF firmware; unset QEMU" >&2
        exit 1
    elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ] && [ -f "$OVMF_DIR/OVMF_CODE_4M.fd" ]; then
        cp "$OVMF_DIR/OVMF_VARS_4M.fd" "$WORK/vars-$3.fd"
        "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
            --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
            "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
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
    python3 tools/pixels.py "$SCENARIO" "$SOCK" "$DUMP"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

echo "--- building the shipped disc ---"
./build-iso.sh || { echo "FAIL: build-iso.sh failed"; exit 1; }

echo "--- boot 1 (the shipped disc: the face of light) ---"
boot_iso_pixels dist/cardnull-os-2.iso proofs/stone9-boot1.py 1 || exit 1

echo "--- boot 2 (a tampered guest, refused in light) ---"
python3 - "$WORK" <<'PYEOF'
import sys
work = sys.argv[1]
guest = bytearray(open("build/guest.bin", "rb").read())
guest[100] ^= 0xFF
open(work + "/guest-tampered.bin", "wb").write(guest)
PYEOF
ISO_OUT="$WORK/cardnull-tampered.iso" GUEST_FILE="$WORK/guest-tampered.bin" ./build-iso.sh >/dev/null || { echo "FAIL: variant build failed"; exit 1; }
boot_iso_pixels "$WORK/cardnull-tampered.iso" proofs/stone9-boot2.py 2 || exit 1

echo "--- boot 3 (no picture granted: the text face, in plain words) ---"
ISO_OUT="$WORK/cardnull-text.iso" KERNEL_FILE=build/cardnull-text.elf ./build-iso.sh >/dev/null || { echo "FAIL: variant build failed"; exit 1; }
boot_iso_text "$WORK/cardnull-text.iso" proofs/stone9-boot3.py 3 || exit 1

echo "--- boot 4 (the shipped disc through the EFI door) ---"
boot_iso_efi dist/cardnull-os-2.iso proofs/stone9-boot1.py 4 || exit 1

echo "PASS"
