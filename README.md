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

- `dist/cardnull-os-2.iso` — 563,200 bytes, as built November 15, 2026
  (rebuilt from the split kernel — see "The kernel's files" above).
  sha256: `29fd550c9237ed5c4e8080d6a3d01f900a5e9133df8d5ef303ecc194ee825dd0`
  (The ISO file itself is a build product and is not kept in this
  repository; the hash records the disc the proof below was run
  against, and `./build-iso.sh` rebuilds it.)

On the disc: the system (`/boot/cardnull.elf`), the settings module,
the guest's card, and the guest itself — everything Stones 4 and 5
need rides as multiboot modules the loader brings with the system —
plus the loader's own files under `/boot/grub/`.

The loader is GRUB, named honestly: it is a means to boot the
multiboot kernel, not part of Cardnull. Cardnull's own bootloader
remains future work, as it was in the first Cardnull OS's early
doors. The disc boots on a BIOS (SeaBIOS) machine; an EFI boot
image is future work too.

**To witness it in UTM:** make a new x86_64 machine, give it
**4096 MB** of memory, attach `cardnull-os-2.iso` as the machine's
CD/DVD drive, and boot. Nothing else is attached — no hard disk,
no second image. The desktop comes up on Eastern time; the words
on its invitation line all work, `guest` included.

Proven by `prove-iso.sh`, booting the ISO file itself as a CD-ROM
(no `-kernel` shortcut) at 4096 MB: the shipped disc shows the
desktop, its carried Eastern choice on the clock (hour 19), the
guest's visit in its color, and `utc` moving the clock for the
session; a variant disc carrying the world's time in its settings
comes up at hour 00 uninvited; and a variant disc with one byte of
the guest flipped refuses the guest in plain words, with the
desktop unharmed.

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
