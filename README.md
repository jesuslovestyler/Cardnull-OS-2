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
./build.sh            # makes build/cardnull.elf, build/guest.bin, and the
                      # disc's two small modules (build/settings.bin,
                      # build/card.bin)
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
and bar are repainted only when drawn; a guest or a stray writer
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
clock starts on Eastern and `guest` is answered plainly.

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

## The kernel's files

The kernel is built as several files, never one big one — Tyler's
standing rule (November 15, 2026), kept from the first Cardnull OS,
whose kernel stood in twenty files. The seed kernel began the
founding morning as a single file; the same day, at Tyler's word, it
was split by duty, without changing its behavior:

- `src/cardnull.nifla` — the main body: the boot sequence, the
  first-breath lift of what the loader brought, all the system's
  state, the face, the typing line, and the loop that calls the
  libraries.
- `src/screenlib.nifla` — the screen library: drawing on the text
  screen's own memory (clearscreen, writeat, paintrow, paintrect,
  scrollanswers).
- `src/clock.nifla` — the clock's face, and the reckoning behind the
  person's time choice (pad2, clocktext).
- `src/bootmods.nifla` — the hands that read what the loader
  brought: the module table and the modules that ride the disc
  (modcount, modstart, modend, modcopyfrom).
- `src/guestdoor.nifla` — the guest door: the card's FNV-1a check,
  the doorstep, the call, and the plain-words refusals (cardnum,
  fnv1a, placeguest, runguest).
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
  (diskhere, savedoffset, remember, disksetup).
- `src/font.nifla` — the letters of the face of light
  (Stone 9): the hand-drawn 8×8 bitmap font for the letters
  a person can type, drawn in this file's own comments and
  laid into a block of bytes by fontload.
- `src/pixface.nifla` — the face of light (Stone 9): the
  picture screen's desk and palette, the page-table reach
  to a screen above the waking map, and the drawing —
  fills, letters, whole lines, the wrapped and scrolling
  answers, and the reading of the guest's cells
  (pixbegin, pixfill, pixglyph, pixline, pixprintline,
  cellbyte, and their helpers).

The libraries join the main body as preludes at build (build.sh
names them all): files of pure functions — values in as arguments,
results back — because on bare metal a function that reads or
assigns the program's shared variables is given a broken value (see
"Notes for builders"). Every function that moved kept its exact
body; the one piece of deciding that used to live in the main loop
(the command dispatch) now asks the command library its three
questions, and the doing still happens in the body, where the state
lives. The welcome guest (`src/welcome-guest.nifla`) is a separate
program that visits through the door, and is no part of the kernel.

Proven after the split by the full shipped proof set —
`prove-stone3.sh`, `prove-stone4.sh`, `prove-stone5.sh`, and
`prove-iso.sh` all PASS, with readback checks identical to the
same proofs run against the single file before it was split.

## The witness disc

Cardnull OS 2 ships as **one disc and nothing else** — Tyler's word
on the founding morning (November 15, 2026): "we should've built the
iso from day one like the first OS." `./build-iso.sh` lays it:

- `dist/cardnull-os-2.iso` — 9,050,112 bytes, as built November 15,
  2026 (the hybrid disc of Stone 9: the framebuffer kernel, booting
  through both the BIOS and the EFI doors).
  sha256: `1f26f3c996076e8f9a12da108f56125c3d728eb9388c162b98a1b648d88d3f83`
  (The ISO file itself is a build product and is not kept in this
  repository; the hash records the disc the proof below was run
  against, and `./build-iso.sh` rebuilds it.)

On the disc: the system (`/boot/cardnull.elf`), the settings module,
the guest's card, and the guest itself — everything Stones 4 and 5
need rides as multiboot modules the loader brings with the system —
plus the loader's own files under `/boot/grub/`, and the EFI system
partition at `/boot/efi.img` carrying its own copies for the EFI
door.

The loader is GRUB at both doors, named honestly: it is a means to
boot the multiboot kernel, not part of Cardnull. Cardnull's own
bootloader remains future work (the BIOS door's is Stone 11's).

**To witness it in UTM:** make a new x86_64 machine, give it
**4096 MB** of memory, attach `cardnull-os-2.iso` as the machine's
CD/DVD drive, and boot. Nothing else is attached — no hard disk,
no second image. **Either firmware works now** — SeaBIOS or UEFI;
for typing, the USB 2.0 arrangement with USB Support **on** (or
the PS/2 keyboard either way), and for a remembering disk,
Stone 8's arrangement in its section above. The desktop comes up
drawn in light, on Eastern time; the words on its invitation line
all work, `guest` included.

Proven by `prove-iso.sh`, booting the ISO file itself as a CD-ROM
(no `-kernel` shortcut) at 4096 MB: the shipped disc shows the
desktop, its carried Eastern choice on the clock (hour 19), the
guest's visit in its color, and `utc` moving the clock for the
session; a variant disc carrying the world's time in its settings
comes up at hour 00 uninvited; and a variant disc with one byte of
the guest flipped refuses the guest in plain words, with the
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
desktop is drawn, and the guest visits through that door too —
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
- A floor block in a **guest** program that is handed a piece of text
  or a block of bytes is given a desk whose length reads as zero:
  measured on the bench both ways (a host's floor blocks, handed the
  same things, work), and confirmed in the compiler's own generated
  assembly — the guest build never stores the handed values into the
  floor-inputs table the block reads, where the host build does. A
  guest's floor blocks that are handed nothing work, and `say` works,
  so the welcome guest paints with a nothing-handed floor block and
  writes its letters as immediate values, each quoted in its source.
  (A finding about the language as it stands at Stone 18.)
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
