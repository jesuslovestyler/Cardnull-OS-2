#!/bin/sh
# Stone 4 proof: the clock's time choice rides the disc.
# The system is booted three times with the modules a
# bootloader would bring from the disc (QEMU's -initrd is
# the bench form of the same multiboot handoff), and the
# bar's clock is read back each time:
#
#   Boot 1: the settings module carries the world's
#     standard time — the clock must come up at hour 00 on
#     its own; the word 'eastern' must move it to 19, with
#     an answer that says the choice lasts until the
#     machine is turned off.
#   Boot 2: the settings module carries Eastern time (the
#     settings the build lays) — the clock must come up at
#     hour 19; the word 'utc' must move it to 00.
#   Boot 3: no modules at all — the clock must start on
#     the honest default, Eastern time, and 'feather' must
#     be answered plainly: this disc holds no feather.
#
# No disk is attached in any boot: the system ships as one
# disc and nothing else. Prints PASS or FAIL.

set -u
cd "$(dirname "$0")"

# Since Stone 7 the system reads the machine's real clock;
# this proof's hours are reckoned against a bench clock
# pinned to midnight at the day's turn (UTC), so the time
# choice's hours come out as they are expected below.
RTC_BASE=2026-11-15T00:00:00
export RTC_BASE

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

echo "--- boot 1 (the disc carries the world's time) ---"
SOCK="$WORK/monitor.sock"
QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96 "" "$WORK/settings-utc.bin,build/welcome.feather")
python3 tools/screen.py proofs/stone4-boot1.py "$SOCK" || exit 1
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""
sleep 1

echo "--- boot 2 (the disc carries Eastern time) ---"
SOCK="$WORK/monitor2.sock"
QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96 "" "build/settings.bin,build/welcome.feather")
python3 tools/screen.py proofs/stone4-boot2.py "$SOCK" || exit 1
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""
sleep 1

echo "--- boot 3 (no modules at all) ---"
SOCK="$WORK/monitor3.sock"
QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96)
python3 tools/screen.py proofs/stone4-boot3.py "$SOCK"
