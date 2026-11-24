#!/bin/sh
# Prove the EFI door: the shipped disc, booted at the
# UEFI door under the bench's OVMF firmware, rises to
# the same desktop and answers the same words as at
# the BIOS door. The EFI doorman was built with the
# disc and never checked until Stone 41's hunt told
# the two doors apart; this proof is its first.
#
# The firmware is the bench's own: the OVMF pair under
# ~/qemu-root/usr/share/OVMF (the read-only code image
# and a throwaway copy of the variables image, so no
# boot writes anything that lasts). A bench without
# that pair is told so plainly and the proof stops.
set -e
cd "$(dirname "$0")"

OVMF_CODE="$HOME/qemu-root/usr/share/OVMF/OVMF_CODE_4M.fd"
OVMF_VARS="$HOME/qemu-root/usr/share/OVMF/OVMF_VARS_4M.fd"
if [ ! -f "$OVMF_CODE" ] || [ ! -f "$OVMF_VARS" ]; then
    echo "FAIL: the bench's OVMF firmware pair is not at $HOME/qemu-root/usr/share/OVMF" >&2
    exit 1
fi

# The bench's emulator, as in prove-iso.sh.
QEMU="$HOME/qemu10-root/usr/bin/qemu-system-x86_64"
QEMU_LOADER="$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2"
QEMU_LIBPATH="$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu"
QEMU_DATADIR="$HOME/qemu10-root/usr/share/qemu"
QEMU_BIOSDIR="$HOME/qemu10-root/usr/share/seabios"

echo "--- building the shipped disc ---"
./build-iso.sh >/dev/null

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cp "$OVMF_VARS" "$WORK/vars.fd"

echo "--- boot 1 (the desktop, the feather's visit, and the Bible window, all at the EFI door) ---"
"$QEMU_LOADER" --library-path "$QEMU_LIBPATH" "$QEMU" \
    -drive "if=pflash,format=raw,readonly=on,file=$OVMF_CODE" \
    -drive "if=pflash,format=raw,file=$WORK/vars.fd" \
    -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
    -boot order=d -display none -m 4096 -nic none \
    -monitor "unix:$WORK/mon.sock,server,nowait" \
    -L "$QEMU_DATADIR" -L "$QEMU_BIOSDIR" \
    >/dev/null 2>&1 &
QPID=$!
sleep 2
RC=0
python3 tools/pixels.py proofs/efi-boot1.py "$WORK/mon.sock" "$WORK/dump.ppm" || RC=$?
kill $QPID 2>/dev/null || true
wait $QPID 2>/dev/null || true
if [ "$RC" -ne 0 ]; then
    exit 1
fi

echo PASS
