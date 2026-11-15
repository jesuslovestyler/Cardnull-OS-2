# Cardnull OS 2

**The operating system of [Cardnull](https://cardnull.com), written in
[Nifla](https://github.com/jesuslovestyler/Nifla) — public domain at every
layer: the language and the system together.**

Cardnull OS 2 is a Christian operating system, built from scratch in Nifla,
Cardnull's own public-domain programming language. Nothing underneath it is
borrowed: no licensed kernel, no licensed language, no runtime carrying
someone else's terms. What is here is given away, free for anyone to read,
learn from, copy, and build on, forever.

It is the successor to the [first Cardnull OS](https://github.com/jesuslovestyler/Cardnull-OS),
which was written in Swift, reached a complete desktop (milestones M1–M38),
and was retired on November 14, 2026 so that this one could be built in
Cardnull's own language instead. The first system's work is not lost — its
lessons are this one's blueprint — and its repository stands as the
permanent public-domain record of it.

Founded November 15, 2026, by Tyler Austin James Kovalevich, in
Washington, North Carolina.

> *Unless Yahweh builds the house, they labor in vain who build it.*
> — Psalm 127:1 (World English Bible)

## Building

The compiler belongs to the language, not to this repository: you need a
checkout of [Nifla](https://github.com/jesuslovestyler/Nifla) beside this
one. By default the build looks for it at `~/workspace/nifla-repo`; set
`NIFLA_REPO` to point somewhere else.

```
./build.sh            # makes build/cardnull.elf, build/welcome.feather
                      # (the feather with its card, by the compiler's
                      # feather mode), and the disc's one small module
                      # (build/settings.bin)
```

The result is a bare-metal program: it boots on its own, with no operating
system underneath. The proofs boot it in QEMU with no display and read the
emulated screen's memory back through the QEMU monitor — the same bench
pattern the Nifla language's own bare-metal proofs use:

```
./prove-stone1.sh     # one script per stone; each prints PASS or FAIL
```

QEMU is the bench's extracted QEMU 10 (`~/qemu10-root`) when present; set
`QEMU` to a plain `qemu-system-x86_64` command line if yours is installed.

To build the bootable witness disc (see "The witness disc" below):

```
./build-iso.sh        # makes dist/cardnull-os-2.iso
./prove-iso.sh        # boots the ISO itself, three ways, and reads the screens
./build-stick.sh      # makes dist/cardnull-stick.img (Stone 17)
```

## The stones

The system is built stone by stone, in order. Each stone is proven on the
bench before the next begins, and its honest limits are written down here.

### Founding (November 15, 2026)

This repository, the license, the build, and the proof bench. No system
code yet — the first stone is the first boot.

### Stone 1 — First boot

The seed kernel (`src/cardnull.nifla`) boots on its own, greets the
person in plain words — "Cardnull", a welcome, and the machine's memory
reported plainly from the loader's memory map — and then stays alive,
sleeping between timer ticks. Proven by `prove-stone1.sh`: booted
headless with 96 MiB, the screen read back the greeting and the figure
100,137,984 bytes (95 megabytes), the usable sum for that machine.

Honest limits: the greeting is three lines and the machine then simply
waits — it cannot hear the keyboard yet (Stone 2), has no face (Stone 3),
and the clock the tick makes possible is not shown yet. The memory
figure is the loader map's usable sum, which is always a little less
than the machine's whole memory; the firmware's reserved stretches are
not counted, and nothing here manages memory beyond reading the map.

### Stone 2 — Ears

The keyboard is heard. A typing line lives on the screen's last row:
letters echo as they are typed, Backspace un-types, and Enter offers
the word to a small command loop that answers in plain words — `hello`
(a greeting back), `time` (the seconds since the machine woke, from
the timer tick), `memory` (the memory figure), and `clear` (the screen
is wiped). Any other word is answered kindly: "I don't know that word
yet. Try hello, time, memory, or clear." Proven by `prove-stone2.sh`:
it types "hellx", erases the x, finishes "hello", and reads every
answer back off the emulated screen, including that the machine still
answers after a clear.

Honest limits: the machine knows only single lowercase words — no
capital letters (there is no shift state yet), no digits in words, and
no commands with parts. Answers appear where the screen's writing
cursor stands and scroll as they accumulate; after `clear`, the
greeting is gone until the next boot and later answers appear wherever
that cursor had reached. The face (Stone 3) gives answers a proper
home. Keystrokes are gathered in a 48-number buffer; a longer word is
simply not gathered further. (`prove-stone2.sh` describes this
pre-face screen; from Stone 3 on, its command checks live on in the
later proofs, against the faced screen.)

### Stone 3 — A face

The desktop. The system's own screen library (`src/screenlib.nifla`,
joined as a prelude) paints a top bar — "Cardnull" at the left and a
live clock at the right, white on blue — and a welcome panel in the
middle, black on light gray, saying what this is, that it is public
domain and free for everyone, and carrying the founding verse
(Psalm 127:1). Answers now have their own region of the screen and
scroll within it; the typing line still works at the bottom with the
same four words, and `clear` now restores the whole face and empties
the answers. Proven by `prove-stone3.sh`: full-screen readback
verified the bar and panel text, their color bytes (31 and 112), and
the clock advancing between two readings (00:00:00 → 00:00:02), and
the commands answering in their region.

Honest limits: the clock counts from the moment the machine woke —
it is an honest count of uptime, not the world's time; nothing reads
a real-time clock yet, and Stone 4's time choice shifts the
shown hour without changing that. The face is drawn in the text
screen's sixteen colors, one panel, no windows, no mouse. The panel
and bar are repainted only when drawn; a feather or a stray writer
could paint over them, and nothing yet defends the arrangement
except the system's own manners.

### Stone 4 — The clock's time choice

The clock's hour offset is a choice made in plain words: `eastern`
(the system's home time, five hours behind the world's standard) and
`utc` (the world's standard time itself). What the choice starts
from is carried by the system disc itself: a small settings module
rides beside the system (the letters C and N, then one byte holding
the offset with 64 added), the bootloader brings it with the system
at boot, and the bar's clock applies it. The disc as built carries
Eastern; a disc carrying no choice also starts on Eastern — the
first Cardnull OS taught this lesson on real hardware, where its
clock quietly showed the world's standard hour as if it were local,
and this system was designed so as never to repeat it. The words
`eastern` and `utc` change the choice for the session, and the
machine says exactly how long that lasts: until the machine is
turned off.

Proven by `prove-stone4.sh`, three boots with the modules a
bootloader brings (QEMU's `-initrd` is the bench form of the same
handoff): a disc carrying the world's time comes up at hour 00 on
its own and `eastern` moves it to 19; a disc carrying Eastern comes
up at 19 and `utc` moves it to 00; and with no modules at all, the
clock starts on Eastern and `feather` is answered plainly.

How this stone came to its present shape, recorded honestly: it was
first built and proven earlier the same day (November 15, 2026)
with the choice kept on an attached disk, read back at every boot —
that build stands in this repository's history (commit `b20761e`).
Tyler then corrected the shape the same morning: the system ships
as **one disc and nothing else** — "we should've built the iso from
day one like the first OS" — and a read-only disc cannot remember
across reboots. So the disk arrangement was retired before it ever
shipped, and the choice was re-pointed to the disc itself, as
above. What the correction cost, stated plainly: **the choice is
no longer remembered across reboots.** To start on a different
time, the disc itself must be laid with that choice in its
settings; within a session, the words still change it.

Honest limits, stated exactly: there is still no reading of the
world's clock — the count is the time since the machine woke, and
the offset shifts only the hour the face shows, the way setting a
clock does; nothing here knows the date or the world's present hour.
The settings are in the system's own small form (the letters C and
N and one byte), not in any standard format another system would
read. And because the loader leaves its module table in low memory
that the system's heap also grows into, the system lifts everything
it needs out of the modules in its first breath, before anything
else is allocated — see the builder note below.

### Stone 5 — First guest

A guest comes to visit. The welcome guest (`src/welcome-guest.nifla`)
is a second program, written in Nifla and built for the guest
doorstep at 2 MiB; it rides the disc as a module, and its card —
its length and its FNV-1a checksum — rides as a small module of its
own. At boot the system lifts both into its own keeping. The new
word `guest` then receives it: the system reckons the lifted
image's checksum with its own hand, and only if it matches the
card does it lay the image at the doorstep and call it. The guest
paints its own panel inside the desktop — rows 15–19, in its own
color, white on green — with its name and two plain lines, returns
the number it was handed, doubled, and goes home; the system notes
the visit in its own line below the panel and carries on. A guest
whose bytes do not match its card is refused in plain words ("The
guest on this disc is not whole, so it was not let in") and never
runs. Proven by `prove-stone5.sh`: one boot shows, in order down
the screen, the desktop, the guest's panel in its color, and the
system's continuation line; a second boot, with one byte of the
guest flipped, shows the refusal, no trace of the guest or its
color anywhere, and the desktop unharmed. (The door was first
proven earlier the same day with the guest staged from a scratch
disk; Tyler's one-disc correction re-pointed it to the disc before
this stone was committed, and it was re-proven in its shipped
shape, as above.)

Honest limits: the guest door's honesty is the language's Stone 17
honesty, unchanged — there is no isolation yet: host and guest
share one privilege level and one memory, the checksum proves the
bytes match the card and nothing more (it is not a signature), and
a guest that faults stops the whole machine. The guest's panel is
a visit, not a fixture: later answers may write over the rows it
painted. The guest writes its lines letter by letter with the
floor, for the reason in the builder note below. And the layout
carries one plain assumption: a guest image is never as small as
the 512-byte settings or the 32-byte card, so a module of exactly
the card's promised length can only be the image.

*A note on this section's words (November 15, 2026): the
programs this section calls guests are called feathers
now — see the rename note at the end of Stone 10's
section. The section above keeps the words of its
morning, as the record of it.*

### Stone 6 — Ears on the USB road

A second road for typing. `src/usbkey.nifla` is a USB host
driver written in Nifla: it finds the machine's UHCI controller
on the PCI bus (the USB 1.1 companion road), raises it — the
reset sequence, a frame list and two queue heads laid in a desk
of bytes the main body hands it, the port reset in the first
Cardnull OS's own measures — and wakes what stands on a port in
plain USB words: its description read, an address given, its
arrangement read descriptor by descriptor until a boot
keyboard's interface is found by its declared numbers, the
arrangement set, the keyboard set to its boot manner, and its
report door armed. The main loop then polls that door whenever
the PS/2 road is quiet, reads each report for the presses that
are new in it, and turns HID usages into the same make codes
the PS/2 road speaks — so both roads feed the one typing line,
and neither disables the other. When a keyboard is ready the
desktop says so at boot ("A USB keyboard is ready."), and the
new word `usb` reports the road's standing, with its own count
of the keys it has brought.

Proven by `prove-stone6.sh`, three boots, all PASS: with a
controller and a USB keyboard, the ready word stands on the
desktop, `hello` is answered, and the `usb` word's count reads
10 — the ten presses of the two typed words and their Enters,
carried by the USB road itself (the count is the road's own;
the PS/2 road cannot raise it). With a controller but no
keyboard, and with no controller at all, the desktop comes up
unbothered, the PS/2 road answers as always, and `usb` answers
plainly that no USB keyboard is plugged in. The full earlier
proof set (Stones 3, 4, 5 and the ISO proof) passes unchanged
on the same build.

**Which USB this covers, plainly:** the proof covers the UHCI
companion road (USB 1.1) — in UTM, that is the **USB 2.0**
arrangement, whose keyboards stand on UHCI companions; turn
USB Support **on** and choose the USB 2.0 form if the machine
offers the choice. The USB 3.0 arrangement (an xHCI
controller) is **not** covered by this stone, and neither is a
standalone EHCI controller; on those, this system would find
no controller it speaks and the PS/2 road would carry typing
alone. Honest limits: the USB road's letters arrive unshifted
(no capitals yet — its table covers the letters, Enter,
Backspace, and Space, the words the desktop speaks today); one
keyboard is woken, the first found; and the driver polls its
door rather than taking interrupts. Two of the language's own
bounds were met and honored on the way: a call hands at most
six words' worth of values, so two of the driver's layings are
done in two calls each; and the driver's signatures carry
Stone 18 kind marks, so the shapes its floor desks are handed
are known from the start.

### Stone 7 — A true clock

The bar's clock stops counting from waking and tells the
world's time. At boot the system reads the machine's own
clock — the CMOS real-time clock every PC keeps — through
`src/rtclock.nifla`: the update-in-progress flag waited out,
the reading taken twice and required to agree, and the
clock's own status word honored, so its numbers are read
right whether they are spelled in packed decimal or plain
binary, and whether its hours run to 24 or to 12. The
reading becomes a count of seconds; the loop carries it
forward by the machine's own tick, and the disc's time
choice (Stone 4) is applied on top, as it always was. The
bar now shows the date in plain words beside the time —
"Sunday, November 15, 2026" — and the word `time` answers
with the real moment in words, the waking count still told
beneath it. Dates are reckoned with the civil calendar
arithmetic (days from a date and back, leap years and all),
so an offset that carries the moment over midnight carries
the date with it, in either direction.

Proven by `prove-stone7.sh`, three boots with the bench
clock pinned to known instants, all PASS: 14:32 UTC on
November 15, 2026 with the Eastern choice shows 09:32 on
Sunday, November 15 (and `time` tells the same in words);
02:00 UTC on November 16 with Eastern shows 21:00 on
Sunday, November 15 — the date carried back over midnight;
and 23:59:50 UTC with the world's choice rolls forward on
its own to Monday, November 16 at 00:00. Because the clock
is now real, the older proofs that reckon hours from the
time choice pin the bench clock (`RTC_BASE` in
`tools/launch.sh`; the ISO proof pins its own), and the
whole earlier proof set passes unchanged against it.

**The standing assumption, said out loud:** the machine's
clock is taken to hold **the world's standard time (UTC)** —
what QEMU and UTM set by default — and the time choice is
applied on top. On a machine whose clock instead held its
local time, the shown hour would stand off by the choice's
hours; if Tyler's witness on his own machine shows that,
the semantics get adjusted then, in the open. Honest
limits: the year is read as this century (the clock's
two-figure year, 2000 + it); the reading is taken once at
boot and carried by the tick, so a machine left running
for very long could drift from the clock it read; and if
no true reading can be had at boot, the bar quietly keeps
the honest count since waking, as it did before this
stone, and shows no date.

### Stone 8 — Remembers for real

The system can remember. When a hard disk is fitted, the
desktop offers it in plain words at boot ("A hard disk is
here. Type setup to let it remember your choices."), and
the word `setup` opens a typed gate — the first Cardnull
OS's W3 lesson kept: never a bare dead end, never a silent
format. The gate asks, "This will clear everything on the
disk. Type yes to go on," and only the exact word `yes`
begins: the disk's first sixty-four sectors (where a disk's
own name and arrangement live) are wiped, and the system's
card is written last and read back before the system calls
it done. Anything else at the gate leaves the disk exactly
as it was. From then on the disk keeps the settings — the
time choice first — on its card (sector 8: the letters C
and N and the choice byte, the shape the founding day's
first disk keeping was proven with), read at every boot in
preference to the disc's settings module; `eastern` and
`utc` write the new choice back and say so ("The disk will
remember it"), and with no disk keeping them they keep
their session-only wording, which is true there. The
language's `disksectors()` fresh-boot blindness is worked
around in the open, as before: the drive is selected first
(`src/diskkeep.nifla`'s small floor piece), then asked.

Proven by `prove-stone8.sh`, five boots, all PASS: one
blank disk lives three lives — offered, gated, given over,
`utc` kept (hour 00); booted again it overrules the disc's
Eastern and comes up at 00, and `eastern` is kept in turn;
a third boot comes up at 19, the write-back persisted both
ways. A second disk, offered and gated but answered `no`,
is byte-for-byte the image it was before (checked by hash).
With no disk at all, the disc's choice rules, no offer
stands, and `setup` answers plainly that there is no hard
disk here. The whole earlier proof set passes unchanged —
every earlier boot attaches no disk, which is itself the
no-disk case.

**Tyler's UTM arrangement for this stone:** alongside the
ISO (CD/DVD, as before), attach **one small blank disk
image as an IDE hard disk** — a few megabytes is plenty;
the system speaks to the master disk on the first IDE
channel. The desktop will offer it; type `setup`, then
`yes` at the gate, and from that boot on the machine
remembers its time choice across restarts. Honest limits:
only the time choice is kept so far (the card has room to
grow); the disk the system speaks to is an ATA (IDE) disk
— a disk attached as NVMe or virtio would not be seen by
this stone; and setup's clearing is the disk's first
sixty-four sectors plus the card — the disk is given over
wholly in intent and in its arrangement, though the system
does not scrub every sector of a large disk.

### Stone 9 — A face with light

The desktop leaves the text screen. The kernel now asks
its loader for a picture screen — 1024×768, thirty-two
bits a pixel (the asking is a compiler addition, recorded
in the Nifla repository: `niflac --bare --video` lays the
request in the kernel's multiboot header) — and when the
loader grants it, the desktop is **drawn**: the blue bar
with its title, date, and clock; the light-gray welcome
panel with its words; the invitation; the answers; the
typing line — all as light, in a hand-drawn 8×8 bitmap
font defined in `src/font.nifla` (ours, public domain,
drawn at twice size in 16-pixel letter cells) by the
drawing library `src/pixface.nifla`. The layout is the
text face's own, reckoned onto whatever grid the granted
screen makes, so the same desktop is drawn larger or
smaller on another screen. Answers wrap at the narrower
grid and scroll as before; the clock is drawn afresh each
second, as before.

Requested and granted, stated honestly: on the bench,
GRUB grants **exactly what was asked** — 1024×768×32,
its framebuffer standing at 0xFD000000, above the first
gigabyte the boot stub maps, so the kernel lays one more
page directory of its own to reach it. The colors are
composed from the field places the loader's answer names,
not assumed. QEMU's own `-kernel` loader grants no
picture at all — which is what the fallback is for.

**The fallback:** when no picture screen is granted, or
the grant is not of a shape this face can draw on (a
direct-color screen, thirty-two bits a pixel, its whole
address under four billion, at least 768×256), the system
does not halt or sit black: the text face — the system's
first face, unchanged — carries the desktop, and its
first answer line says so in plain words: "No picture
screen was granted, so this face stays in words."
`build.sh` also builds the kernel once without the asking
(`build/cardnull-text.elf`), and the disc laid down with
it proves the fallback exactly.

**The guest's visit in light:** the guest still paints a
text screen's cells — but on a machine showing a picture,
the text screen's memory is not a screen, and its cells
cannot be read back from it (measured on the bench: the
painting reads back as one repeated byte, lost among the
picture screen's own workings). So the door changed,
slightly and in the open: the host now tells the guest
which screen to paint, in a word laid at the top of the
guest's doorstep — the text screen's own address on a
text machine (the visit exactly as it always was), or the
address of a block of cells the host keeps, on a picture
machine. The host then draws those cells as light, in the
colors the guest itself chose. The guest's card, check,
and refusals are untouched.

**And the EFI door is healed.** The framebuffer kernel
is what the UEFI handoff needed: the hybrid disc (an EFI
system partition beside the BIOS boot image, GRUB at both
doors) now boots under OVMF to the same drawn desktop,
and the guest visits through that door too. One bench
finding rides with it: the EFI partition must be formed
as mtools forms a small image by default (FAT12) — a
partition forced to FAT32 at that size was measured to be
one the firmware would not boot. Tyler's UTM machine may
now keep its UEFI firmware.

Proven by `prove-stone9.sh`, four boots of ISO files:
the shipped disc through the BIOS door (the drawn
desktop, the typing echo, an answer in light, the drawn
clock's hand moving between two dumps, the guest's green
panel and white letters); a tampered-guest disc (the
refusal drawn, no green anywhere); the no-asking disc
(the text face and its plain-words line); and the shipped
disc through the EFI door, the same checks as the first
boot. The full earlier proof set still passes —
`prove-iso.sh` now reads the disc's words through the
same kernel's fallback text face on identical disc
layouts, as its header says.

Honest limits: no mouse yet; one resolution is asked
for, and another grant is drawn as it comes, but the
asking is fixed at 1024×768×32; the guest's cells are
composited once, when the visit ends — a guest that
painted and repainted would be shown only as it left
things; and the EFI door's loader is still GRUB — its
own replacement is future work, as the BIOS door's is
Stone 11's.

### Stone 10 — Guests that can be handed things

This stone set out to repair the language: the founding
morning's bench notes (kept in "Notes for builders"
below) recorded that a floor block in a guest program,
handed a piece of text or a block of bytes, was given a
desk whose length read as zero — which is why the
welcome guest painted its letters one by one as
immediate values. Measured again at this stone, shape
by shape, **the record did not hold**: a guest's floor
blocks receive handed text and bytes whole — pointer,
length, and letters — for a literal and a block handed
in the main body, for a function's own handed words
passed onward to its floor, for joined and returned
text, and for text handed with numbers to a small
painter, which wrote the line it was handed onto the
host's screen. The assembly the compiler writes for
the handing is the same for a guest as for a host. The
one refusal in the neighborhood — a library whose floor
tools' shapes no call has pinned — falls on host builds
identically, and is the checker's shape reckoning, not
a guest's wound (marks of kind, the language's Stone
18, are its standing cure, and the system's own
libraries carry them where they need them).

So the language needed no change, and none was made.
The full language suites were re-run and stand at their
Stone 18 counts (interpreted 39/39, compiled 112/112,
voice 6/6, self-hosted 39/39, the bare proofs all PASS),
and the verification itself now stands as a proof in
the language's repository (`run-bare-guest-desk.sh`),
so the claim is checkable rather than remembered.

What changed here is the guest: `src/welcome-guest.nifla`
is written plainly now — two small tools handed the
guest's words as text paint its panel and its three
lines, at the screen the doorstep word names (Stone 9).
Its header tells the story, and the founding note in
"Notes for builders" carries this correction beside it,
as corrections are kept in this house: in the open,
dated, next to the words they correct.

Proven by the shipped proofs that cover the guest —
`prove-stone5.sh` (the visit and the tamper refusal),
`prove-iso.sh`, and `prove-stone9.sh` (the visit drawn
in light, at both doors) — all PASS with the guest in
its new shape.

**The rename (November 15, 2026).** Later on the
founding day Tyler restored the name these programs
were always meant to carry: *"Can you name them
feathers instead? Just name them feathers because
that was the original plan of Cardinal OS."* Feathers
are Cardnull's programs, written in Nifla — the
original Cardinal OS plan's name for its programs,
kept from the first Cardnull OS, whose programs were
plain-text feathers with their cards. So the word is
feather now, everywhere the person at the screen
reads: the command is `feather` (the old word `guest`
answers in plain words, "Programs are called feathers
here — type feather."), the window is the feather's,
the messages speak of the feather, and the sources
and the disc follow — `src/welcome-feather.nifla`,
`src/featherdoor.nifla`, and the module `feather.bin`
on the disc, checked against the feather's card as
before. The sections above (Stones 5 and 10, and the
ladder's history between them) keep the words of
their morning; everything that speaks of the system
as it now stands speaks of feathers. One layer
deliberately keeps the old word: Nifla's own
language-level words for this door — `callguest`,
`guestvalue`, `guestgive`, and the `--guest` building
flag — are the language's plumbing, not the system's
names, and they stay unchanged underneath, as does
the language repository's own proof of the doorstep
(`run-bare-guest-desk.sh` there).

### Stone 11 — Our own doorman

The BIOS door is Cardnull's own now. `boot/cardnull-boot.asm`
is a bootloader written for this repository (assembly,
public domain like everything here): one stage of some
1,950 bytes that the El Torito catalog lays at the
doorstep whole. It checks the machine's extended disc
services, walks the disc's own ISO9660 tree to find
`/boot/cardnull.elf` and the three modules, stages them
in low memory, gathers the machine's memory map in
multiboot shape, and — when the system's header asks
for a picture — finds and sets the VESA mode that
matches the asking and records the grant. Then it steps
into protected mode, lays the system's ELF segments and
the modules where the multiboot word expects them, and
hands over exactly as GRUB did: the magic in EAX, the
information (flags, memory, the module table, the map,
and the framebuffer fields when granted) at 0x4000, the
entry from the system's own header. When something is
missing it says so in plain words on the text screen —
"Cardnull could not start: …" — and halts; it never
guesses.

What stands at each door after this stone, plainly:
**the BIOS door is Cardnull's own bootloader; the EFI
door is still GRUB** (its own replacement is a future
stone). GRUB's BIOS image is gone from the disc — the
El Torito catalog's BIOS image is `/boot/boot.img`, this
loader and nothing else. One bench finding rides with
the EFI door: its GRUB resolves its root to the disc
itself, so it reads its seven lines of directions from
the disc's own `/boot/grub/grub.cfg`; that text file
stands on the disc for it, and a copy rides in the EFI
partition as well. It is directions, not a piece of
GRUB, and the BIOS door never touches it.

Two wounds from the building are recorded because they
are the kind that bite quietly. The loader first wrote
the module count and table address at offsets +28 and
+32 in the boot information, where the system reads
them at +20 and +24: the
system came up but read no modules at all — the disc's
time choice silently became the built-in default, and
there was "no guest on this disc". And the modules'
first staging addresses (0x50000 and upward) sat inside
the system's own stage — the system is some 123 KiB, so
its stage reaches past 0x5E000 — and each module's
sector read splashed 2,048 bytes over the staged
system's tail. The text face survived it by luck (the
splashed bytes are largely the system's own, from
nearby in the disc's stream); the drawn face did not —
its font and layout code stands in that tail, and the
machine fell executing the settings module's letters.
The stages now stand at 0x60000 and upward, above the
system's stage, and the staged bytes were verified
against the file byte for byte on the bench.

Proven by booting the finished ISO itself:
`prove-iso.sh` (the text face through our loader —
desktop, the disc's carried time choice, the guest's
visit, the world's-time variant, the tamper refusal)
and `prove-stone9.sh` (the drawn desktop through our
loader with the picture the loader itself granted, the
refusal drawn in light, the text fallback, and the EFI
door's boot unchanged) — all PASS, and the whole
earlier set (Stones 3–8) still passes with them.

Honest limits: the loader speaks the BIOS's extended
disc services and ISO9660 only, and loads the four
files it knows by name from `/boot`; the picture grant
is VESA VBE on the BIOS door — a machine whose BIOS
offers no matching mode gets the text face, said in
plain words, exactly as before. The EFI door's own
Cardnull loader is future work.

### Stone 12 — Real typing

The typing line learns the whole board. The shift keys
and Caps Lock speak on **both** roads: the roads share
one key numbering, so one shift standing in the main
body serves both — the PS/2 road's own numbers for its
shifts (42 and 54 down, 170 and 182 up, 58 for Caps
Lock's press) are the numbers the USB road now speaks
too, its reports' modifier byte turned into those same
numbers when the standing changes (`src/usbkey.nifla`),
and its Caps Lock usage translated like any other key.
When a key is pressed, its standing is resolved at that
moment — the shift keys, with Caps Lock folded in for
the letters alone — and kept beside the key, so the
line is always rebuilt exactly as it was typed: a shift
taken later never rewrites a letter already standing.
The letter table (`charFor` in the main body) now knows
the figures and their shifted marks and the marks
between the letters, as well as the capitals; the pixel
face's font has carried every one of those shapes since
Stone 9.

And a typed line may hold more than one word now. Its
**first word is its command word**, answered exactly as
a one-word line always was — the single-word commands
behave byte-identically, the setup gate included: the
gate still asks for the exact word `yes` as the whole
line, and a line of `yes` followed by anything is not
the gate's word. The rest of the line is kept whole in
the main body's keeping (`linerest`), as handed text
for the words that want it — Stone 15's notes are the
first taker.

Proven by `prove-stone12.sh`, two boots: on the PS/2
road, a shifted sentence ("Hello Cardnull") read back
off the typing line exactly, a two-word line answered
by its first word, `hello world` answered as `hello`,
Caps Lock's capitals and their turning off, a figure
and its shifted mark (`a1!`), and `memory` answered as
it always was. On the USB road, the same grammar from
the keyboard's own reports — the count in the `usb`
word's answer (10) is the road's own evidence, as at
Stone 6 — with Caps Lock making its capitals by its
usage. The whole earlier proof set passes unchanged.

Honest limits: the line still gathers at most 48 keys,
so a line — and with it a note's text — is at most 48
letters long; the keypad and the keys beyond the common
board (function keys, the arrows) are not spoken yet;
and a capital command word is an unknown word — the
machine's words are still spelled small, and it says so
kindly when it meets one it does not know.

### Stone 13 — A pointer

The face of light gains a pointer. `src/mouse.nifla`
wakes the machine's PS/2 mouse — the mouse door of the
keyboard's own controller opened, and the word sent
that starts its reports — and gathers its three-byte
packets into a small desk, polled once a pass of the
main loop. The controller's arrangement byte is never
read or laid, for two honest reasons: its answers come
back as keyboard-side bytes, which the keyboard's
interrupt takes for its own ring before any poll could
read them; and nothing needs it — the mouse's interrupt
could never reach this system anyway, the language's
boot stub masking the second interrupt controller
whole, so polling is the only road the mouse could ever
be heard on. The keyboard's bytes are never read by
this driver: the standing word at the controller's door
tells whose byte waits, and a keyboard byte stops the
asking, for the keyboard's interrupt to take as it
always has.

The arrow is drawn by the pixel face (`pixarrow` in
`src/pixface.nifla`): a hand-drawn shape, black with a
white edge so it reads on any ground, standing in a
sixteen-by-sixteen square whose own pixels are first
kept in a save block and laid back when the arrow moves
on — the desktop under it is never harmed, and each
pass of the loop takes the arrow off before anything is
drawn and lays it again at the pass's end. A fresh
press of the mouse's first button with the arrow's
point on the feather's panel asks for the feather, and the
receiving is the very doing the word `feather` has always
had — the two askings gathered into one at this stone.

Proven by `prove-stone13.sh`: the shipped disc booted
from the ISO file, the bench's mouse driven through the
monitor — the arrow standing at the screen's middle
when the desktop rises, following a move (the monitor's
own reckoning: right and down are forward), the desktop
whole where it left, no green anywhere before the
press, and the feather's green panel standing after a
press on its panel, with `hello` still answered in
light afterward. The whole earlier proof set passes
unchanged.

Honest limits: the pointer lives on the face of light
only — the text face has none, as it never has; the
mouse spoken is the PS/2 mouse, and a USB mouse is a
later road if it is ever taken (the USB road today
carries a keyboard, Stone 6); the arrow's travel is
polled, so it moves in the loop's own steps, not in an
interrupt's; and the one button-press the desktop yet
understands is the feather's panel — the rest of the
desktop does not answer presses yet.

### Stone 14 — Two windows

On the face of light, the welcome panel and the feather's
panel stand as windows now. Each is framed in gray, and
each carries a title bar across its top with its plain
name — Welcome, Feather — and a close mark, a small x at
the bar's right end. One window stands forward: its
title bar is blue, the other's quiet gray, and whenever
the standing changes the windows are painted
back-to-front, so the forward window always stands
whole. The standing itself — which windows are open,
which is forward, and whether a feather has visited — is
kept in the pixel face's desk (offsets 172 to 184),
where the face keeps all its estate; the painting is
`paintwindows` and its helpers in the main body.

The feather's window stands around the panel the feather
has always painted, with its title row above it. Before
any visit, its body says so in plain words: "No feather
has visited yet." A visit — by the word `feather`, or by
the pointer's press on the panel, as since Stone 13 —
opens the window if it stood closed, brings it forward,
and the feather's cells stand in it afterward, kept by
the window until it is closed or the face is drawn
again; the showing itself is the same cell-by-cell
light as Stone 9's.

Bringing forward and closing are a person's own acts:
the Tab key brings the other window forward, and a
press of the pointer on a window brings that window
forward; the Escape key closes the forward window back
to the desktop, and a press on a window's close mark
closes that window, its place painted as the plain
desktop it covered. The word `welcome` opens the
welcome window again and brings it forward, as `feather`
does for its own, and the invitation line on the face
of light names `welcome` among the words now.

Proven by `prove-stone14.sh`: the shipped disc booted
from the ISO file, the windows driven as a person
drives them — Tab bringing each forward in turn (the
title bars read back as pictures: blue forward, gray
behind), a press on the feather's panel visiting with
its window forward, Escape closing the feather window to
a black desktop with the welcome forward in its place,
the word `feather` opening the window and visiting
again, a press on the welcome's close mark closing it
while the feather stands whole, the word `welcome`
opening it again forward, and `hello` answered in
light at the end. The whole earlier proof set passes
unchanged.

Honest limits: the windows live on the face of light
only — the text face keeps its one welcome panel and
has no windows (the word `welcome` there answers in
plain words that the face has no windows to open); the
two windows stand each in its own place and do not move
or change size, and they do not overlap one another —
each paints whole over the desktop, never over its
sister; and where the feather window's ground meets the
answers region, the layering is the desktop's own, as
it has been since Stone 9: an answer printed afterward
may cross the window's lower rows, and the window
paints whole again whenever its standing changes.

### Stone 15 — Notes that stay

The typing line's longer lines (Stone 12) gain their
keeping. The word `note` keeps the rest of its line —
`note` and then the words — as a note on a page of
eight, and the word `notes` shows the page: a heading
that says where the notes live, then each note in its
turn, on either face. A note is kept as bytes in the
main body's page — its length and its letters — and is
shown from its bytes, letter by letter.

When a keeping disk stands ready (Stone 8's disk, given
over at the gate), the page is written through to it
and read back at boot, so the notes stay: the page
lives on the disk beyond the settings card and beyond
the setup clearing's reach — a small header on sector
64 and one sector to a note, sectors 65 onward
(`notesload` and `notesave` in `src/diskkeep.nifla`).
Notes kept during a session before the disk is given
over are written to it at the gate's yes, as the card
is. With no keeping disk, the page lives for the
session only, and every answer says so in plain words:
"Your note is kept until the machine is turned off."
The setup gate stands exactly as Stone 8 left it — the
asking writes nothing, the exact word `yes` alone lets
the keeping begin, and a gate answered otherwise
leaves the disk byte for byte as it was, notes or no
notes.

Proven by `prove-stone15.sh`: one disk through two
lives on the text face (the gate's yes, two notes
answered as kept on the disk and shown; the disk
booted again reading them back at boot, a third note
joining them), the disk image's own bytes checked
afterward (the header on sector 64 and the three notes
in their sectors, word for word as typed); two boots
with no disk (a session note kept and said to be
session-only, and the next boot's page empty again);
the shipped disc on the face of light with the keeping
disk attached, the notes drawn in light; and a second
disk never given over — a session note typed, the gate
answered no, and its bytes afterward exactly as they
were. The whole earlier proof set passes unchanged.

Honest limits: the page holds eight notes, and says so
plainly when it is full; a note is one typed line at
most — the typing line's own measure, 48 keys, less the
word `note` and its space — and there is no erasing or
editing of a kept note yet; the words `note` and
`notes` are not named on the desktop's invitation line,
which has no room left on the face of light's narrower
grid — they answer to their names all the same.

### Stone 16 — Our own EFI doorman

The disc's second door is Cardnull's own now too.
Where GRUB stood at the EFI door since Stone 9, there
stands a loader of this repository's own writing:
`boot/cardnull-efi.c`, a freestanding C program, and
its handover, `boot/cardnull-efi-hand.S`. It does at
its door what the BIOS doorman does at his, and
nothing more: it reads the system and its three
modules from the EFI system partition it stands on
(the partition's own copies under \boot), asks the
firmware's graphics for the very picture the system's
own header asks for and keeps the grant, lays the
system's ELF segments where they belong, and lays the
multiboot information down in the BIOS doorman's own
shape — the information at 0x4000, the module table at
0x4400, the memory map at 0x4800, the modules in a row
at 0x300000. The map is the firmware's own, turned
into the multiboot reckoning: the free memory, and the
loader and boot-services kinds that become free when
the services are left, count as available; the ACPI
tables' ground keeps its own kind; the rest is marked
not to be used. Then it leaves the boot services —
taking the map again at the door when its key has gone
stale, as the firmware's own road prescribes — and
walks the machine down out of the firmware's 64-bit
world into 32-bit protected mode with paging off,
handing over with the multiboot mark in EAX and the
information's address in EBX, interrupts off: the very
handover the BIOS door makes. If anything it needs is
not found — a file, the system's shape, the picture it
asks for, the low pages the handover stands on — it
says so on the firmware's own screen in plain words
and stops, rather than hand over a machine half-laid.

The building of it, told honestly: the bench's clang
compiles the loader for the Windows x64 calling way
the UEFI world speaks (`--target=x86_64-pc-windows-gnu`,
freestanding), the system linker lays it as a PE file
of the i386pep kind, and a two-byte patch in
`build-iso.sh` sets the PE subsystem field to the EFI
application kind, which the linker will not name. The
road was spiked before it was trusted: a first small
application that only spoke a line and filled the
graphics screen red was built the very same way and
booted under the bench's firmware, and filled the
screen red, before the loader itself was written. The
protocol shapes in the loader's source are the UEFI
specification's own, written out by hand; no library
stands between the loader and the firmware.

And GRUB is gone from the disc whole: the EFI
partition holds Cardnull's own BOOTX64.EFI and the
system and its modules, and the `/boot/grub/grub.cfg`
directions file the old door read no longer stands on
the disc at all.

Proven by `prove-stone16.sh`: an audit of the built
disc — its file list read back and its EFI partition's
list read, nothing named for GRUB anywhere on either,
and the BOOTX64.EFI known as Cardnull's own by its
plain-words failure line standing inside it — then the
shipped disc booted under OVMF through the new door
with Stone 9's own scenario (the desktop drawn in
light, the clock's hand moving, the feather's visit in
its green), and the same disc booted through the BIOS
door with the same scenario, unregressed. The whole
earlier proof set passes unchanged — Stone 9's fourth
boot, which always went through GRUB's EFI door
before, goes through Cardnull's own now.

Honest limits: the loader walks the UEFI world's
common road — a 64-bit firmware whose graphics offer
the asked-for shape, and its applications laid in the
low memory the handover's 32-bit reach can touch, as
the bench's firmware (OVMF) lays them; a firmware
offering no picture of the asked shape is told so in
plain words and the loader stops, rather than hand
over a dark machine; the memory map handed over is
the firmware's as it stood at the leaving; and the
loader is as small as its work — it knows the one
disc shape it was written for, the system and its
three modules under \boot, and no other.

### Stone 17 — The stick

Cardnull now also travels on a stick. `./build-stick.sh`
lays `dist/cardnull-stick.img`: the disc's own bytes —
the very ISO of the witness below — with the ISO's
unused system area (its first sixteen sectors) given
to booting as a hard disc. Sector 0 is a master boot
record of Cardnull's own (`boot/cardnull-mbr.asm`): a
small stub that copies itself out of the way, reads
the BIOS bootloader from the sectors after it to the
doorstep at 0x7C00, and jumps to it, the firmware's
drive number carried through untouched. The partition
table names one bootable partition spanning the whole
image, as a courtesy to tools that ask; nothing in the
boot path consults it. Past the system area the image
is the disc, byte for byte — the system, the modules,
and the EFI system partition all ride along as files
in the ISO, exactly as on the disc. No GRUB, no Linux,
no emulator stands on the stick: the firmware boots
the record, the record loads Cardnull's loader, and
the loader brings up Cardnull natively, as a USB hard
disc.

One honest correction belongs to this stone, in the
open as corrections are kept here: the first sketch of
the stick supposed the bootloader would run unchanged
once staged — and it does not, for a reason of
measure. The loader's reckoning is the CD's: a sector
is 2048 bytes, and the volume descriptor stands at
sector 16. A hard disc's sectors — and a stick's,
booted as one — are 512 bytes, so the descriptor
stands at device sector 64 there, and every read must
be four device sectors with its address multiplied by
four. So the bootloader learned to ask the device its
measure once at the door (the BIOS's own question,
int 13h AH=48): on a 512-byte answer its packet
translates every read; on any other answer, or if the
question fails, the CD measure stands — and the whole
regression below proves the CD road byte-for-byte the
road it always was. The ISO filesystem is then walked
exactly as on the CD; only the reckoning of its
sectors changes. (The same visit also corrected a
stale line in the bootloader's own header, which still
said the EFI door opened through GRUB; Stone 16 had
already replaced it.)

Proven by `prove-stone17.sh`, all PASS: the image's
shape (the disc's own length; the boot signature; the
one bootable partition spanning the whole image; the
bootloader byte for byte in the sectors after the
record; the volume descriptor untouched at byte
32768; the image past the system area identical to
the disc) — and a boot: QEMU presents the image as a
USB storage device, SeaBIOS boots it as a hard disc,
and the drawn desktop rises with the clock's hand
moving and the feather's visit in its green (Stone 9's
drawn-desktop scenario). The full earlier proof set
passes unchanged after the bootloader's new question.

**Writing a stick, for the day there is one.** Writing
the image erases the stick whole — everything on it
goes. On a Mac or a Linux machine: build the image
(`./build-stick.sh`), find the stick's device name
(on a Mac, `diskutil list`; on Linux, `lsblk`), unmount
it (Mac: `diskutil unmountDisk /dev/diskN`), and write
the image over the whole device, not a partition of
it: `sudo dd if=dist/cardnull-stick.img of=/dev/diskN
bs=1m` — then eject it (Mac: `diskutil eject
/dev/diskN`). On Windows, a writing tool (Rufus or
balenaEtcher) set to write the image raw — Rufus calls
it DD mode — does the same. Then put the stick in the
machine to boot, open its boot menu, and choose the
stick (it will be named as a USB hard disc); Cardnull
rises as it does from the disc's BIOS door.

Honest limits: the stick boots by the BIOS road — a
machine that offers only UEFI, with no legacy door,
will not boot it this way (the disc's EFI door is the
road for such a machine); the proof above is the
bench's USB emulation, and **the physical witness is
not covered**: no real stick in a real machine has
booted this image yet, and this section does not
pretend otherwise. The keeping disk is a separate
device as always — a stick made from this image is
the system, not the keeping disk, and notes and the
settings card live on the keeping disk as before.

### Stone 18 — A voice

The machine has a small voice now, and it is the last
stone of this ladder. `src/speaker.nifla` speaks to
the PC speaker from the floor: the programmable
timer's second channel is the throat (set counting in
its square-wave way with a divisor of 1,193,182
divided by the pitch, it hums at that pitch), the
speaker gate at port 0x61 lets the hum out and stills
it, and the waits are read off the timer's first
channel, whose count the BIOS leaves falling at the
timer's own rate — latch it, read it, reckon how far
it fell. Every wait is bounded twice over (the count's
wrap is reckoned in, and a guard ends the wait if the
count does not move), so the sound can never hold the
machine: a timer that stands still, or a speaker path
that is absent or strange, costs a little silence and
nothing else.

Three sounds are made, all decided in the main body:

- **The welcome.** Three gentle notes rising — the
  C, E, and G of the middle octave (523, 659, 784),
  the last held a little longer, about two thirds of
  a second in all — sounded as the drawn desktop
  rises, on either face.
- **The refusal.** One low note (the G below middle
  C, 196), about a fifth of a second, when a command
  is refused: a word the machine does not know, and
  the feather's two refusals (no feather on the disc;
  a feather not whole). The old word 'guest' is not a
  refusal — it is answered with the way to the new
  one, and no note sounds for it.
- **`chime`.** A new word (kind 11): the welcome
  sounded again, and a line to say so — "The welcome
  chime, once more."

Proven by `prove-stone18.sh`, all PASS. Its first boot
wires the speaker to the bench's wav capture and opens
a capture window around each event (the bench's
capture delivers the speaker's active samples, so the
proof asserts on those windows exactly): the welcome
in its window (a tone whose crossing-rate sits in the
chime's band), the refusal in its (one low tone), four
seconds of idle holding **no loud sample at all** —
the silence discipline — and the word 'chime' bringing
the welcome again in its window. Its second boot has
**no audio device attached at all**: the text face
rises, 'chime' is answered in plain words, and typing
is unheld — the evidence that machines without the
speaker path are unaffected. The full earlier proof
set passes unchanged. (One bench note, kept honestly:
in this stone's full regression run, prove-stone17.sh
once failed on a truncated screendump read inside the
harness — the same scenario had passed inside
prove-stone9.sh minutes before, and prove-stone17.sh
passed clean on its re-run; the fault was the bench's
reading of a half-written picture, not the system's.)

Honest limits: the voice is the PC speaker **where
one is present** — many modern machines have none, or
route it nowhere a person can hear, and on such a
machine the notes are counted out to silence and
everything else is exactly as it was; QEMU's emulation
of the speaker is this stone's bench proof, as with
the other stones' devices. The pitches are the
timer's arithmetic, within a fraction of a percent of
their names. And the voice says only these three
things; it has no words, and the desktop's law of
plain words is unchanged — the sounds accompany the
words, they never replace them.

### The feather's card moves onto the feather — Nifla Stone 20, adopted (November 15, 2026)

This is not one of this system's own stones; it is the
language's Stone 20, taken into the system the day it
stood. Until now the welcome feather rode the disc as two
modules — its image, and a separate 32-byte binary card
beside it (the image's length and FNV-1a checksum as
eight-byte numbers), laid by this repo's own
`tools/make-modules.py` and read by the door from the
card module. The compiler now lays a plain-text card at
the feather's head itself (`niflac --bare --guest
--feather`), so the feather rides as ONE module —
`build/welcome.feather`, on the disc as `feather.fea` —
and the door reads the card from the feather it is
handed:

- `build.sh` builds the welcome feather with `--feather`;
  `tools/make-modules.py` shrank to the one thing still
  honestly its own — the settings module — and says so in
  its header. The card half is retired.
- The boot lift finds the feather by the card's first
  line ("CARDNULL FEATHER 1") instead of by a promised
  length; the settings are read as before.
- The door (`src/featherdoor.nifla`) parses the card's
  lines in plain Nifla — `name:` and `needs:` are for
  people and are stepped over; `bytes:` and `checksum:`
  are read and checked — reckons the FNV-1a checksum over
  the program bytes after the card's blank line, and lets
  the feather in only when the card is whole, the program
  is exactly as long as lifted, and the reckoning matches
  the promise. The refusals are the same plain words as
  before: no carded feather on the disc, or "The feather
  on this disc is not whole, so it was not let in."
- Both doormen (the BIOS bootloader and the EFI loader)
  stage and hand over two modules now, and the disc
  carries `feather.fea` in both its trees.
- The adoption also surfaced a latent fault in the BIOS
  doorman's staging, found by the proof regression and
  fixed in the open: the modules staged at 0x60000 and
  0x62000, inside the system file's own 192 KiB staging
  claim at 0x40000, on the old reckoning that the system's
  text ended well below them. The door's growth carried
  the text's tail — and its GDT — across the settings
  stage's line (the GDT at file offset 0x201F0, the
  settings splash at 0x20000–0x20200), and the staged
  settings overwrote the GDT's code descriptor: the
  adopted system died at its first far jump through its
  own doorman, while QEMU's loader (which does not stage
  there) booted it fine. The module stages now stand at
  0x70000 and 0x72000, above the whole claim, and the
  doorman's header says why, so no stage ever sits inside
  another's claim again.

The door's honesty is unchanged: the checksum proves the
bytes match the card and nothing more (it is not a
signature), there is no isolation yet, and a faulting
feather still stops the whole machine. The full proof
regression passes on the adopted build — the fifteen
live proofs (stones 3–9 and 12–18, and prove-iso) —
including the Stone 5 door proof in its new shape: the
feather as laid visits and goes home, and a copy with
one byte flipped in its program is refused in plain
words and never appears.

## The kernel's files

The kernel is built as several files, never one big one — Tyler's
standing rule (November 15, 2026), kept from the first Cardnull OS,
whose kernel stood in twenty files. The seed kernel began the
founding morning as a single file; the same day, at Tyler's word, it
was split by duty, without changing its behavior:

- `src/cardnull.nifla` — the main body: the boot sequence, the
  first-breath lift of what the loader brought, all the system's
  state, the face, the typing line, and the loop that calls the
  libraries. The two windows' painting lives here too (Stone 14:
  winframe, onewelcome, onefeather, paintwindows), reading the
  windows' standing from the pixel face's desk.
- `src/screenlib.nifla` — the screen library: drawing on the text
  screen's own memory (clearscreen, writeat, paintrow, paintrect,
  scrollanswers).
- `src/clock.nifla` — the clock's face, and the reckoning behind the
  person's time choice (pad2, clocktext).
- `src/bootmods.nifla` — the hands that read what the loader
  brought: the module table and the modules that ride the disc
  (modcount, modstart, modend, modcopyfrom).
- `src/featherdoor.nifla` — the feather door: reading the card at
  the feather's own head, its FNV-1a check, the doorstep, the call,
  and the plain-words refusals (feathermark, cardparse, fnv1afrom,
  placefeather, runfeather).
- `src/commands.nifla` — deciding what a typed word is answered
  with: what kind of answer, the line that answers it, and the
  clock's offset once the word is done (wordkind, wordline,
  wordoffset).
- `src/usbkey.nifla` — ears on the USB road (Stone 6): the UHCI
  host and the HID boot keyboard it wakes, its whole estate in
  one desk of bytes the main body hands it at every asking
  (usbinit, usbpoll, and their helpers).
- `src/rtclock.nifla` — the real clock (Stone 7): reading the
  machine's own CMOS clock into a block the main body hands
  it, and the calendar reckoning that turns a reading into a
  date in plain words (rtcread, rtcbaseof, datetext, and their
  helpers).
- `src/diskkeep.nifla` — what the system remembers on a hard
  disk (Stone 8): waking the drive, the settings card and its
  reading, the write-back, and the setup clearing
  (diskhere, savedoffset, remember, disksetup). The notes
  page's carrying is here too (Stone 15: notesload, notesave)
  — a header on sector 64 and one sector to a note.
- `src/font.nifla` — the letters of the face of light
  (Stone 9): the hand-drawn 8×8 bitmap font for the letters
  a person can type, drawn in this file's own comments and
  laid into a block of bytes by fontload.
- `src/pixface.nifla` — the face of light (Stone 9): the
  picture screen's desk and palette, the page-table reach
  to a screen above the waking map, and the drawing —
  fills, letters, whole lines, the wrapped and scrolling
  answers, and the reading of the feather's cells
  (pixbegin, pixfill, pixglyph, pixline, pixprintline,
  cellbyte, and their helpers). The pointer's arrow is
  drawn here too (Stone 13: arrowload, pixsave,
  pixrestore, pixarrow).
- `src/mouse.nifla` — the pointer (Stone 13): the PS/2
  mouse's waking and the gathering of its packets into a
  desk the main body hands it, polled once a pass
  (mouseinit, mousepoll, mousedx, mousedy, and the
  controller-door helpers).
- `src/speaker.nifla` — the voice (Stone 18): the PC
  speaker's notes — the timer's singing channel, the
  gate, and the waits read off the timer's falling
  count, bounded twice over (noteon, noteoff, playnote,
  welcomechime, refusenote, and the door helpers).

The libraries join the main body as preludes at build (build.sh
names them all): files of pure functions — values in as arguments,
results back — because on bare metal a function that reads or
assigns the program's shared variables is given a broken value (see
"Notes for builders"). Every function that moved kept its exact
body; the one piece of deciding that used to live in the main loop
(the command dispatch) now asks the command library its three
questions, and the doing still happens in the body, where the state
lives. The welcome feather (`src/welcome-feather.nifla`) is a separate
program that visits through the door, and is no part of the kernel.

Proven after the split by the full shipped proof set —
`prove-stone3.sh`, `prove-stone4.sh`, `prove-stone5.sh`, and
`prove-iso.sh` all PASS, with readback checks identical to the
same proofs run against the single file before it was split.

## The witness disc

Cardnull OS 2 ships as **one disc and nothing else** — Tyler's word
on the founding morning (November 15, 2026): "we should've built the
iso from day one like the first OS." `./build-iso.sh` lays it, and
since Stone 17 the same disc's bytes also travel as a stick image
beside it (the stick is the disc, not a second system):

- `dist/cardnull-os-2.iso` — 8,949,760 bytes, as built November 15,
  2026 (the disc after the adoption of Nifla's Stone 20: the
  framebuffer kernel with its two windows, its notes that stay,
  and its voice, the welcome feather riding as one file with its
  card at its head, and Cardnull's own loaders at both doors — the
  BIOS bootloader and the EFI loader; no GRUB anywhere on it).
  sha256: `76e5effc47da98e34c2718b8619f80537a0243ef7c96e9b1bdf49ca51d75820f`
  (The ISO file itself is a build product and is not kept in this
  repository; the hash records the disc the proof below was run
  against, and `./build-iso.sh` rebuilds it.)
- `dist/cardnull-stick.img` — 8,949,760 bytes, as built November
  15, 2026 by `./build-stick.sh` from the same tree: the disc
  above with Cardnull's master boot record at its head and the
  BIOS bootloader in the sectors after it (Stone 17).
  sha256: `0ac4adebfeabbe1117058e0b854ad8e5c8b84d603dcb8a3f974792dadb7c30b9`
  (Likewise a build product, not kept in this repository.)

On the disc: the system (`/boot/cardnull.elf`), the settings module,
and the feather itself (`/boot/feather.fea`), its card at its head —
everything Stones 4 and 5 need rides as multiboot modules the loader
brings with the system —
plus `/boot/boot.img`, Cardnull's own bootloader (the El Torito
catalog's BIOS image), and the EFI system partition at
`/boot/efi.img` carrying the EFI door's own loader
(`\EFI\BOOT\BOOTX64.EFI`) and its own copies of the system and the
modules.

The doors, named honestly: **both doors are Cardnull's own** —
the BIOS door its own bootloader since Stone 11, the EFI door its
own EFI loader since Stone 16. No GRUB stands anywhere on the
disc.

**To witness it in UTM:** make a new x86_64 machine, give it
**4096 MB** of memory, attach `cardnull-os-2.iso` as the machine's
CD/DVD drive, and boot. Nothing else is attached — no hard disk,
no second image. **Either firmware works now** — SeaBIOS or UEFI;
for typing, the USB 2.0 arrangement with USB Support **on** (or
the PS/2 keyboard either way), and for a remembering disk,
Stone 8's arrangement in its section above. The desktop comes up
drawn in light, on Eastern time; the words on its invitation line
all work, `feather` included.

Proven by `prove-iso.sh`, booting the ISO file itself as a CD-ROM
(no `-kernel` shortcut) at 4096 MB: the shipped disc shows the
desktop, its carried Eastern choice on the clock (hour 19), the
feather's visit in its color, and `utc` moving the clock for the
session; a variant disc carrying the world's time in its settings
comes up at hour 00 uninvited; and a variant disc with one byte of
the feather flipped refuses the feather in plain words, with the
desktop unharmed.

**The EFI door, attempted the same day and recorded honestly:**
Tyler's new UTM machine uses UEFI firmware, and the disc above has
no EFI door — his first boot of it landed in the UEFI shell. A
hybrid disc was therefore built on the bench (an EFI system
partition carrying GRUB's x86_64-efi build as `\EFI\BOOT\BOOTX64.EFI`,
loading the same kernel and modules) and booted under OVMF. What
was found, exactly: the firmware loads and starts the EFI GRUB
willingly. GRUB built without its video drivers then refuses the
multiboot handoff in plain words on the firmware's screen —
"WARNING: no console will be available to OS / error: no suitable
video mode found." GRUB built with its graphics drivers (all_video,
efi_gop) goes further: it sets an 800×600 graphics mode, loads the
kernel, and hands over — the kernel provably runs (its instruction
pointer sits inside the kernel, in its own code segment) — but the
screen a person sees is black, and the text screen at 0xB8000 reads
back as void (0xFF), because **UEFI offers no legacy text screen at
all, only a graphics framebuffer**, and this kernel paints a text
screen. No loader arrangement can hand a text-mode kernel a text
screen under UEFI; the kernel itself must either reprogram the
video card into text mode (a language boot-stub matter) or draw on
the framebuffer the loader already offers — which is Stone 9's
road, below in the ladder Tyler has set. So the EFI door does not
ship yet: a door that opens onto a black screen is not a door. The
disc keeps its BIOS door (in UTM: a machine whose firmware is
SeaBIOS, or UTM's QEMU backend with BIOS), and the EFI attempt
stands here as the record, to be taken up again when the desktop
is drawn in pixels.

**Taken up again at Stone 9, and healed:** the desktop is now
drawn in pixels, the kernel asks its loader for the picture
screen, and the hybrid disc ships: under OVMF the EFI GRUB hands
over the granted framebuffer (1024×768, exactly as asked), the
desktop is drawn, and the feather visits through that door too —
proven in `prove-stone9.sh`'s fourth boot. The record above
stands as the finding that led here; the door it describes is
open now.

## Notes for builders

- The visible screen of this system speaks **plain words only** — no codes
  and no jargon on the desktop surface. Diagnostics belong in proofs and
  in this README, not on the screen a person reads.
- On bare metal, Nifla functions must not read or assign the program's
  shared (global) variables: measured on the bench, a function that does
  so receives a broken value, while the same variables work correctly in
  the program's main body. Every helper in this system is therefore
  written in the pure style — values go in as arguments and come back as
  results — and all state is kept in the main body. (A finding about the
  language as it stands at Stone 18; the language is not changed from
  here.)
- The language's `disksectors()` reads the drive's status port before
  selecting the drive, and an unselected drive's status reads as
  nothing there — so on a freshly booted machine it answers 0 even
  with a disk fitted, until some transfer has selected the drive.
  Measured both ways on the bench. The disk-era build of Stone 4 met
  this by selecting the drive first with a three-instruction floor
  block; the shipped system attaches no disk at all (see Stone 4) and
  no longer uses the disk tools, but the finding stands about the
  language. A `diskread` or `diskwrite` with no disk fitted still
  stops the machine, exactly as the language's Stone 16 notes say.
  (Also a finding, reported rather than repaired from here.)
- A floor block in a **feather** program that is handed a piece of text
  or a block of bytes is given a desk whose length reads as zero:
  measured on the bench both ways (a host's floor blocks, handed the
  same things, work), and confirmed in the compiler's own generated
  assembly — the feather build never stores the handed values into the
  floor-inputs table the block reads, where the host build does. A
  feather's floor blocks that are handed nothing work, and `say` works,
  so the welcome feather paints with a nothing-handed floor block and
  writes its letters as immediate values, each quoted in its source.
  (A finding about the language as it stands at Stone 18.)
  **Correction (Stone 10, November 15, 2026): this finding did not
  survive re-measurement.** Shape by shape — literals, blocks,
  functions handing their own words onward, joined and returned
  text, text with numbers, the letters themselves read back — a
  feather's floor blocks receive the desk whole, and the generated
  assembly for the handing is the same in both builds. The welcome
  feather is written with handed text now, and the language carries
  a standing proof of the desk (`run-bare-guest-desk.sh` in its
  repository). The words above stand as they were recorded on the
  founding morning; this correction stands beside them.
- The bootloader's module table and the modules themselves are left
  in low memory that the language's heap also claims from above:
  measured on the bench, the table was found overwritten by the
  program's own early text allocations when it was read after them,
  while the module bytes themselves, left higher, survived. This
  system therefore reads the table's addresses into plain numbers
  before allocating anything, and lifts the modules' bytes into its
  own blocks immediately after — the table is never read again.
  (Bench discipline for building on this language's bare target,
  recorded so the next builder does not rediscover it the hard way.)
