# Cardnull's own doorman — the BIOS boot loader of
# Cardnull OS 2 (Stone 11). Public domain, like everything
# in Cardnull.
#
# This is the disc's BIOS door: an El Torito no-emulation
# boot image. The firmware loads the whole image at
# 0x7C00 (the catalog's load size spans it), and this code
# does the rest, in the open:
#
#   1. It reads the disc itself, through the BIOS's own
#      disc services (int 13h, the extended read), walking
#      the ISO9660 filesystem from the primary volume
#      descriptor: root directory, then BOOT, then the
#      five files — CARDNULL.ELF, SETTINGS.BIN,
#      FEATHER.FEA, PAINT.FEA, CALC.FEA — each staged in
#      low memory.
#   2. It asks the machine its memory map (int 15h, E820)
#      and lays the multiboot information down: the map,
#      the memory figures, and a module table for the
#      four modules that ride with the system.
#   3. When the system's own header asks for a picture
#      screen (the multiboot video request, Stone 9), it
#      sets the matching VESA mode with its linear
#      framebuffer and writes the grant into the
#      information — address, pitch, size, and the color
#      fields' places — exactly as the loader before it
#      did. When the header does not ask, the machine
#      stays in its text mode and no grant is written.
#   4. It opens the A20 line, steps into 32-bit protected
#      mode with paging off, lays the system's ELF
#      segments where they belong and the modules above
#      them, and hands over: the multiboot mark in EAX,
#      the information's address in EBX, interrupts off.
#
# It borrows nothing at the door: no GRUB stands here any
# more — and since Stone 16 none stands at the EFI door
# either; both doors are Cardnull's own. If anything it
# needs is not found — the disc services, a file, the
# system's shape — it says so on the screen in plain
# words and stops, rather than handing over a machine
# half-laid.
#
# Stone 17 taught this doorman the second road it now
# walks: the stick. The stick image is this same disc's
# bytes with a master boot record at its head (boot/
# cardnull-mbr.asm) that loads this loader from the
# sectors after it; the firmware hands over a hard
# disc's drive number, and this loader's reads — told
# in the CD's 2048-byte sectors everywhere above — are
# translated at the packet by the device's own sector
# measure, asked once at the door (int 13h AH=48). The
# ISO filesystem is walked exactly as on the CD; only
# the reckoning of its sectors changes.
#
# Memory, while the doorman works (all low, all its own):
#   0x1000  one disc sector, read and re-read
#   0x2000  the VESA information blocks
#   0x4000  the multiboot information
#   0x4400  the module table (four entries)
#   0x4800  the memory map, as the BIOS gave it
#   0x7C00  this loader (its stack grows down from here)
#   0x40000 the system file, staged (up to 320 KiB)
#   0x90000 the settings module, staged (up to 2 KiB)
#   0x90800 the feather, staged (up to 6 KiB) — the
#           feather carries its card at its own head
#           (Nifla Stone 20); no card module rides anymore
#   0x92000 the paint feather, staged (Stone 24: the
#           second feather, its own card at its own head,
#           received through the same door) — its claim is
#           8 KiB now (Stone 32)
#   0x94000 the calculator feather, staged (Stone 30:
#           the third feather, its own card at its own
#           head, received through the same door), its
#           16 KiB claim ending at 0x98000
# (The modules' stages stand above the system's WHOLE
# stage, all 256 KiB of its claim: the system's file is
# staged entire, and any byte of it may be wanted by the
# segment copies that follow. They once stood at 0x60000
# and 0x62000, inside the claim, on the reckoning that
# the system's text ended well below them — true until
# the feather door's growth in the Stone 20 adoption
# carried the text's tail, and its GDT with it, across
# the settings stage's line: the staged settings then
# overwrote the GDT's code descriptor, and the system
# died at its first far jump. Measured on the bench
# (November 15, 2026) and moved in the open: nothing may
# stage inside another stage's claim again. The claim
# itself grew at Stone 26 (November 16, 2026), by the
# same measure and for the same reason: Stone 26's code
# carried the staged file's span past the 192 KiB line
# (its text reaching 0x719AD in the stage), the staged
# settings splashed its tail again, and the machine
# never rose — reproduced on the bench, the stages
# moved above the new whole claim, and the feather's
# 56 KiB claim ends where the paint feather's stage
# begins, as it did before. The claim grew again at
# Stone 29 (November 16, 2026), by the same measure and
# for the same reason: Stone 29's verse window carried
# the staged file's span to 234,640 bytes, past the
# 224 KiB line, so the claim stands at 256 KiB now and
# the module stages stand above the whole of it —
# settings at 0x80000, the feather at 0x82000 (its
# 56 KiB claim ending where the paint feather's stage
# begins, as before), the paint feather at 0x90000,
# all below the firmware's own reserved ground. Stone
# 30 (November 16, 2026) laid a fourth module's stage
# the same way: the paint feather's claim stands at
# 32 KiB and the calculator feather stages at 0x98000,
# its 32 KiB claim ending at 0xA0000, where the
# firmware's reserved ground begins — no stage stands
# inside another's claim, as always. The claim grew
# again at Stone 32 (November 16, 2026), by the same
# measure and for the same reason: Stone 32's modern
# USB road carried the staged file's span past the
# 256 KiB line, so the claim stands at 320 KiB now and
# the module stages stand above the whole of it —
# settings at 0x90000, the feather at 0x90800, the
# paint feather at 0x92000, and the calculator feather
# at 0x94000, its claim ending at 0x98000. Above the
# raised claim there stand only 64 KiB before the
# firmware's reserved ground at 0xA0000, so the
# modules' claims stand at their tight measures now —
# 2, 6, 8, and 16 KiB, each with room over its file as
# it stands — and a module that outgrows its claim
# must move the stages again, as always.)
# and on the far side of the step into protected mode:
#   0x300000 the four modules, laid in a row
#
# Assembled flat and linked at 0x7C00 by build-iso.sh.

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
    mov [bootdrive], dl

    # The extended disc services are the road in.
    mov ah, 0x41
    mov bx, 0x55AA
    mov dl, [bootdrive]
    int 0x13
    jc fail_services
    cmp bx, 0xAA55
    jne fail_services

    # The device's own sector measure (Stone 17). The
    # ISO's reckoning in this loader is the CD's: one
    # sector is 2048 bytes, and the volume descriptor
    # stands at sector 16. A hard disc's sectors — and a
    # USB stick's, booted as one — are 512 bytes, so the
    # same descriptor stands at device sector 64 there.
    # AH=48 tells the measure; read_dap translates every
    # read by it (four device sectors to an ISO sector,
    # the address multiplied by four). If the question
    # fails, or the answer is anything but 512, the CD
    # measure stands — the road this loader has always
    # walked, byte for byte as before.
    mov word ptr [drvparams], 30
    mov si, offset drvparams
    mov ah, 0x48
    mov dl, [bootdrive]
    int 0x13
    jc sec_known
    cmp word ptr [drvparams + 24], 512
    jne sec_known
    mov word ptr [sec_mult], 4
    mov byte ptr [sec_shift], 2
sec_known:

    # A20: the fast gate at port 0x92.
    in al, 0x92
    or al, 2
    and al, 0xFE
    out 0x92, al

    # ---- the volume descriptor: LBA 16 ----
    mov word ptr [dap_count], 1
    mov word ptr [dap_buf_off], 0x1000
    mov word ptr [dap_buf_seg], 0
    mov dword ptr [dap_lba], 16
    mov dword ptr [dap_lba + 4], 0
    call read_dap
    jc fail_disc
    cmp byte ptr [0x1000], 1
    jne fail_disc
    # (the "CD001" mark, checked byte by byte)
    cmp byte ptr [0x1001], 0x43   # 'C'
    jne fail_disc
    cmp byte ptr [0x1002], 0x44   # 'D'
    jne fail_disc
    cmp byte ptr [0x1003], 0x30   # '0'
    jne fail_disc
    cmp byte ptr [0x1004], 0x30   # '0'
    jne fail_disc
    cmp byte ptr [0x1005], 0x31   # '1'
    jne fail_disc

    # The root directory's record stands at 0x1000 + 156:
    # its extent (LBA) at +2, its length at +10.
    mov eax, dword ptr [0x1000 + 156 + 2]
    mov [dir_lba], eax
    mov eax, dword ptr [0x1000 + 156 + 10]
    mov [dir_len], eax

    # Find BOOT in the root.
    mov si, offset name_boot
    call find_in_dir
    jc fail_files
    mov [dir_lba], eax
    mov eax, [found_len]
    mov [dir_len], eax

    # The five files, each staged.
    mov si, offset name_kernel
    call find_in_dir
    jc fail_files
    mov edi, 0x40000
    call stage_file
    jc fail_disc
    mov eax, [found_len]
    mov [kernel_len], eax

    mov si, offset name_settings
    call find_in_dir
    jc fail_files
    mov edi, 0x90000
    call stage_file
    jc fail_disc
    mov eax, [found_len]
    mov [settings_len], eax

    mov si, offset name_feather
    call find_in_dir
    jc fail_files
    mov edi, 0x90800
    call stage_file
    jc fail_disc
    mov eax, [found_len]
    mov [feather_len], eax

    mov si, offset name_paint
    call find_in_dir
    jc fail_files
    mov edi, 0x92000
    call stage_file
    jc fail_disc
    mov eax, [found_len]
    mov [paint_len], eax

    mov si, offset name_calc
    call find_in_dir
    jc fail_files
    mov edi, 0x94000
    call stage_file
    jc fail_disc
    mov eax, [found_len]
    mov [calc_len], eax

    # ---- the memory map (int 15h, E820) ----
    # Each entry is laid in the multiboot shape: a size
    # word (20) first, then the BIOS's own twenty bytes.
    mov di, 0x4800
    xor ebx, ebx
    mov dword ptr [mmap_count], 0
mmap_loop:
    mov dword ptr [di], 20
    add di, 4
    mov eax, 0xE820
    mov ecx, 20
    mov edx, 0x534D4150
    int 0x15
    jc mmap_drop
    cmp eax, 0x534D4150
    jne mmap_drop
    add di, 20
    inc dword ptr [mmap_count]
    test ebx, ebx
    jnz mmap_loop
    jmp mmap_done
mmap_drop:
    sub di, 4
mmap_done:
    # mem_lower: KiB below 1 MiB, from the BIOS's own word.
    mov ah, 0x88
    int 0x15
    jc mmap_fig_default
    mov [mem_upper_kb], ax
    jmp mmap_fig_done
mmap_fig_default:
    mov word ptr [mem_upper_kb], 0
mmap_fig_done:

    # ---- does the system ask for a picture? ----
    # Its multiboot header stands in the staged file's
    # first 8192 bytes (the file begins with its ELF
    # header; the multiboot header rides in its first
    # segment): the mark 0x1BADB002, then its flags; the
    # third flag (4) is the video request, and the asked
    # shape stands at +32/+36/+40 from the mark.
    mov dword ptr [want_video], 0
    mov ax, 0x4000
    mov es, ax
    xor di, di
    mov ecx, 8192
mark_scan:
    cmp dword ptr es:[di], 0x1BADB002
    je mark_found
    add di, 4
    sub ecx, 4
    jnz mark_scan
    jmp video_decided
mark_found:
    mov [mb_off], di
    mov eax, dword ptr es:[di + 4]
    test eax, 4
    jz video_decided
    mov dword ptr [want_video], 1
video_decided:
    xor ax, ax
    mov es, ax

    cmp dword ptr [want_video], 0
    je info_lay
    call try_video
    # try_video sets video_ok when a mode was set and its
    # grant recorded into the fb_* words below.

info_lay:
    # ---- the multiboot information, at 0x4000 ----
    xor ax, ax
    mov es, ax
    mov di, 0x4000
    mov cx, 64
    xor ax, ax
    rep stosw
    # flags: memory (1) + modules (8) + map (64); the
    # picture grant adds 4096 when a mode was set.
    mov eax, 73
    cmp dword ptr [video_ok], 0
    je info_flags_done
    or eax, 4096
info_flags_done:
    mov dword ptr [0x4000], eax
    mov dword ptr [0x4004], 640
    mov eax, 0
    mov ax, [mem_upper_kb]
    mov dword ptr [0x4008], eax
    mov dword ptr [0x4014], 4          # mods_count (+20)
    mov dword ptr [0x4018], 0x4400     # mods_addr (+24)
    mov eax, [mmap_count]
    imul eax, 24
    mov dword ptr [0x402C], eax        # mmap_length (+44)
    mov dword ptr [0x4030], 0x4800     # mmap_addr (+48)
    # The module table: four entries of start, end, and
    # two quiet words. The modules are laid at 0x300000
    # on the far side; their lengths are known now.
    mov eax, 0x300000
    mov dword ptr [0x4400], eax
    add eax, [settings_len]
    mov dword ptr [0x4404], eax
    mov dword ptr [0x4408], 0
    mov dword ptr [0x440C], 0
    mov dword ptr [0x4410], eax
    add eax, [feather_len]
    mov dword ptr [0x4414], eax
    mov dword ptr [0x4418], 0
    mov dword ptr [0x441C], 0
    mov dword ptr [0x4420], eax
    add eax, [paint_len]
    mov dword ptr [0x4424], eax
    mov dword ptr [0x4428], 0
    mov dword ptr [0x442C], 0
    mov dword ptr [0x4430], eax
    add eax, [calc_len]
    mov dword ptr [0x4434], eax
    mov dword ptr [0x4438], 0
    mov dword ptr [0x443C], 0
    # The picture grant's fields, when there is one.
    cmp dword ptr [video_ok], 0
    je info_done
    mov eax, [fb_addr]
    mov dword ptr [0x4058], eax
    mov dword ptr [0x405C], 0
    mov eax, [fb_pitch]
    mov dword ptr [0x4060], eax
    mov eax, [fb_width]
    mov dword ptr [0x4064], eax
    mov eax, [fb_height]
    mov dword ptr [0x4068], eax
    mov al, [fb_bpp]
    mov byte ptr [0x406C], al
    mov byte ptr [0x406D], 1           # type: direct color
    mov al, [fb_rpos]
    mov byte ptr [0x4070], al
    mov al, [fb_rsize]
    mov byte ptr [0x4071], al
    mov al, [fb_gpos]
    mov byte ptr [0x4072], al
    mov al, [fb_gsize]
    mov byte ptr [0x4073], al
    mov al, [fb_bpos]
    mov byte ptr [0x4074], al
    mov al, [fb_bsize]
    mov byte ptr [0x4075], al
info_done:

    # ---- the step into 32-bit protected mode ----
    cli
    lgdt [gdtr]
    mov eax, cr0
    or eax, 1
    mov cr0, eax
    jmp 0x08:pm_entry

# ----------------------------------------------------------------
# read_dap: one read through the packet at 'dap'.
# Carries the BIOS's own verdict in the carry flag.
# The callers always fill dap_lba (in the ISO's 2048-byte
# reckoning) and dap_count (= 1) afresh before calling;
# the translation into the device's own sector measure
# (Stone 17: four 512-byte sectors on a hard disc or a
# stick, one 2048-byte sector on a CD) happens here, in
# the packet itself, and no caller reads the packet back.
read_dap:
    mov eax, [dap_lba]
    mov cl, byte ptr [sec_shift]
    shl eax, cl
    mov [dap_lba], eax
    mov ax, [sec_mult]
    mov [dap_count], ax
    mov si, offset dap
    mov ah, 0x42
    mov dl, [bootdrive]
    int 0x13
    ret

# ----------------------------------------------------------------
# find_in_dir: SI names the file (a counted, NUL-ended name
# in this loader's data, compared against each record's
# name up to any ';' — the disc's version mark). The
# directory is [dir_lba]/[dir_len]. On success: carry
# clear, EAX = the file's extent LBA, [found_len] its
# length. On failure: carry set.
find_in_dir:
    mov [want_name], si
    mov eax, [dir_lba]
    mov [scan_lba], eax
    mov eax, [dir_len]
    mov [scan_left], eax
scan_sector:
    cmp dword ptr [scan_left], 0
    jle scan_fail
    mov word ptr [dap_count], 1
    mov word ptr [dap_buf_off], 0x1000
    mov word ptr [dap_buf_seg], 0
    mov eax, [scan_lba]
    mov dword ptr [dap_lba], eax
    mov dword ptr [dap_lba + 4], 0
    call read_dap
    jc scan_fail
    mov bx, 0x1000
scan_record:
    mov al, byte ptr [bx]
    test al, al
    jz scan_sector_next
    # Compare the record's name (at +33, counted at +32)
    # with the wanted name, up to ';' or the count's end.
    mov si, [want_name]
    lea di, [bx + 33]
    movzx cx, byte ptr [bx + 32]
scan_cmp:
    test cx, cx
    jz scan_cmp_end
    mov al, byte ptr [di]
    cmp al, 0x3B          # ';'
    je scan_cmp_end
    cmp al, byte ptr [si]
    jne scan_next
    inc si
    inc di
    dec cx
    jmp scan_cmp
scan_cmp_end:
    cmp byte ptr [si], 0
    jne scan_next
    # A match: extent at +2, length at +10.
    mov eax, dword ptr [bx + 2]
    mov edx, dword ptr [bx + 10]
    mov [found_len], edx
    clc
    ret
scan_next:
    movzx ax, byte ptr [bx]
    add bx, ax
    cmp bx, 0x1800
    jb scan_record
scan_sector_next:
    inc dword ptr [scan_lba]
    sub dword ptr [scan_left], 2048
    jmp scan_sector
scan_fail:
    stc
    ret

# ----------------------------------------------------------------
# stage_file: EAX = the file's extent LBA, [found_len] its
# length, EDI = the flat staging address (a multiple of
# 64 KiB in segment terms: 0x40000, 0x70000, ...). Reads
# the file a sector at a time into its stage.
stage_file:
    mov [stage_lba], eax
    mov eax, edi
    shr eax, 4
    mov [stage_seg], ax
    mov word ptr [stage_off], 0
    mov eax, [found_len]
    add eax, 2047
    shr eax, 11
    mov [stage_left], eax
stage_loop:
    cmp dword ptr [stage_left], 0
    je stage_done
    mov word ptr [dap_count], 1
    mov ax, [stage_off]
    mov word ptr [dap_buf_off], ax
    mov ax, [stage_seg]
    mov word ptr [dap_buf_seg], ax
    mov eax, [stage_lba]
    mov dword ptr [dap_lba], eax
    mov dword ptr [dap_lba + 4], 0
    call read_dap
    jc stage_fail
    inc dword ptr [stage_lba]
    add word ptr [stage_off], 2048
    jnz stage_no_wrap
    add word ptr [stage_seg], 0x1000
stage_no_wrap:
    dec dword ptr [stage_left]
    jmp stage_loop
stage_done:
    clc
    ret
stage_fail:
    stc
    ret

# ----------------------------------------------------------------
# try_video: find and set the VESA mode the system's
# header asks for (its width/height/depth at the staged
# file's +36/+40/+44), with the linear framebuffer. On
# success [video_ok] = 1 and the fb_* words hold the
# grant; on any failure the machine simply stays as it
# is, in text mode, and [video_ok] stays 0 — the system
# will draw its text face, as it honestly does when no
# picture is granted.
#
# The witness fix (November 15, 2026) hardened this
# walk against the ways one machine's picture firmware
# honestly answers differently from another's:
#   - Both information blocks are WIPED before each
#     asking, and the controller is asked with the
#     "VBE2" mark standing in its block, the standard's
#     own way of asking for the full answer. A field a
#     firmware does not write now reads as the nothing
#     it is, never as a former mode's leavings — the
#     walk once read its grant out of a block it had
#     never cleared, so one mode's framebuffer address
#     or pitch could be inherited by the next.
#   - The depth asked for is read from the system's own
#     header, as the width and height always were,
#     instead of being assumed.
#   - A mode whose block carries no framebuffer address
#     is no grant at all (an older firmware's shape,
#     which cannot be drawn on): the walk goes on.
#   - The pitch is taken from the block's scan-line
#     field; when that stands at nothing, from its
#     linear scan-line field; when both stand at
#     nothing, it is reckoned from the shape itself.
#   - A set is believed only when the firmware, asked
#     which mode now stands, names the chosen one (or
#     cannot answer the asking at all, in which case
#     the set's own success is the evidence there is).
#   - The walk is bounded, so a broken mode list can
#     not hang the door.
try_video:
    mov dword ptr [video_ok], 0
    # The controller's word (int 10h, AX=4F00), asked
    # into a wiped block with the "VBE2" mark standing
    # in it.
    mov di, 0x2000
    mov cx, 256
    xor ax, ax
    rep stosw
    mov dword ptr [0x2000], 0x32454256   # "VBE2"
    mov ax, 0x4F00
    mov di, 0x2000
    int 0x10
    cmp ax, 0x004F
    jne video_out
    cmp dword ptr [0x2000], 0x41534556   # "VESA"
    jne video_out
    # The mode list: a far pointer at +14.
    mov ax, [0x2000 + 16]
    mov [mode_ptr_seg], ax
    mov ax, [0x2000 + 14]
    mov [mode_ptr_off], ax
    mov word ptr [walk_left], 512
video_mode_loop:
    cmp word ptr [walk_left], 0
    je video_out
    dec word ptr [walk_left]
    mov es, [mode_ptr_seg]
    mov bx, [mode_ptr_off]
    mov ax, word ptr es:[bx]
    cmp ax, 0xFFFF
    je video_out
    add word ptr [mode_ptr_off], 2
    mov [mode_try], ax
    # The mode's own word (AX=4F01) — its block is
    # written to ES:DI, so ES goes back to this loader's
    # own page first, and the block is wiped before the
    # asking, so the answer is this mode's alone.
    mov cx, ax
    xor ax, ax
    mov es, ax
    mov di, 0x2200
    push cx
    mov cx, 128
    xor ax, ax
    rep stosw
    pop cx
    mov ax, 0x4F01
    mov di, 0x2200
    int 0x10
    cmp ax, 0x004F
    jne video_mode_loop
    # Its shape against the asking (the staged system's
    # header, read through its own segment, at the
    # offset the mark was found):
    push es
    mov ax, 0x4000
    mov es, ax
    mov di, [mb_off]
    mov dx, word ptr es:[di + 36]
    mov [ask_width], dx
    mov dx, word ptr es:[di + 40]
    mov [ask_height], dx
    mov dx, word ptr es:[di + 44]
    mov [ask_depth], dl
    pop es
    mov ax, [0x2200 + 18]
    cmp ax, [ask_width]
    jne video_mode_loop
    mov ax, [0x2200 + 20]
    cmp ax, [ask_height]
    jne video_mode_loop
    mov al, [0x2200 + 25]
    cmp al, [ask_depth]
    jne video_mode_loop
    # Attributes: supported (1) and a linear framebuffer
    # offered (128); memory model 6 (direct color).
    mov ax, [0x2200]
    test ax, 1
    jz video_mode_loop
    test ax, 128
    jz video_mode_loop
    cmp byte ptr [0x2200 + 27], 6
    jne video_mode_loop
    # A grant must carry its framebuffer: a block with
    # no address in it is an older firmware's shape,
    # which no one can draw on.
    cmp dword ptr [0x2200 + 40], 0
    je video_mode_loop
    # This is the mode. Set it, with its framebuffer.
    mov bx, [mode_try]
    or bx, 0x4000
    mov ax, 0x4F02
    int 0x10
    cmp ax, 0x004F
    jne video_out
    # And believe the set only when the firmware, asked
    # which mode now stands (AX=4F03), names this one.
    # A firmware that cannot answer the asking at all
    # is not held to it: the set's own success stands.
    mov ax, 0x4F03
    int 0x10
    cmp ax, 0x004F
    jne grant_record
    mov ax, bx
    and ax, 0x3FFF
    cmp ax, [mode_try]
    jne video_mode_loop
grant_record:
    # Record the grant.
    mov eax, dword ptr [0x2200 + 40]
    mov [fb_addr], eax
    # The pitch: the block's scan-line field; when it
    # stands at nothing, its linear scan-line field;
    # when both stand at nothing, the shape's own
    # reckoning — width by depth, in bytes.
    movzx eax, word ptr [0x2200 + 16]
    test eax, eax
    jnz pitch_recorded
    movzx eax, word ptr [0x2200 + 50]
    test eax, eax
    jnz pitch_recorded
    movzx eax, byte ptr [0x2200 + 25]
    shr eax, 3
    movzx edx, word ptr [0x2200 + 18]
    imul eax, edx
pitch_recorded:
    mov [fb_pitch], eax
    movzx eax, word ptr [0x2200 + 18]
    mov [fb_width], eax
    movzx eax, word ptr [0x2200 + 20]
    mov [fb_height], eax
    mov al, [0x2200 + 25]
    mov [fb_bpp], al
    mov al, [0x2200 + 32]
    mov [fb_rpos], al
    mov al, [0x2200 + 31]
    mov [fb_rsize], al
    mov al, [0x2200 + 34]
    mov [fb_gpos], al
    mov al, [0x2200 + 33]
    mov [fb_gsize], al
    mov al, [0x2200 + 36]
    mov [fb_bpos], al
    mov al, [0x2200 + 35]
    mov [fb_bsize], al
    mov dword ptr [video_ok], 1
video_out:
    xor ax, ax
    mov es, ax
    ret

# ----------------------------------------------------------------
# The failure words: plain, on the text screen, and stop.
fail_services:
    mov si, offset msg_services
    jmp fail_say
fail_disc:
    mov si, offset msg_disc
    jmp fail_say
fail_files:
    mov si, offset msg_files
    jmp fail_say
fail_say:
    mov ax, 0xB800
    mov es, ax
    xor di, di
    mov ah, 0x07
fail_char:
    lodsb
    test al, al
    jz fail_stop
    stosw
    jmp fail_char
fail_stop:
    cli
    hlt
    jmp fail_stop

# ----------------------------------------------------------------
# 32-bit protected mode: lay the system, lay the modules,
# hand over.
    .code32
pm_entry:
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x8F000

    # The system's segments, from its ELF header at its
    # stage (0x40000): program headers at e_phoff (+28),
    # of e_phentsize (+42) bytes, e_phnum (+44) of them.
    # Each PT_LOAD (type 1): copy p_filesz (+16) bytes
    # from stage + p_offset (+4) to p_paddr (+12), and
    # wipe the rest of p_memsz (+20).
    mov esi, 0x40000
    movzx ecx, word ptr [esi + 44]
    movzx eax, word ptr [esi + 42]
    mov edx, dword ptr [esi + 28]
    add edx, esi
ph_loop:
    test ecx, ecx
    jz ph_done
    cmp dword ptr [edx], 1
    jne ph_next
    push ecx
    push edx
    mov esi, 0x40000
    add esi, dword ptr [edx + 4]
    mov edi, dword ptr [edx + 12]
    mov ecx, dword ptr [edx + 16]
    rep movsb
    mov ecx, dword ptr [edx + 20]
    sub ecx, dword ptr [edx + 16]
    xor eax, eax
    rep stosb
    pop edx
    pop ecx
ph_next:
    movzx eax, word ptr [0x40000 + 42]
    add edx, eax
    dec ecx
    jmp ph_loop
ph_done:

    # The modules, in a row at 0x300000.
    mov esi, 0x90000
    mov edi, 0x300000
    mov ecx, [settings_len]
    rep movsb
    mov esi, 0x90800
    mov ecx, [feather_len]
    rep movsb
    mov esi, 0x92000
    mov ecx, [paint_len]
    rep movsb
    mov esi, 0x94000
    mov ecx, [calc_len]
    rep movsb

    # Hand over.
    mov eax, dword ptr [0x40000 + 24]   # the entry
    mov ebx, 0x4000
    mov ecx, 0x2BADB002
    xchg eax, ecx
    jmp ecx

# ----------------------------------------------------------------
# The gate's table.
    .align 8
gdt:
    .quad 0
    .quad 0x00CF9A000000FFFF   # code: flat, 32-bit
    .quad 0x00CF92000000FFFF   # data: flat
gdtr:
    .word 23
    .long gdt

# The disc address packet.
    .align 4
dap:
    .byte 16
    .byte 0
dap_count:
    .word 0
dap_buf_off:
    .word 0
dap_buf_seg:
    .word 0
dap_lba:
    .quad 0

# The doorman's own keeping.
bootdrive:
    .byte 0
# The device's sector measure (Stone 17): how many
# device sectors make one ISO sector (1 on a CD, 4 on
# a hard disc or a stick), and the shift that reckons
# an ISO sector address into a device address.
sec_mult:
    .word 1
sec_shift:
    .byte 0
    .align 4
drvparams:
    .fill 64, 1, 0
    .align 4
dir_lba:
    .long 0
dir_len:
    .long 0
found_len:
    .long 0
want_name:
    .word 0
scan_lba:
    .long 0
scan_left:
    .long 0
stage_lba:
    .long 0
stage_seg:
    .word 0
stage_off:
    .word 0
stage_left:
    .long 0
kernel_len:
    .long 0
settings_len:
    .long 0
feather_len:
    .long 0
paint_len:
    .long 0
calc_len:
    .long 0
mmap_count:
    .long 0
mem_upper_kb:
    .word 0
want_video:
    .long 0
video_ok:
    .long 0
mode_ptr_off:
    .word 0
mode_ptr_seg:
    .word 0
mode_try:
    .word 0
mb_off:
    .word 0
ask_width:
    .word 0
ask_height:
    .word 0
walk_left:
    .word 0
fb_addr:
    .long 0
fb_pitch:
    .long 0
fb_width:
    .long 0
fb_height:
    .long 0
fb_bpp:
    .byte 0
fb_rpos:
    .byte 0
fb_rsize:
    .byte 0
fb_gpos:
    .byte 0
fb_gsize:
    .byte 0
fb_bpos:
    .byte 0
fb_bsize:
    .byte 0
ask_depth:
    .byte 0

name_boot:
    .asciz "BOOT"
name_kernel:
    .asciz "CARDNULL.ELF"
name_settings:
    .asciz "SETTINGS.BIN"
name_feather:
    .asciz "FEATHER.FEA"
name_paint:
    .asciz "PAINT.FEA"
name_calc:
    .asciz "CALC.FEA"

msg_services:
    .asciz "Cardnull could not start: this machine's disc services are not the extended kind it needs."
msg_disc:
    .asciz "Cardnull could not start: the disc could not be read as its own."
msg_files:
    .asciz "Cardnull could not start: the disc does not carry the system whole."
