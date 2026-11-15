#!/bin/sh
# Stone 18 proof: a voice.
#
# Two boots of the shipped disc:
#
#   Boot 1 (the drawn face, the speaker heard): QEMU
#     with the PC speaker wired to a wav audiodev and
#     two monitors — one drives the screen scenario
#     (proofs/stone18-boot1.py), the other carries the
#     monitor's wavcapture, opened by the scenario in a
#     window around each event. The bench's capture
#     delivers the speaker's active samples, so the
#     analysis below asserts on those windows exactly:
#       boot.wav   non-silent, a tone in the chime's
#                  band (the welcome, as the desktop
#                  rises)
#       refuse.wav non-silent, a tone in the low band
#                  (the refusal of an unknown word)
#       idle.wav   silence — four seconds of nothing,
#                  and no stray noise in them
#       chime.wav  non-silent, the chime's band again
#                  (the word 'chime')
#   Boot 2 (the text face, NO audio device at all): the
#     'chime' word is answered in plain words and typing
#     is unheld — the evidence that a machine without
#     the speaker path is unaffected (proofs/
#     stone18-boot2.py).
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

echo "--- boot 1 (the drawn face; the voice in its windows) ---"
SOCK="$WORK/monitor.sock"
SNDSOCK="$WORK/sound.sock"
DUMP="$WORK/dump.ppm"
ISO="$PWD/dist/cardnull-os-2.iso"
if [ -n "${QEMU:-}" ]; then
    echo "FAIL: the sound boot needs the bench QEMU's two-monitor shape; unset QEMU" >&2
    exit 1
elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
    "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
        --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
        "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
        -drive "file=$ISO,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
        -boot order=d -display none -m 4096 -nic none \
        -rtc base=2026-11-15T00:00:00 \
        -audiodev "wav,id=snd,path=$WORK/backend.wav" \
        -machine pcspk-audiodev=snd \
        -monitor "unix:$SOCK,server,nowait" \
        -monitor "unix:$SNDSOCK,server,nowait" \
        -L "$HOME/qemu10-root/usr/share/qemu" \
        -L "$HOME/qemu10-root/usr/share/seabios" \
        >/dev/null 2>&1 &
    QEMU_PID=$!
else
    echo "FAIL: no QEMU found (looked for ~/qemu10-root)" >&2
    exit 1
fi
SNDSOCK="$SNDSOCK" SNDWORK="$WORK" python3 tools/pixels.py proofs/stone18-boot1.py "$SOCK" "$DUMP" || exit 1
QEMU_PID=""

echo "--- the captures, weighed ---"
python3 - "$WORK" <<'PYEOF' || exit 1
import array
import sys
import wave

work = sys.argv[1]
failed = []


def weigh(name):
    try:
        w = wave.open(work + "/" + name, "rb")
    except Exception:
        return None
    frames = w.getnframes()
    rate = w.getframerate()
    chans = w.getnchannels()
    a = array.array("h")
    a.frombytes(w.readframes(frames))
    if chans == 2:
        a = a[::2]
    loud = [x for x in a if abs(x) > 2000]
    freq = 0.0
    if len(loud) > 100:
        crossings = sum(1 for i in range(1, len(loud))
                        if (loud[i - 1] < 0) != (loud[i] < 0))
        freq = crossings / 2.0 / (len(loud) / float(rate))
    return {"frames": frames, "loud": len(loud), "freq": freq,
            "peak": max((abs(x) for x in a), default=0)}


def check(cond, what):
    print(("ok: " if cond else "FAIL: ") + what)
    if not cond:
        failed.append(what)


boot = weigh("boot.wav")
check(boot is not None and boot["loud"] >= 600,
      "the welcome sounded as the desktop rose (%s)"
      % (boot and boot["loud"]))
check(boot is not None and 400 <= boot["freq"] <= 900,
      "the welcome is a tone in the chime's band (%.0f Hz)"
      % (boot and boot["freq"]))

refuse = weigh("refuse.wav")
check(refuse is not None and refuse["loud"] >= 300,
      "the refusal sounded (%s)" % (refuse and refuse["loud"]))
check(refuse is not None and 120 <= refuse["freq"] <= 300,
      "the refusal is one low tone (%.0f Hz)"
      % (refuse and refuse["freq"]))

idle = weigh("idle.wav")
check(idle is not None and idle["loud"] <= 30,
      "silence discipline: nothing sounds unbidden (%s loud)"
      % (idle and idle["loud"]))

chime = weigh("chime.wav")
check(chime is not None and chime["loud"] >= 600,
      "'chime' sounded the welcome again (%s)"
      % (chime and chime["loud"]))
check(chime is not None and 400 <= chime["freq"] <= 900,
      "the repeated welcome is in the chime's band (%.0f Hz)"
      % (chime and chime["freq"]))

sys.exit(1 if failed else 0)
PYEOF

echo "--- boot 2 (the text face; no audio device at all) ---"
ISO_OUT="$WORK/cardnull-text.iso" KERNEL_FILE=build/cardnull-text.elf ./build-iso.sh >/dev/null || { echo "FAIL: variant build failed"; exit 1; }
SOCK="$WORK/monitor-text.sock"
if [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
    "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
        --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
        "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
        -drive "file=$WORK/cardnull-text.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
        -boot order=d -display none -m 4096 -nic none \
        -rtc base=2026-11-15T00:00:00 \
        -monitor "unix:$SOCK,server,nowait" \
        -L "$HOME/qemu10-root/usr/share/qemu" \
        -L "$HOME/qemu10-root/usr/share/seabios" \
        >/dev/null 2>&1 &
    QEMU_PID=$!
fi
python3 tools/screen.py proofs/stone18-boot2.py "$SOCK" || exit 1
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""

echo "PASS"
