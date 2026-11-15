#!/bin/sh
# Starts the bench QEMU in the background and prints its
# process id — the shared launch of every proof in this
# repository, copied from the pattern of the Nifla language's
# bare-metal proofs: the extracted QEMU 10 in ~/qemu10-root,
# run through its own loader, or a plain qemu-system-x86_64
# command line in $QEMU when one is installed.
#
# Usage: tools/launch.sh <elf> <monitor.sock> <megabytes> [disk-image]

ELF="$1"
SOCK="$2"
MEM="$3"
IMG="${4:-}"

DRIVE=""
if [ -n "$IMG" ]; then
    DRIVE="-drive file=$IMG,format=raw,if=ide,index=0"
fi

if [ -n "${QEMU:-}" ]; then
    # Ready-made command lines and the drive words are split
    # on purpose.
    # shellcheck disable=SC2086
    $QEMU -kernel "$ELF" -display none -m "$MEM" -nic none $DRIVE \
        -monitor "unix:$SOCK,server,nowait" &
    echo $!
elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
    # shellcheck disable=SC2086
    "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
        --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
        "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
        -kernel "$ELF" -display none -m "$MEM" -nic none $DRIVE \
        -monitor "unix:$SOCK,server,nowait" \
        -L "$HOME/qemu10-root/usr/share/qemu" \
        -L "$HOME/qemu10-root/usr/share/seabios" \
        >/dev/null 2>&1 &
    echo $!
else
    echo "FAIL: no QEMU found (looked for ~/qemu10-root; set QEMU to a qemu-system-x86_64 command)" >&2
    exit 1
fi
