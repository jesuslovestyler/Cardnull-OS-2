#!/bin/sh
# Builds the Cardnull OS 2 witness disc: dist/cardnull-os-2.iso.
#
# The disc carries everything, and nothing else is needed:
#
#   /boot/cardnull.elf    the system itself
#   /boot/settings.bin    the settings module (Stone 4)
#   /boot/feather.fea     the welcome feather (Stone 5),
#                         carrying its card at its own head
#                         (Nifla Stone 20)
#   /boot/paint.fea       the paint feather (Stone 24),
#                         its own module with its own card,
#                         received through the same door
#   /boot/calc.fea        the calculator feather (Stone 30),
#                         its own module with its own card,
#                         received through the same door
#   /boot/boot.img        the BIOS boot image: Cardnull's
#                         own bootloader (Stone 11 —
#                         boot/cardnull-boot.asm)
#   /boot/efi.img         the EFI system partition image:
#                         \EFI\BOOT\BOOTX64.EFI — Cardnull's
#                         own EFI loader (Stone 16 —
#                         boot/cardnull-efi.c) — and its own
#                         copies of the kernel and modules
#
# The disc boots BOTH ways (the EFI door was healed by
# Stone 9 — see the README): on a BIOS machine through the
# El Torito boot image, and on a UEFI machine through the
# EFI system partition. At BOTH doors stands Cardnull's
# OWN loader now: at the BIOS door since Stone 11 (written
# for this repository, in assembly, public domain), and at
# the EFI door since Stone 16 (boot/cardnull-efi.c, a
# freestanding C program compiled for the firmware's own
# calling way and linked as an EFI application). Each
# reads the system and its modules, sets the picture mode
# the system asks for, lays the multiboot information in
# the same shape, and hands over — no GRUB stands at
# either door any more. The disc is laid with xorriso's
# El Torito support for both entries. (The bench's
# grub-mkrescue was tried first, long ago, and, from its
# relocated tree, silently produced a disc with no boot
# image at all; the explicit route below is the one that
# is proven — see prove-iso.sh.)
#
# The EFI loader's building: clang (a system clang when
# present, else the bench's own tree at ~/qemu-root)
# compiles the loader's C and its handover assembly for
# the Windows x64 calling way the UEFI world speaks, the
# system linker lays them as a PE file of the console
# kind, and a two-byte patch — the PE subsystem field,
# set by a small python3 pass below, because the linker
# will not name the EFI kind — makes it an EFI
# application, the kind the firmware loads. The spike of
# this road stands behind Stone 16's README section.
#
# The EFI partition is formed with mtools at its own
# default reckoning for a small image (which lays down
# FAT12): forcing FAT32 at this size was measured on the
# bench to make a partition the firmware would not boot.
#
# Tooling: xorriso and mtools from the PATH; the
# assembler and linker from the system.
#
# Overrides (used by prove-iso.sh to lay variant discs):
#   ISO_OUT, KERNEL_FILE, SETTINGS_FILE, FEATHER_FILE,
#   PAINT_FILE, CALC_FILE

set -e
cd "$(dirname "$0")"

./build.sh >/dev/null

ISO_OUT="${ISO_OUT:-dist/cardnull-os-2.iso}"
KERNEL_FILE="${KERNEL_FILE:-build/cardnull.elf}"
SETTINGS_FILE="${SETTINGS_FILE:-build/settings.bin}"
FEATHER_FILE="${FEATHER_FILE:-build/welcome.feather}"
PAINT_FILE="${PAINT_FILE:-build/paint.feather}"
CALC_FILE="${CALC_FILE:-build/calculator.feather}"

# The stage check (Stone 41): the BIOS doorman stages the
# system file entire at 0x40000, the four modules on the
# low ground below it, and works in protected mode on a
# stack whose top stands at 0x3F000 (boot/cardnull-boot
# .asm's own map tells the laying). Stone 41's growth
# carried the staged file's span across the old stages
# and the old stack silently — the file outgrew the
# header's claim while the claim went on being believed
# — and the running machine reset on a pointer press.
# So the laying is checked here, on every build, by the
# files' ACTUAL sizes and never any claim: the system
# span [0x40000, 0x40000 + its size) must meet no module
# stage and not the stack's top, every module's stage
# span must meet neither the system span nor another
# stage, and every module file must fit its stage. A
# build that breaks the law stops here and says so.
SYS_BASE=262144        # 0x40000
STACK_TOP=258048       # 0x3F000
SET_BASE=65536;  SET_SPAN=2048    # 0x10000, 2 KiB
FEA_BASE=67584;  FEA_SPAN=6144    # 0x10800, 6 KiB
PNT_BASE=73728;  PNT_SPAN=8192    # 0x12000, 8 KiB
CAL_BASE=81920;  CAL_SPAN=16384   # 0x14000, 16 KiB
SYS_SIZE=$(wc -c < "$KERNEL_FILE")
SYS_END=$(( SYS_BASE + SYS_SIZE ))
stage_fail() {
    echo "FAIL: the doorman's stage laying is broken — $1" >&2
    echo "The system file stands at $SYS_SIZE bytes, staged at 0x40000 (span to $SYS_END)." >&2
    echo "Move the stages in boot/cardnull-boot.asm and this check together, as the map there tells." >&2
    exit 1
}
# The stack's top must stand outside the system span.
if [ "$STACK_TOP" -ge "$SYS_BASE" ] && [ "$STACK_TOP" -lt "$SYS_END" ]; then
    stage_fail "the protected-mode stack's top (0x3F000) stands inside the staged system's span"
fi
# Each stage: its file fits it, and its span meets neither
# the system span nor (checked pairwise below) another's.
check_stage() {
    _name="$1"; _base="$2"; _span="$3"; _file="$4"
    _size=$(wc -c < "$_file")
    if [ "$_size" -gt "$_span" ]; then
        stage_fail "the $_name file ($_size bytes) outgrows its stage ($_span bytes)"
    fi
    _end=$(( _base + _span ))
    if [ "$_base" -lt "$SYS_END" ] && [ "$SYS_BASE" -lt "$_end" ]; then
        stage_fail "the $_name stage stands inside the staged system's span"
    fi
}
check_stage "settings"        "$SET_BASE" "$SET_SPAN" "$SETTINGS_FILE"
check_stage "feather"         "$FEA_BASE" "$FEA_SPAN" "$FEATHER_FILE"
check_stage "paint feather"   "$PNT_BASE" "$PNT_SPAN" "$PAINT_FILE"
check_stage "calculator feather" "$CAL_BASE" "$CAL_SPAN" "$CALC_FILE"
# The stages among themselves.
stages_meet() {
    _ab="$1"; _ae=$(( $1 + $2 )); _bb="$3"; _be=$(( $3 + $4 ))
    [ "$_ab" -lt "$_be" ] && [ "$_bb" -lt "$_ae" ]
}
if stages_meet "$SET_BASE" "$SET_SPAN" "$FEA_BASE" "$FEA_SPAN" ||
   stages_meet "$SET_BASE" "$SET_SPAN" "$PNT_BASE" "$PNT_SPAN" ||
   stages_meet "$SET_BASE" "$SET_SPAN" "$CAL_BASE" "$CAL_SPAN" ||
   stages_meet "$FEA_BASE" "$FEA_SPAN" "$PNT_BASE" "$PNT_SPAN" ||
   stages_meet "$FEA_BASE" "$FEA_SPAN" "$CAL_BASE" "$CAL_SPAN" ||
   stages_meet "$PNT_BASE" "$PNT_SPAN" "$CAL_BASE" "$CAL_SPAN"; then
    stage_fail "two module stages stand inside one another's ground"
fi

if command -v clang >/dev/null 2>&1; then
    CLANG=clang
elif [ -x "$HOME/qemu-root/usr/bin/clang" ]; then
    CLANG="$HOME/qemu-root/usr/bin/clang"
else
    echo "FAIL: no clang found (system or ~/qemu-root) — the EFI loader is built with it" >&2
    exit 1
fi
command -v xorriso >/dev/null 2>&1 || { echo "FAIL: no xorriso found" >&2; exit 1; }
command -v mformat >/dev/null 2>&1 || { echo "FAIL: no mtools found (mformat)" >&2; exit 1; }
command -v mcopy >/dev/null 2>&1 || { echo "FAIL: no mtools found (mcopy)" >&2; exit 1; }
command -v as >/dev/null 2>&1 || { echo "FAIL: no assembler found (as) — the BIOS bootloader is built with it" >&2; exit 1; }
command -v ld >/dev/null 2>&1 || { echo "FAIL: no linker found (ld) — both bootloaders are linked with it" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "FAIL: no python3 found — the EFI application's subsystem patch is laid with it" >&2; exit 1; }

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/root/boot" "$(dirname "$ISO_OUT")"

cp "$KERNEL_FILE" "$WORK/root/boot/cardnull.elf"
cp "$SETTINGS_FILE" "$WORK/root/boot/settings.bin"
cp "$FEATHER_FILE" "$WORK/root/boot/feather.fea"
cp "$PAINT_FILE" "$WORK/root/boot/paint.fea"
cp "$CALC_FILE" "$WORK/root/boot/calc.fea"

# The BIOS door: Cardnull's own bootloader (Stone 11),
# assembled from boot/cardnull-boot.asm and linked flat at
# 0x7C00, padded to whole sectors — the El Torito catalog's
# load size spans the whole image, so the firmware lays it
# all at the doorstep and it runs as one stage.
as --32 -o "$WORK/boot.o" boot/cardnull-boot.asm
ld -m elf_i386 -Ttext 0x7C00 --oformat binary -o "$WORK/root/boot/boot.img" "$WORK/boot.o"
BOOT_SIZE=$(wc -c < "$WORK/root/boot/boot.img")
BOOT_SECTORS=$(( (BOOT_SIZE + 511) / 512 ))
truncate -s $(( BOOT_SECTORS * 512 )) "$WORK/root/boot/boot.img"

# The EFI door: Cardnull's own EFI loader (Stone 16),
# compiled from boot/cardnull-efi.c and its handover
# (boot/cardnull-efi-hand.S), linked as a PE file, and
# patched to the EFI application kind (subsystem 10) —
# the two bytes at the PE optional header's +68 that the
# firmware reads to know what it is loading.
mkdir -p "$WORK/esp/EFI/BOOT" "$WORK/esp/boot"
"$CLANG" --target=x86_64-pc-windows-gnu -ffreestanding -nostdinc \
    -fno-stack-protector -fno-builtin -mno-red-zone -O1 \
    -c boot/cardnull-efi.c -o "$WORK/efi.o"
"$CLANG" --target=x86_64-pc-windows-gnu -ffreestanding \
    -c boot/cardnull-efi-hand.S -o "$WORK/efi-hand.o"
ld -mi386pep -e efi_main "$WORK/efi.o" "$WORK/efi-hand.o" \
    -o "$WORK/esp/EFI/BOOT/BOOTX64.EFI"
python3 - "$WORK/esp/EFI/BOOT/BOOTX64.EFI" <<'PYEOF'
import struct
import sys
path = sys.argv[1]
data = bytearray(open(path, "rb").read())
pe = struct.unpack_from("<I", data, 0x3C)[0]
assert data[pe:pe + 4] == b"PE\0\0", "not a PE file"
struct.pack_into("<H", data, pe + 4 + 20 + 68, 10)  # EFI application
open(path, "wb").write(data)
PYEOF
cp "$KERNEL_FILE" "$WORK/esp/boot/cardnull.elf"
cp "$SETTINGS_FILE" "$WORK/esp/boot/settings.bin"
cp "$FEATHER_FILE" "$WORK/esp/boot/feather.fea"
cp "$PAINT_FILE" "$WORK/esp/boot/paint.fea"
cp "$CALC_FILE" "$WORK/esp/boot/calc.fea"
dd if=/dev/zero of="$WORK/root/boot/efi.img" bs=1M count=8 2>/dev/null
mformat -i "$WORK/root/boot/efi.img" ::
mcopy -i "$WORK/root/boot/efi.img" -s "$WORK/esp/EFI" ::
mcopy -i "$WORK/root/boot/efi.img" -s "$WORK/esp/boot" ::

xorriso -as mkisofs -o "$ISO_OUT" \
    -b boot/boot.img -no-emul-boot -boot-load-size "$BOOT_SECTORS" \
    -eltorito-alt-boot -e boot/efi.img -no-emul-boot \
    "$WORK/root" 2>/dev/null

SIZE=$(wc -c < "$ISO_OUT")
SHA=$(sha256sum "$ISO_OUT" | awk '{print $1}')
echo "Built $ISO_OUT ($SIZE bytes)"
echo "sha256: $SHA"
