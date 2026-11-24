# Cardnull's own EFI doorman — the handover (Stone 16;
# the witness fix, November 15, 2026). Public domain,
# like everything in Cardnull.
#
# The last step of boot/cardnull-efi.c: the firmware
# runs its applications in its own 64-bit world — long
# mode, its page tables, its arrangements — but the
# system is handed over the multiboot way, as at the
# BIOS door: 32-bit protected mode, paging off,
# interrupts off, the multiboot mark in EAX and the
# information's address in EBX. This small piece of
# assembly walks the machine down from the one world
# into the other:
#
#   1. It takes the system's entry and the information's
#      address from its caller (the firmware's calling
#      way: the two words arrive in RCX and RDX) and
#      keeps them in EDI and ESI, which the walking down
#      does not spend.
#   2. It lays its own gate table — the BIOS doorman's
#      very descriptors: a flat 32-bit code and a flat
#      32-bit data — and makes a far return through the
#      code gate, which lands it in the gate's
#      compatibility reach: still the firmware's paging,
#      but 32-bit code now.
#   3. There it turns paging off at CR0 — the step that
#      truly leaves the firmware's world — then turns
#      off the long-mode reach itself (CR4's PAE and
#      the EFER's LME), as the architecture's own order
#      prescribes.
#   4. It lays the data gates, sets the stack on the page
#      this doorman claimed for it from the firmware
#      (0x8F000, claimed as loader data before the boot
#      services were left — this door's own ground; the
#      BIOS doorman keeps his own stack at 0x3F000 since
#      Stone 41), puts the mark in EAX and the
#      information in EBX, and jumps to the system's
#      entry. It never returns.
#
# The witness fix (November 15, 2026): this code once
# ran where the firmware had laid the doorman's own
# image, and its header trusted that ground to stand
# low — "the firmware lays its applications in the
# machine's low memory, as the bench's firmware does."
# On Tyler's machine the trust broke: a firmware is
# free to lay the image ABOVE the four-billion line
# (the bench's own firmware does exactly that on the
# q35 machine shape), and up there the far return of
# step 2 lands in 32-bit compatibility reach, where an
# instruction pointer is thirty-two bits wide — the
# high half of the code's address falls away, and the
# processor walks off into whatever stands at the
# truncated address. The machine never reaches the
# system at all: a black screen that no key can wake,
# which is what the witness reported at this door.
#
# So the handover now stands as one self-carrying
# piece — its code, its gate table, and the gate's
# pointer all inside the span from cardnull_tramp_start
# to cardnull_tramp_end, every inner address reckoned
# from the instruction pointer at the run, never from
# where a linker laid it. The doorman copies the piece
# whole onto a low page it claims for the purpose
# (0x8E000, claimed as loader code) and calls it THERE,
# so the walking down always stands on low ground of
# Cardnull's own choosing, wherever the firmware laid
# the rest.

    .text
    .globl cardnull_tramp_start
    .globl cardnull_tramp_end
    .globl cardnull_handoff
cardnull_tramp_start:
cardnull_handoff:
    cli
    movl %ecx, %edi
    movl %edx, %esi
    leaq tramp_gdt(%rip), %rax
    leaq tramp_gdt_ptr(%rip), %rcx
    movq %rax, 2(%rcx)
    lgdt (%rcx)
    pushq $0x08
    leaq tramp_compat(%rip), %rax
    pushq %rax
    lretq

    .code32
tramp_compat:
    movl %cr0, %eax
    andl $0x7FFFFFFF, %eax
    movl %eax, %cr0
    movl %cr4, %eax
    andl $0xFFFFFFDF, %eax
    movl %eax, %cr4
    movl $0xC0000080, %ecx
    rdmsr
    andl $0xFFFFFEFF, %eax
    wrmsr
    movw $0x10, %ax
    movw %ax, %ds
    movw %ax, %es
    movw %ax, %fs
    movw %ax, %gs
    movw %ax, %ss
    movl $0x8F000, %esp
    movl $0x2BADB002, %eax
    movl %esi, %ebx
    jmp *%edi

# The gate's table: the BIOS doorman's own descriptors
# (boot/cardnull-boot.asm) — nothing, a flat 32-bit
# code, a flat 32-bit data. It stands inside the piece,
# and the pointer above it is patched at the run to
# name THIS copy of the table, wherever it was laid.
    .balign 8
tramp_gdt:
    .quad 0
    .quad 0x00CF9A000000FFFF
    .quad 0x00CF92000000FFFF
tramp_gdt_ptr:
    .word 23
    .quad 0
cardnull_tramp_end:
