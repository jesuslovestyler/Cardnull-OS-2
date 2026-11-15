#!/bin/sh
# Stone 8 proof: remembers for real. A blank disk image is
# attached as the machine's hard disk (tools/launch.sh's
# fourth argument, IDE master), the bench clock pinned to
# midnight UTC so the time choice's hours are known:
#
#   Boots 1-3 (one disk, three lives): the offer, the gate,
#     'yes', and 'utc' kept (hour 00); the same disk booted
#     again comes up at 00 though the disc still carries
#     Eastern, and 'eastern' is kept in turn; a third boot
#     comes up at 19 — the write-back persisted both ways.
#   Boot 4 (a second disk, never given over): the offer,
#     ordinary answers, the gate answered 'no' — and the
#     disk image's bytes afterward must be the very bytes
#     they were before (checked by hash below).
#   Boot 5 (no disk): the disc's choice rules, no offer,
#     and 'setup' answered plainly.
#
# Prints PASS or FAIL.

set -u
cd "$(dirname "$0")"

./build.sh >/dev/null || { echo "FAIL: build.sh failed"; exit 1; }

WORK=$(mktemp -d)
QEMU_PID=""
cleanup() {
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    rm -rf "$WORK"
}
trap cleanup EXIT

python3 - "$WORK" <<'PYEOF'
import sys
work = sys.argv[1]
for name in ("disk1.img", "disk2.img"):
    with open(work + "/" + name, "wb") as f:
        f.write(bytes(8 * 1024 * 1024))
print("Two blank 8 MB disk images laid.")
PYEOF
DISK2_BEFORE=$(sha256sum "$WORK/disk2.img" | cut -d' ' -f1)

boot() {
    # $1 = scenario, $2 = disk image ("" for none), $3 = socket tag
    SOCK="$WORK/monitor-$3.sock"
    QEMU_PID=$(RTC_BASE=2026-11-15T00:00:00 tools/launch.sh build/cardnull.elf "$SOCK" 96 "$2" "build/settings.bin,build/card.bin,build/feather.bin")
    python3 tools/screen.py "$1" "$SOCK"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

echo "--- boot 1 (blank disk: offer, gate, yes, utc kept) ---"
boot proofs/stone8-boot1.py "$WORK/disk1.img" 1 || exit 1

echo "--- boot 2 (same disk: its choice overrules the disc) ---"
boot proofs/stone8-boot2.py "$WORK/disk1.img" 2 || exit 1

echo "--- boot 3 (same disk: the write-back persisted) ---"
boot proofs/stone8-boot3.py "$WORK/disk1.img" 3 || exit 1

echo "--- boot 4 (second disk: the gate answered no) ---"
boot proofs/stone8-boot4.py "$WORK/disk2.img" 4 || exit 1

DISK2_AFTER=$(sha256sum "$WORK/disk2.img" | cut -d' ' -f1)
if [ "$DISK2_BEFORE" = "$DISK2_AFTER" ]; then
    echo "ok: the never-given disk's bytes are exactly as they were"
else
    echo "FAIL: the never-given disk's bytes changed"
    exit 1
fi

echo "--- boot 5 (no disk at all) ---"
boot proofs/stone8-boot5.py "" 5
