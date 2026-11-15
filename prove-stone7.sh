#!/bin/sh
# Stone 7 proof: a true clock. The bench's real-time clock
# is pinned to known instants (QEMU's -rtc base, handed
# through tools/launch.sh's RTC_BASE), and the bar's date
# and time are read back:
#
#   Boot 1: pinned to Sunday, November 15, 2026, 14:32
#     UTC, the disc carrying Eastern — the bar must show
#     November 15 at 09:32, and 'time' must tell the same
#     moment in words.
#   Boot 2: pinned to Monday, November 16, 02:00 UTC,
#     Eastern again — the offset carries the date back
#     over midnight: November 15 at 21:00.
#   Boot 3: pinned to November 15, 23:59:50 UTC, the disc
#     carrying the world's time — the bar comes up on
#     November 15 and rolls forward to November 16 at
#     00:00 as the bench clock ticks.
#
# The bench clock is taken to hold the world's standard
# time — the standing assumption, named in rtclock.nifla
# and the README. Prints PASS or FAIL.

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

# A settings module carrying the world's standard time.
python3 tools/make-modules.py "$WORK/settings-utc.bin" 64 >/dev/null

echo "--- boot 1 (Nov 15, 14:32 UTC; the disc carries Eastern) ---"
SOCK="$WORK/monitor.sock"
QEMU_PID=$(RTC_BASE=2026-11-15T14:32:00 tools/launch.sh build/cardnull.elf "$SOCK" 96 "" "build/settings.bin,build/welcome.feather")
python3 tools/screen.py proofs/stone7-boot1.py "$SOCK" || exit 1
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""
sleep 1

echo "--- boot 2 (Nov 16, 02:00 UTC; Eastern carries the date back) ---"
SOCK="$WORK/monitor2.sock"
QEMU_PID=$(RTC_BASE=2026-11-16T02:00:00 tools/launch.sh build/cardnull.elf "$SOCK" 96 "" "build/settings.bin,build/welcome.feather")
python3 tools/screen.py proofs/stone7-boot2.py "$SOCK" || exit 1
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""
sleep 1

echo "--- boot 3 (Nov 15, 23:59:50 UTC; the date rolls forward) ---"
SOCK="$WORK/monitor3.sock"
QEMU_PID=$(RTC_BASE=2026-11-15T23:59:50 tools/launch.sh build/cardnull.elf "$SOCK" 96 "" "$WORK/settings-utc.bin,build/welcome.feather")
python3 tools/screen.py proofs/stone7-boot3.py "$SOCK"
