# Cardnull's own EFI doorman — the handover (Stone 16).
# Public domain, like everything in Cardnull.
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
#   4. It lays the data gates, sets the stack where the
#      BIOS doorman sets his (0x8F000), puts the mark in
#      EAX and the information in EBX, and jumps to the
#      system's entry. It never returns.
#
# The code's own address must stand where 32-bit code
# can reach it — the firmware lays its applications in
# the machine's low memory, as the bench's firmware
# does; the doorman's proof is that road, driven.

    .text
    .globl cardnull_handoff
cardnull_handoff:
    cli
    movl %ecx, %edi
    movl %edx, %esi
    leaq gdt_ptr(%rip), %rax
    lgdt (%rax)
    pushq $0x08
    leaq compat(%rip), %rax
    pushq %rax
    lretq

    .code32
compat:
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
# (boot/cardnull-boot.asm) — nothing, a flat 32-bit code,
# a flat 32-bit data.
    .data
    .balign 8
gdt:
    .quad 0
    .quad 0x00CF9A000000FFFF
    .quad 0x00CF92000000FFFF
gdt_ptr:
    .word 23
    .quad gdt
