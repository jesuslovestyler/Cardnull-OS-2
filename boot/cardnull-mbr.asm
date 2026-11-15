# The stick's first sector — the master boot record of
# the Cardnull stick image (Stone 17). Public domain,
# like everything in Cardnull.
#
# The stick image is the disc's own bytes (an ISO9660
# image, whose volume descriptor stands at byte 32768)
# with its first sectors given to booting as a hard
# disc: this record at sector 0, and Cardnull's BIOS
# bootloader (boot/cardnull-boot.asm) in the sectors
# after it, inside the ISO's unused system area. The
# firmware loads this sector at 0x7C00 and hands over
# the drive number in DL, exactly as for any hard disc.
#
# The stub is small and does three things:
#   1. It copies itself down to 0x0600, out of the way
#      of the doorstep it is about to fill.
#   2. From there, it reads the bootloader's sectors
#      (BOOT_SECTORS of them, counted by build-stick.sh
#      and baked in here) from sector 1 to 0x7C00,
#      through the BIOS's extended read, with DL — the
#      drive number — carried through untouched.
#   3. It jumps to the bootloader at 0x7C00, which walks
#      the ISO filesystem and does the rest, exactly as
#      at the disc's BIOS door; only its sector reckoning
#      differs (it asks the device its measure itself).
#
# If the read fails, it says so on the screen in plain
# words and stops.
#
# The partition table names one partition — the whole
# image, bootable — as a courtesy to tools that ask;
# nothing in the boot path consults it. STICK_SECTORS
# (the image's length in 512-byte sectors) is likewise
# baked in by build-stick.sh.
#
# Linked at 0x0600: the first instructions are position-
# independent (no label is named until after the move),
# and every label after the move is the address the code
# actually runs at, down at 0x0600.

    .intel_syntax noprefix
    .code16
    .text
    .globl _start
_start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00
    sti
    # Copy this sector down to 0x0600.
    mov si, 0x7C00
    mov di, 0x0600
    mov cx, 256
    rep movsw
    # Run on from the copy.
    jmp 0x0000:here
here:
    mov [drive], dl
    # The read packet: BOOT_SECTORS sectors from
    # sector 1, laid at 0x0000:0x7C00.
    mov ah, 0x41
    mov bx, 0x55AA
    int 0x13
    jc fail
    cmp bx, 0xAA55
    jne fail
    mov si, offset dap
    mov ah, 0x42
    mov dl, [drive]
    int 0x13
    jc fail
    # The bootloader takes the doorstep, with the drive
    # number in DL as the firmware gave it.
    mov dl, [drive]
    jmp 0x0000:0x7C00

fail:
    # Say it plainly on the text screen, then stop.
    mov si, offset fail_text
    mov ah, 0x0E
    xor bx, bx
fail_char:
    lodsb
    test al, al
    jz fail_stop
    int 0x10
    jmp fail_char
fail_stop:
    cli
    hlt
    jmp fail_stop

drive:
    .byte 0

    .align 4
dap:
    .byte 16
    .byte 0
    .word BOOT_SECTORS
    .word 0x7C00
    .word 0
    .quad 1

fail_text:
    .asciz "Cardnull could not start: the stick could not be read.\r\n"

    # The partition table stands at byte 446, as the
    # form of a master boot record asks.
    .fill (446 - (. - _start)), 1, 0
    .byte 0x80                # bootable
    .byte 0x00, 0x02, 0x00    # first sector, in the old reckoning
    .byte 0x83                # a plain partition
    .byte 0xFF, 0xFF, 0xFF    # last sector, in the old reckoning
    .long 0                   # it begins at the image's first sector
    .long STICK_SECTORS       # and spans the whole image
    .fill 48, 1, 0            # three empty entries
    .word 0xAA55
