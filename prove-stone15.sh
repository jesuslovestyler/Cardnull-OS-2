#!/bin/sh
# Stone 15 proof: notes that stay. One keeping disk lives
# through three boots, and two more boots have no disk:
#
#   Boots 1-2 (one disk, two lives, the text face): the
#     gate's 'yes', two notes kept on the disk and shown;
#     the same disk booted again reads them back at boot,
#     and a third note joins them. The disk image's own
#     bytes are then checked below: the notes page's
#     header on sector 64 and the three notes in their
#     sectors, exactly as they were typed.
#   Boots 3-4 (no disk): a note kept for the session and
#     said to be; the next boot's page is empty again.
#   Boot 5 (the shipped disc, the face of light, the
#     keeping disk attached): 'notes' draws the kept
#     notes in light.
#   Boot 6 (a second disk, never given over): a session
#     note is typed, the gate is answered 'no' — and the
#     disk image's bytes afterward must be the very bytes
#     they were before (checked by hash below), Stone 8's
#     discipline standing over the notes too.
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
    QEMU_PID=$(tools/launch.sh build/cardnull.elf "$SOCK" 96 "$2" "build/settings.bin,build/card.bin,build/guest.bin")
    python3 tools/screen.py "$1" "$SOCK"
    RC=$?
    [ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
    QEMU_PID=""
    sleep 1
    return $RC
}

echo "--- boot 1 (blank disk: gate, yes, two notes kept) ---"
boot proofs/stone15-boot1.py "$WORK/disk1.img" 1 || exit 1

echo "--- boot 2 (same disk: the notes read back, a third kept) ---"
boot proofs/stone15-boot2.py "$WORK/disk1.img" 2 || exit 1

echo "--- the disk's own bytes: the notes page as it was laid ---"
python3 - "$WORK/disk1.img" <<'PYEOF' || exit 1
import sys
data = open(sys.argv[1], "rb").read()
def sector(n):
    return data[n * 512:(n + 1) * 512]
head = sector(64)
assert head[0] == 67 and head[1] == 78 and head[2] == 78, "the notes header stands on sector 64"
assert head[3] == 3, f"the header keeps three notes (keeps {head[3]})"
for i, text in enumerate((b"remember the garden",
                          b"call billy about the roof",
                          b"pray for quinton")):
    s = sector(65 + i)
    assert s[0] == len(text), f"note {i + 1}'s length stands at its sector's head"
    assert s[1:1 + len(text)] == text, f"note {i + 1}'s words stand in its sector"
print("ok: the notes page stands on the disk, note for note as typed")
PYEOF

echo "--- boot 3 (no disk: a note for the session, said plainly) ---"
boot proofs/stone15-boot3.py "" 3 || exit 1

echo "--- boot 4 (no disk again: nothing stayed) ---"
boot proofs/stone15-boot4.py "" 4 || exit 1

echo "--- boot 5 (the shipped disc, the face of light, the keeping disk) ---"
./build-iso.sh >/dev/null || { echo "FAIL: build-iso.sh failed"; exit 1; }
SOCK="$WORK/monitor-5.sock"
DUMP="$WORK/dump.ppm"
if [ -n "${QEMU:-}" ]; then
    # shellcheck disable=SC2086
    $QEMU -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
        -drive "file=$WORK/disk1.img,format=raw,if=ide,index=0" \
        -boot order=d -display none -m 4096 -nic none \
        -monitor "unix:$SOCK,server,nowait" &
    QEMU_PID=$!
elif [ -x "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" ]; then
    "$HOME/qemu10-root/usr/lib64/ld-linux-x86-64.so.2" \
        --library-path "$HOME/qemu10-root/usr/lib/x86_64-linux-gnu:$HOME/qemu10-root/lib/x86_64-linux-gnu" \
        "$HOME/qemu10-root/usr/bin/qemu-system-x86_64" \
        -drive "file=dist/cardnull-os-2.iso,format=raw,if=ide,index=2,media=cdrom,readonly=on" \
        -drive "file=$WORK/disk1.img,format=raw,if=ide,index=0" \
        -boot order=d -display none -m 4096 -nic none \
        -monitor "unix:$SOCK,server,nowait" \
        -L "$HOME/qemu10-root/usr/share/qemu" \
        -L "$HOME/qemu10-root/usr/share/seabios" \
        >/dev/null 2>&1 &
    QEMU_PID=$!
else
    echo "FAIL: no QEMU found (looked for ~/qemu10-root; set QEMU to a qemu-system-x86_64 command)" >&2
    exit 1
fi
python3 tools/pixels.py proofs/stone15-boot5.py "$SOCK" "$DUMP" || exit 1
[ -n "$QEMU_PID" ] && kill "$QEMU_PID" 2>/dev/null
QEMU_PID=""

echo "--- boot 6 (second disk: a session note, the gate answered no) ---"
cat > "$WORK/stone15-boot6.py" <<'PYEOF'
def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")

typewrite("note a session note")
enter()
found = waitfor(
    lambda r: region_has(r, "Your note is kept until the machine is turned off."), 20)
expect(found is not None, "with no keeping yet, the note lives for the session")

typewrite("setup")
enter()
found = waitfor(
    lambda r: region_has(r, "This will clear everything on the disk."), 20)
expect(found is not None, "'setup' asks behind the gate, in plain words")

typewrite("no")
enter()
found = waitfor(
    lambda r: region_has(r, "The disk was left as it was."), 20)
expect(found is not None, "the gate's no leaves the disk as it was")

done()
PYEOF
boot "$WORK/stone15-boot6.py" "$WORK/disk2.img" 6 || exit 1

DISK2_AFTER=$(sha256sum "$WORK/disk2.img" | cut -d' ' -f1)
if [ "$DISK2_BEFORE" = "$DISK2_AFTER" ]; then
    echo "ok: the never-given disk's bytes are exactly as they were"
else
    echo "FAIL: the never-given disk's bytes changed"
    exit 1
fi

echo "PASS"
