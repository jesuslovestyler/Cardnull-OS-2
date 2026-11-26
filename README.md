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
                      # and build/paint.feather (the feathers with
                      # their cards, by the compiler's feather mode),
                      # and the disc's one small module
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
./prove-nowitness.sh  # boots the disc and the stick with NO input at all,
                      # and watches the face paint (the witness fix)
./prove-featherpaint.sh  # receives the feather and DECODES its painted
                      # window letter by letter (the feather paint fix)
./prove-featherstart.sh  # boots with NO input and DECODES the word
                      # "feather" wherever the startup view shows it
                      # (the feather start fix)
./prove-pointertrail.sh  # drags the pointer across the desktop and
                      # requires the desktop pixel for pixel as it was
                      # (the pointer trail fix)
./prove-stone19.sh    # opens the files window on a prepared disk and
                      # DECODES its list letter by letter (Stone 19)
./prove-stone20.sh    # opens the settings window, CLICKS its choices,
                      # and reads them back from the disk's card after
                      # a re-boot (Stone 20)
./prove-stone21.sh    # opens the editor window, TYPES a note in it,
                      # changes it, and reads the changed words back
                      # from the disk's CNN3 store (Stone 21)
./prove-stone22.sh    # DRAGS the files window by its title bar to a
                      # new place, DECODES it there, checks the ground
                      # it left, and clicks a note's row in the
                      # dragged window (Stone 22)
./prove-stone24.sh    # opens the paint feather by its word, DRAWS
                      # with the pointer in its canvas, changes color
                      # at its swatches, and CLEARS the canvas —
                      # every mark read back as pixels (Stone 24)
./prove-stone25.sh    # keeps a note, chooses Rest (by the menu and
                      # by the word), SHUTS DOWN — the machine
                      # actually powers off under QEMU — and, in a
                      # second boot, RESTARTS: the desktop falls
                      # and rises a second time in the same run,
                      # and the kept note is read back after it
                      # (Stone 25)
./prove-stone26.sh    # DRAWS in the paint feather on a keeping
                      # disk, reads the picture store's own
                      # bytes off the disk, then REBOOTS on the
                      # same disk: the files window lists the
                      # picture beside a note, and opening it
                      # there shows the drawing again, its
                      # cells decoded back (Stone 26)
./prove-stone27.sh    # prepares a disk with three known
                      # notes, CANCELS a letting go twice in
                      # the files window (the note stands
                      # whole), lets one note go there and
                      # one in the editor, reads the CNN3
                      # store's own bytes (one note whole,
                      # the let-go sectors wiped), REBOOTS
                      # and finds only the remaining note —
                      # and lets a sitting's note go with no
                      # disk fitted at all (Stone 27)
./prove-stone28.sh    # opens the settings window on an
                      # old-shape card, CLICKS 'Large',
                      # DECODES the whole desktop at the
                      # large size (the bar standing 24
                      # pixels tall), DRAGS a window and
                      # clicks a choice at that size,
                      # REBOOTS on the same disk and finds
                      # large print standing from the card,
                      # and proves an old-shape card and a
                      # sitting with no disk (Stone 28)
./prove-stone29.sh    # opens the verse window by its word
                      # and from the bar's menu, DECODES the
                      # day's verse letter by letter at the
                      # usual size and at large print, and
                      # closes it by Escape and by its close
                      # mark (Stone 29)
./prove-stone30.sh    # opens the calculator window by its
                      # word and from the bar's menu, presses
                      # its painted keys with the pointer and
                      # DECODES the sum's line off the
                      # feather's cells after each press —
                      # one of each working, a sum below
                      # nothing, the remainder named, a
                      # clear, and a sharing out by 0
                      # answered in plain words (Stone 30)
./prove-stone31.sh    # opens the help window by its
                      # word and from the bar's menu,
                      # DECODES every page of its plain
                      # help words letter by letter at the
                      # usual size and at large print,
                      # turning its pages by its foot and
                      # by the arrow keys (Stone 31)
./prove-stone32.sh    # boots with a modern (xHCI) USB
                      # controller and a keyboard on it:
                      # the ready word stands for the
                      # modern road, shifted letters and
                      # Caps Lock type on it, and the
                      # 'usb' word's own count for that
                      # road proves it carried the keys;
                      # then the controller with no
                      # keyboard, and no controller at
                      # all, unbothered (Stone 32)
./prove-stone33.sh    # boots the glass face: the bar
                      # at the screen's foot with its
                      # sheen bands, the round start
                      # button's pixel-drawn cardinal
                      # proven in its own colors and
                      # shape, the menu risen from the
                      # button with its nine choices
                      # decoded letter by letter, a
                      # glass window dragged by its
                      # title bar with its vacated
                      # ground whole, the pointer
                      # leaving the glass desktop
                      # pixel-for-pixel as it found it,
                      # and Rest opened from the menu —
                      # at the usual size, and again at
                      # large print from a card that
                      # carries it (Stone 33)
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

*A later word (November 16, 2026): the USB 3.0
arrangement named above as not covered by this stone
is covered now — Stone 32 adds the xHCI road beside
this one, in its own library, feeding the same typing
line. This section's words stand as the record of
Stone 6; the coverage as it now stands is told in
Stone 32's section.*

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

### Stone 19 — The files window

A third window stands on the face of light now, opened
by the new word `files` (kind 12). It lists what the
fitted disk actually holds — and what the disk honestly
holds today is the notes page of the CNN3 store
(sectors 64 onward, Stone 15): the window is a list of
exactly those notes, each entry the note's own words,
and no filesystem is invented beyond them. The picked
entry stands white on blue; picking one — a press of
the pointer on its row, or the up and down arrow keys
while the window stands forward — shows that note's
whole words at the window's foot, under the plain label
"The note you picked:". Tab cycles through all three
windows now, Escape closes the forward one as before,
and each window's close mark still closes it, the files
window's included. The window's standing lives in the
pixel face's desk beside the others' (offsets 188 to
204), with the main body's facts — how many notes stand
kept, whether a disk is keeping them, whether one is
fitted at all — copied into the desk whenever they
change, so its painting can say plainly where the notes
live.

With no disk fitted, the window says so in plain words
— "There is no disk fitted." and "Nothing is saved." —
and shows no entry at all; a disk fitted but not yet
given over is told the same honest way ("This disk is
not keeping your choices yet." / "Nothing is saved on
it."), and a keeping disk with an empty page says that
instead. Notes kept only for the session are never
shown as if they were saved.

Proven by `prove-stone19.sh`: a keeping disk prepared
with three known notes in the CNN3 store (the settings
card on sector 8, the header on sector 64, one sector
to a note — the shape Stone 15's proof checks byte for
byte) is booted with the shipped disc, the word `files`
is typed, and the window's rendered list is **decoded
letter by letter** against the system's own letter
shapes and compared against the known notes; the down
arrow and then a pointer press each move the pick, and
the picked note's whole words must stand at the
window's foot; Tab cycles through all three windows;
Escape closes the files window back to the desktop. A
second boot with no disk at all reads the plain
no-disk words back the same way, and checks that no
picked note is shown.

Honest limits: the list is the notes page and nothing
more — the store holds no other kind of file, so the
window shows no other kind; a note's entry is its whole
text (a note is one line of at most 43 letters, and the
window is wide enough for it whole). The files window
stands on the face of light only; the text face answers
`files` as it answers `welcome`, in plain words. The
word `files` is not named on the desktop's invitation
line, as `note` and `notes` are not. And the window is
a reader, not an editor: a note is still kept by the
word `note`, and there is still no erasing or editing
of a kept note.

### Stone 20 — The settings window

A fourth window stands on the face of light now, opened
by the new word `settings` (kind 13). Two choices are
set there **by clicking**: the time zone — "Eastern
time" or "World's standard time", under the plain label
"Time zone:" — and whether the welcome chime sounds —
"Chime on" or "Chime off", under "Welcome chime:". Each
choice stands as its own row, and the one that truly
stands is shown white on blue with the pick mark, the
files window's way; a press of the pointer on a choice's
row sets that choice. The window shows the choices as
they actually stand — its time zone from the very
offset the bar's clock reckons by, its chime from
whether the chime is on — and the typed words follow it
and it follows them: `eastern` and `utc` move the
window's pick as they move the clock, and `chime` is
governed by the standing, answering in plain words
("The chime is off, so nothing sounded.") when the
chime stands off. The refusal's low note is not the
chime and sounds as it always has. Tab cycles through
all four windows now, Escape closes the forward one,
and the window's close mark closes it like the others'.
Its standing lives in the pixel face's desk beside the
others' (offsets 208 to 216), the main body's facts
copied in whenever they change.

The choices are kept the way the time choice has been
kept since Stone 8: on the fitted keeping disk's
settings card (sector 8), which grows by one byte at
its end — the chime byte, fourth on the card: 1 when
the chime stands on, 2 when it stands off, and 0 when
no choice was ever kept there, so a card laid before
this stone keeps the chime on, as it always sounded.
A click on a keeping disk writes both choices through
at once, and the window's foot says so: "Your choices
are kept on the disk." With no keeping disk the window
says plainly, "Your choices last only for this sitting."
— with "There is no disk fitted." or "This disk is not
keeping them yet." beneath, as the case stands — and
the choices still work for the sitting, exactly as
honestly as the typed words have always put it.

Proven by `prove-stone20.sh`: a keeping disk prepared
with an Eastern card (its chime byte 0, as an older
card carries) is booted with the shipped disc at a
bench clock where Eastern reads 19 and the world's
standard 00; the word `settings` opens the window and
its rendered choices are **decoded letter by letter**
against the system's own letter shapes; the typed word
`eastern` is answered as before; a pointer press on
the world's-standard row moves the bar clock's own
rendered figures to 00, and a press on the chime-off
row stands the chime off in the window; Tab cycles
through all four windows and Escape closes the
settings window. The disk's bytes are then checked —
the card carries offset 64 and chime byte 2 — and a
second boot on the same disk, choosing nothing, finds
the clock already at 00 and both choices as they were
left: they persisted from the card. A third boot with
no disk at all reads the plain sitting-only words back
and clicks the clock over for the sitting.

Honest limits: the settings window stands on the face
of light only; the text face answers `settings` as it
answers `welcome`, in plain words. The word `settings`
is not named on the desktop's invitation line, as
`files` is not. The chime's standing governs the
welcome chime — at the desktop's rising and at the
word `chime` — and nothing else that sounds; and a
choice made with no keeping disk is gone when the
machine is turned off, as the window itself says.

### Stone 21 — The editor window

A fifth window stands on the face of light now, opened
by the new word `editor` (kind 14). Here a note is
**written and changed in a window**, not only by the
word `note` — and it is kept to the very same CNN3 note
store that word keeps to: the same page in the main
body's keeping, written through by the same `notesave`,
so a note kept here stands in the files window and in
the reckoning of the word `notes`, and theirs stand
here. Nothing about the store changed; the window is a
second road to it.

The window stands in two ways. In its **picking way** it
lists "Write a new note" first, then every kept note,
the picked one white on blue with the pick mark, the
files window's way; the up and down arrow keys or a
press of the pointer on an entry's row pick, and Enter
— on an empty typing line — takes the pick into the
**writing way**. (A line with words on it is a command,
as it always is; the window never takes a typed word's
Enter from it.) In the writing way the note's words
stand as a draft: a note being changed is copied in
whole, a new note starts empty, and the desktop's own
typing writes into the draft — the shift keys and Caps
Lock resolve exactly as they do on the typing line,
Backspace forgets the draft's last letter, and Enter
keeps the draft back to the same slot, so a changed
note keeps its place on the page. A press of the
pointer on the keep row keeps the draft the same way.
The draft lives in a ninth slot of the notes block,
beyond the eight the disk carries; it reaches the disk
only by being kept, through the store's own path.

A note holds **forty-three letters at most** — the
typing line's own measure, the measure the word `note`
has always kept by (its line holds forty-eight keys,
and the word and its space take five) — and the
writing way says so in plain words, "A note can hold
43 letters at most.", rather than letting the words
run past it in silence: typing past the measure simply
adds nothing, and the draft that stands in the window
is the whole of what will be kept. Tab cycles through
all five windows now, Escape closes the forward one
(a draft not yet kept is thrown away with the window),
and the window's close mark closes it like the others'.
Its standing lives in the pixel face's desk beside the
others' (offsets 220 to 232); the count and the keeping
it speaks of are the files window's copies in the same
desk, the same facts.

The honesty is the store's own, said in the window:
with a keeping disk, "Your note will be kept on the
disk."; with none, "Your note will be kept only for
this sitting." — with "There is no disk fitted." or
"This disk is not keeping notes yet." beneath, as the
case stands — and the note still lives for the sitting,
in the window's list and in the word `notes`, exactly
as the answers have always put it.

Proven by `prove-stone21.sh`: a keeping disk prepared
with one known note is booted with the shipped disc;
the word `editor` opens the window and its rendered
list is **decoded letter by letter** against the
system's own letter shapes; a pointer press picks the
kept note and Enter shows its whole words as the
draft; a new note is typed and kept, and stands in the
list; forty-six letters typed at a fresh note stop at
forty-three, and that draft is thrown away by Escape —
the page still holds exactly two notes. The kept note
is then changed in the window (its last word rubbed
out, another typed) and kept back to the same place;
the files window lists the changed words from the same
store; Tab brings the editor forward among the five
and Escape closes it. The disk's bytes are then
checked: the CNN3 header counts two notes and the
second sector carries the changed words — the window
truly wrote through the store. A second boot with no
disk at all reads the plain sitting-only words back
from both of the window's ways, keeps a note for the
sitting in the window, and finds it again in the
reckoning of the word `notes`.

Honest limits: the editor window stands on the face of
light only; the text face answers `editor` as it
answers `welcome`, in plain words. The word `editor`
is not named on the desktop's invitation line, as
`files` and `settings` are not. A note is one line of
words, as the store has always held it — the window
writes the line the store holds, no longer and no
otherwise shaped. Editing speaks to the notes page
only; the settings card is the settings window's, as
it has been since Stone 20.

### Stone 22 — Window dragging

The windows move now: **a window is dragged by its
title bar with the pointer.** A press of the pointer's
first button on a window's title bar — anywhere on the
bar except its close mark, which still closes, as it
always has — takes hold of the window and brings it
forward, as any press on a window has always brought
it forward. While the button stands held, the window
follows the pointer by the same hold (the place within
the bar where it was taken is kept, so the window does
not jump to the pointer); letting the button go sets
it down. The drag is reckoned in letter cells, the
measure every window's place is reckoned in, and a
window is kept **whole on the desktop**, simply
clamped at the edges: its left stands between the
desktop's left edge and the place where its right edge
meets the desktop's right edge, and its top between
the top bar's underside and the place where its bottom
meets the desktop's foot. As a window moves, the
ground it stood on is filled back to the plain desktop
and the windows are painted again, so a window that
stood under the dragged one stands whole in its place
— the same manners closing a window has always kept.

The geometry discipline is the one the windows have
kept since Stone 14, now made literal: **a window's
place is one reckoned place, read by the painter and
the pointer alike.** Each window's left and top live
in the pixel face's desk — the welcome's at 140 and
144, where they have always lived, and the feather's,
files, settings, and editor windows' at 236 to 264,
laid at the face's rising from the places their
measures first reckon (centered, at the layout's rows
14 and 17) — and a window's own left/top reckonings
(the feather's `fwleft` and its kin) read that place,
while its width and height are reckoned as before. The
main loop's pressing — the drag's taking hold and
following, the close marks, and every content press:
the files window's rows, the settings window's
choices, the editor window's rows, the feather's panel
— reads a window's place only through one set of
measures (`winleft` and its kin) standing on those
same reckonings, so after a drag a click lands on the
row that stands under it, because painter and pointer
were never reading two places. When windows overlap, a
press on a title bar takes the forward window first —
its bar is the one standing visible. The pointer's
save and laying back are untouched: the arrow is off
the screen while a pass draws, as it always is, and is
laid again at the pass's end over its kept patch, the
whole sixteen-by-seventeen footprint (the pointer
trail fix), so a drag — the pointer moving more than
ever — leaves no trail of it. Tab, Escape, the close
marks, and the typed words (`welcome`, `files`,
`settings`, `editor`, `feather`) all work as before,
from wherever a window now stands.

One building note, recorded honestly: the desk's
numbers are read back unsigned, so a dragged *offset*
from a window's first place — which goes negative the
moment a window moves up or to the left — came back as
a number near four billion on the first bench build,
and the painter wrote to wild addresses and the
machine reset. That is why the places themselves, and
never offsets, are what the desk holds: a place is
never negative, by the clamping above.

Proven by `prove-stone22.sh`: a keeping disk prepared
with two known notes is booted with the shipped disc;
the word `files` opens the files window at its first
place and its rendered list is **decoded letter by
letter** against the system's own letter shapes; the
pointer is laid on its title bar, the button pressed,
and the pointer carried — button held, in small steps
— five cells across and ten rows up. On release the
window renders at the new place: its title, heading,
and list are decoded there, letter by letter. Every
pixel of the ground it stood on that neither its new
place nor the feather window behind it covers is
checked plain black — no remnants, compared the way
`prove-pointertrail.sh` compares the whole desktop. A
press on the second note's row **in the dragged
window** picks that note, its whole words standing at
the window's foot, and a press on the close mark at
the dragged place closes the window.

Honest limits: a dragged window's new place **lasts
only for the sitting** — nothing writes it to the disk
or the disc, and the next boot lays every window where
its measures first reckon it, as before. Dragging is
the pointer's alone: no key moves a window, and the
text face has no windows to move, as it never has. A
window dragged over the desktop's own words (the
invitation, the answers) covers them, and moving it
away leaves the plain desktop there, not the words —
the same manners opening and closing a window have
always kept; `clear` draws the face whole again.

### Stone 23 — The bar's menu

The top bar answers the pointer now: **a press on the
Cardnull bar opens a small menu of plain words** just
under the bar, at the desktop's left — the five
windows' names, one to a row: **Welcome, Feather,
Files, Settings, Editor**, the names the desktop
already gives them. A press on a choice opens that
window (or brings it forward), **exactly as the
choice's typed word does** — the Feather choice asks
for the feather through the door, as the word
`feather` does, and the Editor choice opens the editor
in its picking way, as the word `editor` does. A press
anywhere else puts the menu away without opening
anything, and so does the Escape key — while the menu
stands open, Escape is the menu's, and closes no
window. A press that meets the menu is never a
title-bar drag (Stone 22): while the menu stands open,
every press is the menu's alone, and the bar itself
answers no other press — no window's title bar can
stand in its row, since a drag keeps every window's
top at row 1 or below — so the bar's press is the
menu's alone too.

The menu is desktop chrome, kept under the windows'
own discipline: plain words in the pixel face, no
codes, and **its place reckoned once** — its left,
top, width, and height in letter cells (`menuleft` and
its kin in the main body: left cell 0, top row 1,
twelve wide — room for the longest name, Settings —
and five high, one row to a choice) — read by its
painter and by the pointer's pressing alike, so the
two can never disagree about where the menu stands.
Its standing lives in the pixel face's desk at 268,
with the windows' standings; while it stands open it
is painted last, over everything, and putting it away
wipes its ground back to the plain desktop and paints
the windows again, so whatever stood under it stands
whole once more. A clearing of the face (`clear`) puts
it away too. The typed words keep working exactly as
before, and the bar's clock keeps telling time above
it all.

Proven by `prove-stone23.sh`: the shipped disc is
booted with no disk fitted; a press on the bar opens
the menu and its five rendered choices are **decoded
letter by letter** against the system's own letter
shapes. A press on the Files choice opens the files
window — its title and its plain heading ("There is
no disk fitted.") decoded at the window's own place —
and Escape closes it again, as it always has. The
menu is reopened and dismissed by a press on the plain
desktop elsewhere: every pixel of its ground stands
plain desktop again, no window has opened, and the
welcome window's title still decodes — the desktop
whole. The typed word `files` opens the files window
again, exactly as before. Finally the menu is opened
once more and Escape puts the menu away and no window
with it — the files window's title still decodes — and
the bar's clock still stands at its right end.

Honest limits: the menu is the pixel face's alone, as
the windows are — the text face has no pointer and no
bar to press, as it never has. The menu holds no
standing of its own beyond open or closed: it is not
kept anywhere, and each boot starts with it closed.
(Stone 25 grows the menu by a sixth choice, Rest,
beneath these five — the menu six rows high, its
reckoned place unchanged in kind; see Stone 25's
section. This stone's proof still checks the five it
always checked.)

### Stone 24 — A paint feather

A second feather rides the disc now, and it draws:
**the paint feather** (`src/paint-feather.nifla`,
built with `niflac --bare --guest --feather` like the
welcome feather, riding as its own module `paint.fea`
with its own card at its own head). The word **`paint`**
opens a sixth window — the paint window — and asks for
the feather through **the same feather door** as the
welcome feather: both doormen (BIOS and EFI) now carry
three modules, the boot lift tells the two feathers
apart by the name on the card (`paintmark` in
`featherdoor.nifla` — the name only routes the module),
and **each feather is let in by its own card's
reckoning, on every visit, exactly as the one feather
always was**. Neither's check is weakened by sharing
the door. On its opening visit the feather paints its
whole window into a second block of cells the host
holds and shows 1:1 (the feather-paint fix's
discipline, carried): an invitation in words, a row of
**six color swatches — Red, Green, Blue, Purple,
Orange, Black** — the chosen color **named in words**
("Color: Red" at the opening, the chosen swatch
carrying a star), a **Clear** word on a red ground,
and an empty canvas on a light-gray ground.

**The contract, as it stands, and the shape it
honestly gives.** A feather is handed one number
across the desk (`guestvalue`), the screen it is to
paint (named in the doorstep's top word — here the
paint window's cell block), and the way back
(`guestgive`). It does **not** own the machine: the
compiler refuses a guest the timer, the keyboard, and
the disk, and there is no pointer tool on either side
of the door — so a feather cannot hear the mouse
itself, and this one does not pretend to. What the
contract does carry is the desk, used as a
conversation of visits: while the paint window stands
open, **a press of the pointer inside its shown cells
is carried across the desk as another visit** — gift
1000 plus the press's row times 100 plus its column,
in the very cells the feather paints — and **the
feather itself reckons what the press means**: a
press on the swatch row chooses that color, a press
on the Clear word empties the canvas, a press on the
canvas paints that cell in the chosen color, and a
held drag paints as it goes, press by carried press.
The host is a courier of presses and a keeper of
cells; **every mark in the canvas is the feather's
own**, laid in answer to a press it was handed. The
chosen color is the feather's keeping too, and since
a feather's heap is fresh each visit, it lives where
it can stand between visits: in the cells themselves,
as a figure in a cell the window never shows. The
paint window itself is a window like the others — it
drags by its title bar, Tab reaches it, Escape and
its close mark close it — and the bar's menu keeps
its five choices: `paint` is a typed word, as the
feather's own word has always been a word.

Proven by `prove-stone24.sh`: the shipped disc is
booted at the BIOS door, the word `paint` is typed,
and the door's plain-words line ("The paint feather
visited. Pick a color, then draw.") is **decoded
letter by letter**, as are the feather's invitation
and its named color in the window; the six swatches
are read back in their colors and the canvas empty.
Then the bench's PS/2 mouse — the real pointer road —
**presses a canvas cell** (it stands Red), **drags**
across the canvas (the crossed cells stand Red),
**presses the Blue swatch** ("Color: Blue" decodes,
the star stands on Blue and has left Red), **presses
the canvas again** (Blue), and **presses Clear** —
every painted cell back to the canvas ground, the
swatches and the chosen color still standing.

Honest limits: the drawing lives for the sitting —
the canvas stands in the host's kept cells, nothing
writes it to a disk, and a reboot starts with an
empty canvas and Red chosen. The canvas is the
window's shown region (seven rows by forty-eight
cells of the cells' reckoning), and its colors are
the six a cell's ground can honestly be among the
first eight of the sixteen — bright grounds would
fall under the color byte's blink reckoning, so they
are not offered. A press is carried once a pass of
the main loop at most, so a very fast drag can step
over a cell the way a fast hand steps over a square
of paper. The paint window is the pixel face's, as
every window is: on the text face the word `paint`
is answered plainly, as `files` and `editor` are. And
the door's standing honesty is unchanged: host and
feather share one privilege level and one memory, the
card proves the bytes match it and nothing more, and
a faulting feather stops the whole machine.

### Stone 25 — A kind shutdown, with restart

The machine can rest now, kindly. The word **`rest`**
offers the resting, and so does the bar's menu, which
gains a sixth choice, **Rest**, under Stone 23's five
window choices (the menu is six rows high now, its
place still reckoned once and read by painter and
pointer alike; Stone 23's proof still checks its five,
and this stone's proof checks all six). Choosing Rest
offers **two plain-words choices**: on the face of
light a small panel stands at the desktop's middle —
its place reckoned once, like the menu's — headed
**Rest**, with **Shut down** and **Restart** one to a
row, and a third row, **Stay**, which simply puts the
panel away; a press anywhere else, or Escape, puts it
away too. On the text face, which has no pointer, the
word offers the choices in words and the next typed
line names one. The words **`shutdown`** and
**`restart`** name the two choices directly as well.
The panel's standing lives in the pixel face's desk
at 292, beside the menu's. The doors themselves —
the ACPI power word, the reset words, the final
halt — live in a new library, `src/rest.nifla`; the
kernel is still several files, never one big one.

**The flush, said truthfully.** Either choice first
flushes the disk — and what "flush" honestly means
here is narrow, because this system keeps no cache of
its own: every keeping (a note, a settings choice, a
time-choice word) is a completed disk writing at the
moment it is made, through `diskwrite`, and nothing
is held back anywhere in the system. So the resting's
flush is a **final writing-through**: when a disk is
keeping things, the kept settings card and the whole
notes page are written once more, whole, through the
same `rememberall` and `notesave` every keeping has
always used — and then the drive is sent **its own
flush word** (the ATA flush-cache command, 0xE7, in
`diskkeep.nifla`'s `ataflush`, its waits bounded), so
anything the drive itself still holds in its own
cache is committed too. That is all the flushing
there honestly is, and it is done before either
resting, whichever was chosen.

**Shut down** then says its goodbye in plain words —
"Goodbye for now. Thank you for using this
computer.", and, when a disk is keeping things, "Your
notes and choices are kept on the disk." — and tries
the ACPI power doors (`powerofftry` in
`src/rest.nifla`): a sixteen-bit word to the ACPI
power-management control door, the sleep-enable bit
standing with that door's sleep kind for turning off
whole. The doors are tried in turn — a door a machine
does not have takes the word into unclaimed air and
nothing happens. **The bench's own door was measured,
not guessed**: read back through the bench monitor
from the machine's own ACPI tables, its FACP names
the control door as **0x0604** and its DSDT's \_S5
package gives sleep kind 0, so the bench's word is
0x2000 to 0x0604, and that door stands first. The
wider doors other machines carry stand after it
(0x6004 with both sleep kinds, the older 0xB004, and
0x4004). Recorded honestly, as this house keeps its
corrections: **the first building of this stone tried
the wider doors first and the bench stayed on** — the
machine said its goodbye, printed the fallback below,
and halted, and the stone's proof passed on the
fallback ending until the tables were read and the
bench's true door (its power base is 0x0600, not
0x6000) stood first. If every door leaves a machine
on, the fallback stands: plain words say "The machine
is still on. It is now safe to turn it off.", and the
machine **halts where it stands** — interrupts off,
the processor sleeping in its halt loop, the goodbye
standing on the screen. On the shipped build the
bench does not reach it: the machine powers off.

**Restart** flushes the same way, says "The machine
will start again now." (and the kept-on-the-disk line,
when it is true), and resets the machine through the
reset doors (`machinerestart` in `src/rest.nifla`):
first the **keyboard controller's reset word** (0xFE
at its door 0x64, through the mouse library's own
bounded wait and writing — the same controller the
pointer speaks to), then the **reset control door at
0xCF9** (the PCI reset door beside the configuration
door at 0xCF8): its hard-reset word, then its
system-reset word. No triple fault is provoked, on
purpose. The machine boots again fresh, and what was
kept before the rest is read back from the disk as it
rises, as at every boot — a note kept before a restart
is there after it, and the settings choices with it.
If neither reset door answered, the machine would say
so in plain words and carry on; on the bench the
controller's word answers at once.

Proven by `prove-stone25.sh`, both halves exercised
for real on the real roads. **Shutdown:** a keeping
disk is fitted; a note is kept by the word `note` and
seen in the files window; the bar's menu is opened
and its **six** choices **decoded letter by letter**;
a press on Rest opens the panel and its four rows are
decoded; a press on Shut down rests the machine —
and the bench's ending is the true one: **the machine
actually powers off under QEMU** (it was gone before
the harness could even send the press's release; the
monitor's door closed under its hand, and the
scenario records the ending in a file the script
reads back, since after any ending the harness's own
quit makes the process gone either way). The disk's
bytes are then read: the CNN3 header counts the note
and its sector carries its words, and the settings
card stands — nothing kept was lost. **Restart:** a
note is kept, the word `rest` opens the panel, a
press on Restart resets the machine, and the scenario
watches the desktop **fall** and **rise a second time
in the same QEMU run** — the drawn desktop standing
again, the welcome window's title decoded again — and
then opens the files window and reads the note kept
before the restart standing in its list, read back
from the disk by the second rising. The whole earlier
proof set passes unchanged — Stone 23's included, its
five window choices standing where they always stood,
with Rest beneath them now.

Honest limits: the power doors are the known doors
named above, tried in turn — a machine whose firmware
names some other door in its tables would stay on and
reach the fallback, which is exactly what the
fallback is for; the tables themselves are not parsed
by the system (the bench's were read by the bench's
own monitor, by hand, and the door the tables named
stands first in the trying). The rest panel and the
menu's Rest choice are the face of light's, as every
window and the menu are; the text face's resting is
the typed gate, whole and plain. A draft being
written in the editor window when Rest is chosen is
a sitting's draft, as it always was — what was *kept*
is what the flush writes through, and the panel's
choosing is a person's own act, like closing a window
on a draft. And the drawing in the paint window lives
for the sitting, as Stone 24 said: a restart starts
with an empty canvas, as a reboot always has.
(Stone 26, below, keeps the picture on a keeping disk
now; that line stands as the record of how it was,
and Stone 26's own limits say where it still holds.)

### Stone 26 — Paint keeps its pictures

The paint feather's drawing stays now, when a disk is
keeping things: **a picture drawn in the paint window
is kept on the fitted keeping disk and stands again
after a restart**, with its colors as drawn, and the
files window can open it again.

**The shape of the keeping, said plainly: it is the
host's, and the feather is unchanged.** A feather is
refused the disk by the compiler — that refusal stands
exactly as it always has — and it needs no disk: the
host already holds the painted cells between visits
(that holding IS the canvas, Stone 24), so the host
keeps the picture. After every press visit that stands
— each one still received through the door's full
reckoning first, the card parsed and the FNV-1a-64
check run, nothing weakened — when a disk is keeping
things, the host writes the feather's painted region
through to the disk at once, and the files window's
standing follows. The picture lives in the disk's
store beyond the notes page, in the store's own style
(`picload` and `picsave` in `src/diskkeep.nifla`): a
header on **sector 80** — the letters C, N, P, one byte
saying whether a picture stands kept, and the feather's
chosen-color figure — and the region itself on
**sectors 81 to 83**: the cells the feather paints
(the text reckoning's rows 10 to 20, columns 14 to 65),
a letter byte and a color byte to a cell, exactly as
the feather left them. Nothing already kept moves:
the settings card still stands on sector 8, the notes
page on sectors 64 onward, and the setup clearing
(sectors 0 to 63) reaches neither, as it has never
reached the notes. At boot a keeping disk's picture is
read back into the main body's keeping, and when the
paint window is next opened — the word `paint`, or
the files window's opening below — the feather's
opening visit paints its fresh window as it always
has, and the host then lays the kept region back into
the cells over it: the invitation, the swatches with
their star, the named color, and the canvas, every
cell as it was left, and the chosen-color figure back
at the cells' own keeping cell, so the feather's next
press reckons from the color the picture was left in.
A picture stands kept while any canvas cell stands
painted; clearing the canvas clear through lets the
keeping go, and the header says so. Marks drawn before
a disk is given over at the gate are kept with the
rest at the first press after the gate's yes, because
what is written is the whole region as it then stands.
With no keeping disk, painting is exactly as Stone 24
left it — for the sitting only — and Paint says
nothing of keeping at all, as it never has.

**The files window opens it again.** The window lists
the kept picture beside the notes, in plain words, on
a row of its own at the window's foot — **"A picture
you painted"** — and the window grew by that one row
(it is fifteen high now; nothing above the new row
moved). The pick runs over the notes and then the
picture: the arrow keys can pick it, and the window's
foot then names it ("The picture you picked:") and
says how it opens ("Press Enter or click it to open
it in Paint."). A press on its row, or Enter while it
stands picked, opens the paint window with the
picture standing in it, through the same opening the
word `paint` makes. The window's standing for the
picture lives in the pixel face's desk at 296, beside
the others'.

**One building finding, in the open, as this house
keeps them.** This stone's first bench build never
rose: the screen stayed at the firmware's text shape,
and the founding proofs failed with it. The fault was
not in the stone's logic — the same kernel booted and
answered through the bench's own loader — but in
measure, the very fault the feather-card adoption
recorded at the BIOS door (see its section below): the
BIOS doorman stages the system file at 0x40000 under a
192 KiB claim, with the modules staged above it, and
this stone's growth carried the staged file's span
past that line (its text reaching 0x719AD in the
stage, where the baseline reached 0x6FF35 — two
hundred and three bytes under the line). The staged
settings then splashed the staged system's tail, as
in the adoption's telling, and the machine never
rose. The remedy is the adoption's own: the doorman's
header now claims 224 KiB for the system's stage, and
the module stages stand above the whole of it —
settings at 0x78000, the feather at 0x7A000 (its
56 KiB claim ending where the paint feather's stage
begins, as before), the paint feather at 0x88000, all
below the firmware's own reserved ground. The EFI
doorman needed no move: it lays the system's segments
directly and stages no file. The full proof set below
was re-run on the moved stages.

Proven by `prove-stone26.sh`: a keeping disk prepared
with its Eastern card and one known note is booted;
the word `paint` opens the feather and the bench's
mouse **draws** — a Red cell, the Blue swatch, a Blue
cell — on the real pointer road; the word `files`
lists the note and **"A picture you painted"** beside
it, **decoded letter by letter**, and a press on the
picture's row opens it again in the paint window. The
disk's own bytes are then read: the header on sector
80 (its kept byte standing, its figure the Blue '2'),
the two drawn cells' color bytes standing in the
region on sectors 81 to 83, an untouched cell on the
canvas ground, and the settings card and the CNN3
header unharmed beside the new store. A **second
boot on the same disk** — nothing drawn yet in that
sitting — finds the files window listing the picture
still; the down arrow picks it, its foot is decoded,
and **Enter opens it in the paint window with its
cells decoded back against what was drawn**: the Red
cell Red, the Blue cell Blue, an untouched cell on
its ground, "Color: Blue" standing with the star on
the Blue swatch. The neighbouring proofs pass with it
— Stones 24, 19, and 25, the feather start fix, the
ISO proof, and, because the doorman's stages moved,
Stones 9 and 16, with Stones 15, 20, 21, and 23
beside them. Stone 22 passes too, its proof's own
reckoning of the files window's place updated for
the window's new height — the one measure this stone
changed — its ground check scanning the whole true
place exactly as before. (Two bench notes, kept
honestly. In this stone's regression run,
`prove-stone25.sh` once failed a single check — the
rest panel's "Restart" not decoding within its poll
in boot 2 — while the restart itself, the second
rise, and the kept note all stood in that same run;
the proof passed clean, whole, on its re-run, the
bench's reading race the earlier stones' notes also
record, not the system's. And `prove-stone17.sh`
stood intermittent on this bench throughout: it
passed whole, and in other runs its stick boot was
refused at the loader — "the disc could not be read
as its own" — a refusal reproduced the same way on
the unmodified baseline build, so the intermittency
is this bench's USB road, not this stone's stages;
the proof's shape audit passed in every run.)

Honest limits: one picture is kept — the paint
window's one canvas — not a gallery of them; a new
drawing writes over the kept one as it is drawn, press
by press. The keeping is the disk's CNN3-style store
of this system, in its own shape, as the notes are —
no other system would read it as a picture file. The
paint window and the files window are the face of
light's, as they have always been: on the text face
the picture still stands kept on the disk, but no
window there shows or opens it, and the word `paint`
is answered as it always has been there. And the
door's standing honesty is unchanged, for the keeping
as for the drawing: host and feather share one
privilege level and one memory, the card proves the
bytes match it and nothing more, and the host's
keeping trusts the cells the feather laid — it keeps
them verbatim, and reckons nothing of its own into
them but where they live.

### Stone 27 — Letting a note go

A kept note can be **let go** now — removed, in plain
words, from the files window and from the editor
window — and **nothing is removed without a plain-words
asking first**. Stone 15's honest limit ("there is no
erasing or editing of a kept note yet") is half retired:
editing came at Stone 21, and erasing comes here.

**In the files window**, while a note stands picked,
**"Let this note go"** stands in white at the foot's
right, beside "The note you picked:". A press on those
words — or **Enter while the note stands picked**, the
window's own acting key, as Enter on the picked picture
opens it (Stone 26) — opens the asking on the window
itself: **"Let this note go for good?"**, the note's own
words beneath it, and two choices, one to a row —
**"Yes, let it go"** and **"Keep it"**. **In the editor
window** the same words stand while a note stands picked
in its picking way (at its foot's right, beside the
keeping word) and while a note stands open in its
writing way (under "Press Enter to keep the note."); a
press on them opens the same asking there, over the same
store. A new note being written has nothing to let go,
and none is offered.

**The asking is built so Enter alone can never let a
note go:** it opens with **"Keep it" standing picked**.
The yes must be chosen on purpose — the up and down
arrow keys move the asking's pick and Enter does the
picked choice, or a press lands on a choice's row.
**"Keep it" leaves the note exactly as it was** — and so
do **Escape**, which stands in the asking's way as it
stands in the menu's and the rest panel's (it puts the
asking away and closes no window), and **closing the
window**, whose close mark puts the asking away with
it. While an asking stands, its window's list does not
pick and the editor's draft does not take letters: the
asking is the window's whole business until it is
answered or put away.

**The removal goes through the store's own path** — the
very `notesave` the editor's keeping writes through
(Stone 21), over the same page in the main body's
keeping. The notes after the let-go one move up a place
in the page, in their order; the place the last note
leaves is wiped in the page; and the page is written
through **twice** — once with the old count, so the
wiped place's sector is wiped on the disk too, and once
with the new count, so the CNN3 header and the standing
notes are the disk's truth. After a restart the let-go
note is gone from the files window and the editor alike,
the remaining notes stand whole and in their order, and
the raw bytes agree: a let-go note's sector no longer
reads as a kept note. No parallel store was invented;
the header on sector 64 and one sector to a note from
sector 65 are the whole of it, as they have been since
Stone 15. **A note kept only for the sitting is let go
the same way**, in the page alone — and so the files
window now **lists a sitting's notes too**, under their
honest heading ("Notes kept only for this sitting:"),
picked and let go there as the editor has always shown
them; with no notes at all its plain no-disk words stand
exactly as Stone 19 left them. The windows' asking
standings live in the pixel face's desk at 300 to 316,
beside the others'.

**One building note, in the open:** this stone's growth
carried the kernel's staged segment end from 203,181 to
219,902 bytes — the headroom under the BIOS doorman's
224 KiB claim (Stone 26) narrows from 26,195 bytes to
**9,474 bytes**. No stage moved: the claim still holds
the whole system with room to spare, and the full proof
set below was run on it as it stands. The next stone
that grows the kernel by more than that headroom must
move the stages again, the adoption's own remedy, and
say so.

Proven by `prove-stone27.sh`: a keeping disk prepared
with three known notes is booted; in the files window
a press on "Let this note go" opens the asking and its
words are **decoded letter by letter** — the question,
the note's words, the yes unpicked and "Keep it"
picked — and the **cancel paths are proven before any
removal**: a press on "Keep it" leaves all three notes
whole, and Escape after Enter opens the asking leaves
the first note whole at the window's foot. Enter, up,
Enter then lets the first note go (the second stands
first, whole, the third second); in the editor window
the third note is picked, its asking opened by a press
on the foot's words, and a press on "Yes, let it go"
lets it go. The disk's own bytes are then read: the
CNN3 header counts **one** note, its sector carries
"call billy about the roof" whole, the two let-go
notes' sectors are **wiped**, and the settings card
stands unharmed. A **second boot on the same disk**
finds the files window and the editor listing the one
remaining note and neither let-go one. A **third boot
with no disk at all** keeps two notes for the sitting,
lists them in the files window under their honest
heading, and lets the second go by keyboard with the
same asking. The neighbouring proofs pass with it —
Stones 19, 21, 26, 15, and the ISO proof, and Stone 22
beside them (the files window's place and height are
unchanged; nothing it reckons moved).

Honest limits: letting go is the two windows' — the
face of light's, as they are; the text face's word
`notes` still only shows the page, and no typed word
removes a note. In the editor's writing way the offer
is the pointer's (the draft owns the keyboard there,
as it always has); the picking way's offer is likewise
taken by a press, while the files window's asking is
reachable by pointer and keyboard alike — and in both
windows the asking itself is answered by pointer or by
arrows and Enter. A note let go is gone: there is no
bringing it back, which is exactly why the asking
stands in front of it and opens on "Keep it". The
picture in the files window is not a note and cannot
be let go here — clearing the paint canvas lets its
keeping go, as Stone 26 said.

### Stone 28 — Large print

The desktop's words can stand **larger** now, by a
choice in the settings window: a third choice stands
there, in plain words, set by clicking like the other
two — **"Words:"**, with **"Usual size"** and
**"Large"** one to a row, the standing one white on
blue with the pick mark, the window's own way. The
window grew by the rows the choice takes (sixteen
high now; its keeping word moved down by the same
rows, and nothing above it moved).

**How the scaling is done: a scale reckoning in the
face's own text path, not a second font.** The letter
cell's size in pixels stands in the pixel face's desk
at 320 — sixteen at the usual size, twenty-four at
large — and everything reads that one measure:
`pixbegin` reckons the face's grid from it (1024×768
holds sixty-four by forty-eight cells at the usual
size, forty-two by thirty-two at large), `pixglyph`
draws the one hand-drawn 8×8 font (`src/font.nifla`)
at twice size or three times size by it, every
window's painting lays its cells out by it, and every
pointer reckoning in the main loop — the settings
window's choice rows, every window's rows and close
marks, the menu, the rest panel, the drag's taking
hold and following — divides and multiplies by it, so
painter and pointer agree everywhere at either size,
the discipline the windows have kept since Stone 14,
now kept across a change of size itself. Switching
size in the window lays the new measure in the desk,
begins the face again on the new grid, lays the
windows at their first places there, and repaints the
desktop whole at once — the way switching time moves
the bar clock at once.

**The one exception, by its own standing rule: a
feather's cells are carried 1:1, never scaled** (the
feather window's discipline since Stone 14, the paint
window's since Stone 24). At large print the feather
and paint windows' frames and titles grow with the
words, and the windows stand as many large cells wide
as the carried panel needs — but the cells a feather
painted stand at sixteen pixels inside them at either
size, counted in pixels from the window's corner by
both the painters and the pointer's carried presses,
exactly where the cell reckoning has always put them.

**The choice is kept the way the chime is kept:**
on the fitted keeping disk's settings card (sector
8), which grows by one byte at its end — the size
byte, fifth on the card: 1 when the words stand at
their usual size, 2 when they stand large, and 0 when
no choice was ever kept there, so **a card laid
before this stone keeps the usual size**, as the
words always stood — Stone 20's chime-byte pattern,
followed exactly. It is read at boot in preference
order like the other choices (the disk's card over
the disc's standing), a click on a keeping disk
writes all three choices through at once, and the
typed time words and the resting's final
writing-through keep the size byte as they keep the
chime's. With no keeping disk the choice lasts for
the sitting, and the window says so the way it
already does for the other choices.

**One building note, in the open:** this stone's
growth carried the kernel's staged segment end from
219,902 to **224,274 bytes** — the headroom under the
BIOS doorman's 224 KiB claim (Stone 26) narrows from
9,474 bytes to **5,102 bytes**. No stage moved: the
claim still holds the whole system with room to
spare, and the full proof set below was run on it as
it stands. The next stone that grows the kernel by
more than that headroom must move the stages again,
the adoption's own remedy, and say so.

Proven by `prove-stone28.sh`: a keeping disk prepared
with an **old-shape card** (its size byte 0, as a card
laid before this stone carries) is booted; the word
`settings` opens the window and its new choice is
**decoded letter by letter** against the system's own
letter shapes ("Words:", "Usual size" picked, "Large"
unpicked); a press on the Large row repaints the
desktop at the large size, and the bar's title and
clock, the window's title, labels, choices, and
keeping word are **decoded letter by letter at the
new scale** — the decode is itself the measure of the
bigger words, and the bar stands **twenty-four pixels
tall** where it stood sixteen, its frame spanning
forty large cells. The welcome window is then
**dragged at the large size** and decoded at its new
place with its ground left plain; a press on the
chime-off row at the large size stands the chime off;
and the typing line's echo and an answer are decoded
at the large size. The disk's bytes are then read:
the card carries offset 59, chime byte 2, **size byte
2**. A **second boot on the same disk**, choosing
nothing, rises **large from the card** — title and
clock decoded at the large scale, both choices as
they were left — and a press on "Usual size" there
brings the usual size back at once (the card then
carries size byte 1, the chime byte still 2). A
**third boot on a fresh old-shape disk** rises at the
usual size, "Usual size" picked and the chime on, as
such a card has always behaved. A **fourth boot with
no disk at all** reads the plain sitting-only words
back at both sizes and clicks the words large for the
sitting. The neighbouring proofs pass with it —
Stones 8, 9, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22,
23, 24, 25, 26, and 27, the feather start fix, the
feather paint fix, the pointer trail fix, the
no-witness proof, and the ISO proof. (One bench note,
kept honestly: in this stone's regression run
`prove-stone8.sh` once failed a single check in one
boot and passed whole, every check, on each of two
re-runs — the bench's timing, of the kind the earlier
stones' notes record, not the system's; and Stone
20's own proof had its settings reckoning updated for
the one measure this stone changed — the keeping
word's row, which moved down with the taller window —
exactly as Stone 26 updated Stone 22's proof for the
files window's new height.)

Honest limits: large print lives on the **face of
light only** — the text face (fallback) stays exactly
as it is, as the windows themselves have always been
the face of light's. On the narrower grid the bar
holds the **clock alone** — the date and the title
cannot both stand beside it at this size, and the
word `time` still tells the date in full, as it
always has — and the invitation names the words that
fit, leaving the rest unnamed as it has always left
words it has no room for; every word still answers to
its name. The longest fixed lines (the welcome
window's verse among them) reach the grid's edge at
large size and are cut there, as any line is at the
face's edge; answers wrap at the narrower width, as
they always have at the grid they are given. A
dragged window's place is forgotten at a size switch,
as it is at a reboot: the windows return to their
first places on the new grid. And the settings window
at its standing place now reaches the desktop's foot
at either size — its keeping word stands on the
typing line's own row, and paints over it while the
window stands open, as the files window's foot has
always done at its place; typing paints the line
again, as it always has.

### Stone 29 — A verse window

A **seventh window** stands on the desktop now, titled
**Verse** in plain words, opened by the typed word
`verse` and by a new choice in the bar's menu. It
carries **a verse of Scripture**, standing whole in
the window with its reference named plainly under it
— the window is fifty-four cells wide at the usual
size, and the verse is wrapped by the window's own
painter at the window's width (fifty letters at the
usual size, thirty-six at large), so the whole verse
stands at **both print sizes** through Stone 28's one
scale measure, as every window's painting does. The
window keeps the windows' discipline entire: framed,
its close mark closes it, Tab brings windows forward
in their turn (seven now, the verse window last
before the round begins again), Escape closes it,
and it drags by its title bar.

**The kept set** stands in its own library,
`src/verses.nifla`, in the pattern of `src/rest.nifla`:
**twelve beloved verses in exact World English Bible
wording** — the wording the desktop already carries,
as the welcome window's Psalm 127:1 is WEB — each
with its reference: Genesis 1:1, Psalm 23:1, Psalm
46:1, Proverbs 3:5, Isaiah 41:10, Matthew 11:28, John
3:16, John 10:11, Romans 8:28, Philippians 4:13,
Hebrews 11:1, and 1 John 5:13. The wording is copied
from the World English Bible as published, never
paraphrased and never mixed with another translation.

**Which verse stands is reckoned simply, and in the
open:** when the window is opened, the day is counted
from the date the desktop itself shows — the true
clock's reading (Stone 7) turned by the kept time
choice, the same date the bar's clock and the word
`time` speak — as days since New Year's Day 1970, and
that count is taken around the kept set of twelve.
So a new day brings a new verse, and the same day
brings the same verse every time the window opens.
**Nothing is kept about which verse was seen** — no
mark is made on any disk, and the system makes no
claim to remember it. The bar's menu grew by the one
choice: its seven choices now stand Welcome, Feather,
Files, Settings, Editor, **Verse**, and Rest — Rest
moved down one row, and Stone 25's proof, which
presses Rest by its row, had its reckoning updated
for that one moved measure, exactly as Stone 26
updated Stone 22's proof and Stone 28 updated Stone
20's.

**One building note, in the open:** this stone's
growth carried the kernel's staged segment end from
224,274 to **234,640 bytes** — past the BIOS
doorman's 224 KiB claim — so the doorman's stages
were moved the way Stone 26 moved them, and the
doorman's header says so: the claim stands at
**256 KiB** now, and the module stages stand above
the whole of it (the settings at 0x80000, the feather
at 0x82000, its 56 KiB claim ending where the paint
feather's stage begins, the paint feather at
0x90000), all below the firmware's own reserved
ground. The headroom under the new claim is
**27,504 bytes**.

Proven by `prove-stone29.sh`: the disc is booted
twice with no disk fitted, the bench clock pinned at
2026-11-15T00:00:00 on the world's standard time —
with the disc's Eastern choice the desktop's date is
November 14, 2026, a count of 20,771 days, which
taken around twelve stands at the twelfth verse,
**1 John 5:13**. In the first boot the word `verse`
opens the window and the verse standing in it is
**decoded letter by letter** against the system's own
letter shapes, its wrapped lines joined back into the
verse's **exact WEB wording**, its reference decoded
under it; Tab brings the welcome window forward, the
word brings the verse window forward again, Escape
closes it; the bar's menu is opened and its **seven
choices decoded**, a press on the Verse choice opens
the window again, and a press on its close mark
closes it (38 checks across the two boots). In the
second boot the settings window's Large row is
pressed, and the same verse stands whole in the
window at the **large size**, wrapped at the narrower
width, decoded letter by letter at the large scale.
The neighbouring proofs pass with it — Stones 14, 23,
25 (with its updated reckoning), and 28, the feather
start fix, and the ISO proof, which boots the shipped
disc itself through the moved doorman.

Honest limits: the verse is reckoned **when the
window opens** — a window left open across midnight
keeps the verse it opened with until it is closed and
opened again, and nothing anywhere records that any
verse was seen. The set is **twelve verses, fixed**:
there is no "another verse" choice — the day's
turning is the choosing, as it is stated above. If
the machine gives **no true clock reading** at all,
the first verse of the set stands (Genesis 1:1) — the
reckoning says so plainly rather than pretend a date
it does not have. And the verse window lives on the
**face of light only**, as every window does: on the
text face the word `verse` is answered in plain
words — "This face has no windows to open."

### Stone 30 — A calculator feather

A third feather, and the first that reckons: a real
working calculator, a guest program written in Nifla
(`src/calculator-feather.nifla`), built with the bare
guest/feather toolchain like its sisters, riding the
disc as its own module — `calc.fea`, a **fourth
module** beside the settings, the welcome feather,
and the paint feather — and received through the
same door, by the same card and the same reckoning,
as every feather. Both doormen grew to hand it over:
at the BIOS door the paint feather's stage claim
stands at 32 KiB (0x90000) and the calculator stages
above it at **0x98000**, its 32 KiB claim ending at
0xA0000 where the firmware's reserved ground begins,
with a fourth entry in the module table; at the EFI
door the doorman reads `\boot\calc.fea` the same way.
The kernel's first-breath lift routes the fourth
module by the name on its card, as it routes the
paint feather; the name only routes — each feather
is still let in by its own card's reckoning at the
door, or not at all.

The word **`calculator`** opens its window — title
**Calculator** — and the bar's menu gains the choice
with it: the menu stands at **eight choices** now,
Calculator the seventh and Rest last, and the proofs
that decode the menu (Stones 25 and 29) moved with
it, as they have each time the menu grew. The window
keeps the full discipline of its sisters: framed,
titled, close mark, forward and Escape and dragging,
Tab cycling eight windows, right at both print sizes
with the carried cells at sixteen pixels.

The contract's shape is Stone 24's, **unweakened**,
and it is stated plainly, as Stone 24 stated its
finding: a feather cannot receive live pointer input
while it runs — each visit is one synchronous call,
one number in, the painted cell block, one number
back — and **every visit runs the full card parse
and FNV-1a-64 reckoning before anything is laid at
the doorstep**. So the person drives the calculator
the way Paint is driven: the host carries each press
of its painted keys across the desk as a fresh,
checked visit — the gift 1000 plus the press's row
times 100 plus its column, in the painted cells' own
reckoning — and the feather itself reckons what the
press means. Its standing lives where Paint's canvas
lives: **in the painted cells**, in a row the window
never shows — the sum's size laid byte by byte in
base 256 with its sign beside it, the number being
typed the same way, the working waiting, and the
rest of the standing — held by the host between
visits, and read back by the feather at the next
visit's start. The sum is therefore truly kept
across visits, not remembered by the host: the host
reckons nothing of what a press means.

Its face is plain: an invitation — "Press the keys
to reckon a sum." — the sum's line standing black on
light gray, the figure keys white on blue, the
workings' keys white on purple and named in plain
words — **Add**, **Take away**, **Times**, **Share
out** — Equals white on green, and Clear white on
red. The line shows the standing as it grows ("12",
"12 add", "12 add 3"), and Equals paints the
answered line whole ("12 add 3 is 15"). A working
taken up against a standing reckoning reckons that
reckoning first; Equals with no second number uses
the sum as its own; a figure pressed after an
answered sum starts a new reckoning; Clear starts
again.

Honest scope, stated exactly: the calculator reckons
in **whole numbers**. A number being typed holds at
most **six figures** — further figure presses are
let go. An answer's size is held to
**999,999,999,999**; a sum past that is answered
**"That sum is too big."** and the next figure
starts fresh. Sharing out answers **whole, with the
remainder named** — "10 share 3 is 3, 1 left over" —
the remainder reckoned on the numbers' sizes, so it
is never below nothing; a sum below nothing is
carried honestly ("5 take 9 is -4"). Sharing out by
0 is checked **before any division is tried** — a
division by nothing would fault the machine — and
answered in plain words: **"Cannot share out by
0."** Never a crash.

And the honest limit of the road, in the open: the
desktop's **typing line cannot reach the feather**.
Typing speaks to the host, and no road in the
contract carries typed figures across the desk — so
the calculator is driven by presses on its painted
keys, as Paint is driven by presses on its canvas,
and not by typing on the line. On the text face the
word `calculator` is answered in plain words, as its
sisters are: "This face has no windows to open."

Proven by `prove-stone30.sh` (60 checks): the disc
is booted at the BIOS door, the word `calculator`
opens the window, the door's plain-words line says
the feather visited, its invitation and its keys'
names and colors are **decoded letter by letter**
off its painted cells, and then real pointer presses
on its painted keys work real sums, the sum's line
**decoded off the feather's cells after each press**
— 7 add 5 is 12; 9 take away 4 is 5; 5 take away 9
is -4; 6 times 7 is 42; 10 share out 3 is 3, 1 left
over; a Clear after each; and 5 share out 0 answered
"Cannot share out by 0.", the machine still
standing. Escape closes the window; the bar's menu
is opened, its **eight choices decoded**, a press on
the Calculator choice opens the window again, and a
press on its close mark closes it. The neighbouring
proofs pass with it — Stones 23, 24, 25 (with its
moved Rest reckoning), and 29 (with its grown menu),
the featherpaint proof, the ISO proof, and the
no-witness proof, the loaders and the disc having
changed under them all.

### Stone 31 — A help window

A **ninth window** stands on the desktop now, titled
**Help** in plain words, opened by the typed word
`help` and by a new choice in the bar's menu. It
explains how Cardnull works — every window and every
word, plainly, the way you would explain it to a
neighbor: what each window is (Welcome, Feather,
Files, Settings, Editor, Paint, Verse, Calculator,
and Help itself), what the typed words do (`hello`,
`time`, `memory`, `clear`, `feather`, `files`,
`settings`, `editor`, `paint`, `verse`, `calculator`,
`help`, `welcome`, `note`, `notes`, `setup`,
`eastern`, `utc`, `chime`, `usb`, and `rest`, with
`shutdown` and `restart` named under the resting),
how to move windows, open the menu, and rest the
machine. The window keeps the windows' discipline
entire: framed, titled, its close mark closes it,
Tab brings windows forward in their turn (nine now,
the help window last before the round begins again),
Escape closes it, and it drags by its title bar. The
bar's menu grew by the one choice: its nine choices
now stand Welcome, Feather, Files, Settings, Editor,
Verse, Calculator, **Help**, and Rest — Rest moved
down one row, and the proofs that decode the menu or
press Rest by its row (Stones 25, 29, and 30) had
their reckonings updated for that one moved measure,
exactly as each earlier menu growth moved them.

**The words themselves** stand in their own library,
`src/helpwords.nifla`, in the pattern of
`src/verses.nifla`: **five short pages of eleven
lines each**, shortened for a window from this
README's own telling, and every claim in them true
of the shipped system — each line checked against
the stones' sections above as it was written. The
window is fifty-four cells wide at the usual size
and forty at large, and **every line is at most
thirty-six letters** — the window's inner width at
the large size — so no line is cut at either print
size, through Stone 28's one scale measure, as every
window's painting reads it. **The pages are turned
two ways:** a press on the window's foot — its plain
turning word stands at the foot's right, **More**,
or **First page** on the last page, which returns to
the first page, with the foot's left naming the page
that stands ("Page 1 of 5") — and the **up and down
arrow keys** while the window stands forward (down
turns forward, as the foot's word does; up turns
back, and stands still on the first page). Opening
the window always stands its first page in it. Its
standing lives in the pixel face's desk at 360 to
372, beside the others' — and the desk grew to 384
bytes to hold it.

**One building note, in the open:** this stone's
growth carried the kernel's staged segment end from
247,106 to **260,128 bytes** — the headroom under the
BIOS doorman's 256 KiB claim (Stone 29) narrows from
15,038 bytes to **2,016 bytes**. No stage moved: the
claim still holds the whole system with room to
spare, and the full proof set below was run on it as
it stands. The next stone that grows the kernel by
more than that headroom must move the stages again,
the adoption's own remedy, and say so.

Proven by `prove-stone31.sh` (120 checks across two
boots): the disc is booted twice with no disk fitted.
In the first boot the word `help` opens the window
and **every page's eleven lines are decoded letter
by letter** against the system's own letter shapes
and compared against the kept help words — the pages
turned by the down arrow and by presses on the
window's foot, the foot's standing and turning word
decoded as they change, First page returning to the
first page, and the up arrow on the first page
turning nothing; Tab brings the welcome window
forward, the word brings the help window forward
again, Escape closes it; the bar's menu is opened,
its **nine choices decoded**, a press on the Help
choice opens the window again, and a press on its
close mark closes it. In the second boot the
settings window's Large row is pressed, and the
first two pages stand whole in the window at the
**large size**, decoded letter by letter at the
large scale, the second reached by the down arrow.
The neighbouring proofs pass with it — Stones 14,
23, 25 (with its moved Rest reckoning), 28, 29 and
30 (with their grown menus), the feather start fix,
and the ISO proof.

Honest limits: the help window lives on the **face
of light only**, as every window does: on the text
face the word `help` is answered in plain words —
"This face has no windows to open." The words are
**five fixed pages**: there is no searching them and
no asking them questions — they tell the system's
working as it stands at this stone, and a future
stone that changes a window or a word must change
these words with it, as the menu's growths have
changed the proofs. And the telling is shortened
for a window, as its heading here says: the full
account of each window and word stands in the
stones' sections above, and the window's plain
lines point a neighbor truly, not exhaustively.

### Stone 32 — Ears on the modern USB road

A third road for typing. `src/xhcikey.nifla` is a
second USB host driver written in Nifla, standing
beside the UHCI driver of Stone 6 in the same pattern
— its whole estate in one desk of bytes the main body
hands it — but speaking to a wholly different
controller: an **xHCI**, the eXtensible Host
Controller of the USB 3 years, found on the PCI bus
by its class numbers (serial bus 0x0C, USB 0x03,
xHCI 0x30). Where the UHCI road speaks through I/O
ports, this controller is reached through its
**memory door** — the address its card names (its
BAR) — so the driver reads and writes its registers
as memory, and first lays the page-table reach to
the door's gigabyte quarter when that quarter stands
above the waking map, the very reckoning the face of
light's pixmap lays for its screen (the bench's door
stands at 0xFEBF0000, in the screen's own quarter).
The raising stills the controller, resets it, and
sets it walking with the fields the standard
prescribes: the device context list, a command ring,
one event ring with its table (polled, as every road
here is polled — no interrupts are taken), and the
run word. Each port is then asked in turn whether
anything stands on it; anything standing is reset
(the warm door for a super-speed standing, the plain
door for the rest), and the first device that wakes
as a keyboard is taken.

The waking itself follows the modern road's own
order: the controller is asked for a device place
(its Enable Slot order), the device is addressed
with its control door (the Address Device order —
the control door's packet bound first guessed from
the device's speed, then learned truly from the
description's own seventh byte and re-valued by the
Evaluate order when the guess stood wrong), its
whole arrangement is read descriptor by descriptor
until a boot keyboard's interface is found **by the
same declared numbers the UHCI road reads** (the
HID class 3, the boot subclass 1, the keyboard
protocol 1) with its inward interrupt door, that
door is arranged with the controller (the Configure
Endpoint order), the arrangement is set, the
keyboard is set to its boot manner, and its report
door is armed with one plain transfer block. The
main loop then reads the controller's event ring
once a pass: when the keyboard's door answers, the
report is read and the door armed again, and the
report's presses are turned into the same make codes
every road speaks **by the UHCI library's own
translation** — so all roads feed the one typing
line, and the shift keys and Caps Lock are resolved
by the one shared standing in the main body, exactly
as Stone 12 settled for both roads then standing.
When a keyboard is ready on this road the desktop
says so at boot ("A USB keyboard is ready on the
modern USB road."), and the word `usb` reports this
road's standing in its own line beside the UHCI
road's, with **its own count** of the keys it has
brought.

**The hearing order, stated plainly:** the loop asks
the PS/2 road first, then the UHCI road, then the
modern road — so when more than one USB keyboard
stands ready, the first road in that order with a
key waiting is the one heard that pass; in practice
the UHCI road, asked first, is the one the loop
hears when both carry keyboards. Both USB roads may
stand ready together; neither disables the other,
and neither disables the PS/2 road. With no xHCI
controller, or a controller but no keyboard on it,
the desktop comes up exactly as before and the other
roads carry on — the raising's every wait is
bounded, and a controller that will not raise leaves
the road quiet and the desktop unbothered.

**Which USB this covers, plainly, as it now
stands:** the UHCI companion road of Stone 6 (in
UTM, the **USB 2.0** arrangement, whose keyboards
stand on UHCI companions) and now the xHCI road (in
UTM, the **USB 3.0** arrangement) are both covered. A
**standalone EHCI controller is still not covered**:
a machine offering only an EHCI host and no UHCI
companion would find no controller either driver
speaks, and the PS/2 road would carry typing alone.
One building measure, in the open: this stone's
growth carried the kernel's staged segment end from
260,128 to **285,795 bytes**, past the BIOS
doorman's 256 KiB claim — so the claim was raised
the established way, to **320 KiB**, and the module
stages moved above the whole claim: settings at
0x90000 (a 2 KiB claim), the feather at 0x90800
(6 KiB), the paint feather at 0x92000 (8 KiB), and
the calculator feather at 0x94000 (16 KiB, ending at
0x98000). Above the raised claim only 64 KiB stand
before the firmware's reserved ground, so the
modules' claims stand at their tight measures now,
each with room over its file as it stands; the
headroom under the 320 KiB claim is 41,885 bytes.
The EFI doorman was checked and needed no move: it
stages no file — it reads the system and its modules
from its partition directly to their row at
0x300000 — so no claim of its own stands to grow.

Proven by `prove-stone32.sh`, three boots, all PASS
(16 checks): with an xHCI controller (the bench's
`qemu-xhci`) and a USB keyboard on it, the modern
ready word stands on the desktop, a shifted word
stands capital on the typing line, the `usb` word's
count for the modern road reads **10** — the ten
presses of the typed words and their Enters, carried
by the modern road itself (the count is this road's
own; no other road can raise it) — Caps Lock makes
its capitals by its usage, and small letters answer
again when it is turned off. With the controller but
no keyboard, and with no controller at all, the
desktop comes up unbothered, the PS/2 road answers
as always, and `usb` answers plainly that no USB
keyboard is plugged in. The neighbouring proofs pass
beside it: Stones 6, 12, 18, and 9, the ISO proof,
and the no-witness proof, all on the same build with
the doorman's stages in their new places.

Honest limits: the road is proven on the bench's
controller in the shape the bench offers it — QEMU's
`qemu-xhci` (its capability words read on the bench:
sixty-four device places, eight ports, no scratch
pages asked, the thirty-two-byte context size), with
the keyboard standing at **high speed** on one of its
ports. The driver honors the other context size (64)
and up to four scratch pages in its layings, but
those shapes are **not proven** here, and neither is
a keyboard that itself stands at super speed — the
warm reset door for one is laid, untested by any
device the bench has. A memory door whose high word
is not zero (a 64-bit door standing above the
four-billion line) is passed by, as beyond this
system's present reach, and a controller that does
not walk by the four-thousand-byte page measure
leaves the road quiet, said in its standing rather
than guessed at. One keyboard is woken, the first
that answers; a keyboard standing **behind a hub**
is not woken — no hub is spoken to on either USB
road. A USB mouse on this road is not spoken either:
the pointer remains the PS/2 mouse of Stone 13. And
the road polls its event ring once a pass of the
loop, as the UHCI road polls its door — a key is
heard at the loop's own pace, not an interrupt's.

### Stone 33 — The glass face

The desktop's face, remade as glass. The look Tyler
named is the glass desktop of the Windows 7 years —
but nothing here is Microsoft's: no artwork, no
assets, no borrowed pixels. Every part of the glass
is drawn by Cardnull's own code in Cardnull's own
hand, the style evoked and the making wholly ours,
in the drawing library (`src/pixface.nifla`) and the
main body (`src/cardnull.nifla`).

**The bar stands at the foot now.** It left the top
of the screen and stands two letter rows tall at the
bottom, glassy: a pale sheen band across its upper
part, a mid-glass band under it, a calm blue-green
tint at the seam, and the bar's own blue carrying
its name and its clock on the lower row, where they
have always stood in their colors. The name stands
at the lower row's left, just right of the button;
the clock stands at the right as it always has, with
the date beside it as the size allows — Stone 28's
large-print rule for the bar stands unchanged.

**A round start button stands at the bar's left,
carrying the Cardnull cardinal.** The bird is a
small bitmap in the drawing library, hand-drawn in
the pattern of the font's own letter shapes: a
twenty-four by twenty-four reckoning of the
stained-glass cardinal from Cardnull's own logo —
the crest, the black mask with its white eye, the
orange beak, the gold wing, the long tail — in deep
red and bright red, gold, beak orange, and the dark
lead color standing for the leaded divisions
between the glass. It is drawn at the same honest
size at both print sizes, on a glass disc of its
own: a soft shadow, a lead rim, deep blue-green
glass, and a sheen gathered at its upper left.
**The button, and only the button, opens the
menu** — the Stone 23 rule "a press on the bar
opens the menu" narrowed to the button itself, as
the stone ordered: a press elsewhere on the bar is
a press on the desktop and opens nothing. The menu
rises UP from the button, its foot standing on the
bar's top edge; its nine choices, their order (Rest
last), and their behavior are unchanged, and Escape
still dismisses it and closes nothing.

**The windows wear glass too.** Every window's
frame is drawn with rounded corners — the corner
pixels are left to the ground beneath, said
plainly: a press on a rounded corner's missing
pixel is a press on the desktop beneath it, not on
the window. A gentle sheen band runs across the
title bar's upper part, a blue-green tint strip
stands at the title's foot, and a soft dark shadow
falls five pixels along each window's right and
bottom edges, clipped so it never paints across
the bar. The washes that clear a window's ground
reckon the shadow's reach with the window's own, so
the ground a window vacates stands whole again,
shadow and all — and the pointer's save and restore
of its whole footprint is untouched, so the arrow
still leaves the glass desktop pixel-for-pixel as
it found it.

**Everything underneath works as it did.** Windows
now stand ABOVE the bar: their first places are
reckoned through the same shared measures as
always, and the taller windows' first places rose
to clear the bar's two rows — at the usual size the
files window stands at row 31, settings and help at
row 30; at large print, files at 15, settings and
help at 14, the editor, paint, and calculator at
16, the verse at 18. Dragging by the title bar
clamps a window whole on the desktop above the bar.
The typing line stands one row above the bar. One
help line changed its words with the face: the help
window now says "The round button opens the menu."
where it said "Press the top bar for the menu."

**One honest limit:** the glass lives on the face
of light only. The text face — the fallback the
doorman falls back to when no picture screen is
granted — keeps its own face, as it was; it did not
grow glass.

One building measure, in the open: the glass
drawing carried the kernel's staged segment end
from 285,795 to **294,371 bytes**, still under the
doorman's 320 KiB claim — the headroom under the
claim is **33,309 bytes**, and no stage moved.

Proven by `prove-stone33.sh`, two boots, all PASS
(72 checks): with no disk, at the usual size, the
bar's bands stand sampled at the screen's foot; the
button's cardinal stands proven in its own colors
and shape — lead at the crest, the white eye, the
orange beak, the gold wing; the welcome window's
rounded corner leaves its corner pixel to the
desktop while its frame stands beside it, and its
shadow stands along its right and foot; a press on
the button opens the risen menu and all nine
choices decode letter by letter; the menu's Files
choice opens the files window at its new place,
glass title and shadow standing; the window is
dragged by its title bar and decoded at its new
place, its foot's shadow with it, and the ground it
vacated stands plain; its close mark closes it; the
pointer is carried across the bar, the button, and
a window's shadow and home again, and the whole
desktop — the clock's own ground left out, as time
honestly passes there — stands pixel-for-pixel as
it was found; Rest opens from the menu and Stay
puts the panel away; Escape dismisses the menu and
closes nothing. At large print, from a disk whose
card carries it: the bar stands at the foot in its
large bands, the cardinal stands on the large
button, the menu rises at its large place with all
nine choices decoded, and the files window opens at
its large first place.

The bar's move and the windows' new first places
moved pixels that older proofs read, and those
proofs were updated to the new geometry with the
same letter-by-letter discipline — no check weakened
and none deleted: `prove-nowitness.sh` and
`prove-stone9.sh` (the bar's samples, the title's
band, the typing echo's band, and the clock-diff
region moved to the foot; Stones 16 and 17 ride the
same scenario and pass with it), `prove-pointertrail.sh`
(its whole-desktop difference now leaves out the
bottom bar's clock ground instead of the top bar's),
`prove-stone19.sh` and `prove-stone26.sh` and
`prove-stone27.sh` (the files window's first place,
row 31; Stone 27's editor readings split onto the
editor's own row, 32, which did not move),
`prove-stone20.sh` (the settings window's first
place, row 30, and the bar clock read at the foot),
`prove-stone21.sh` (the files window's rows read one
above the editor's), `prove-stone22.sh` (the files
window's place and the drag's target row, 21; its
vacated-ground reckoning now leaves out the windows'
own shadows, which are the face's paint, not
remnants — the same reckoning Stone 33's own proof
makes), `prove-stone23.sh` (the menu risen at row
37, opened from the button; its nine choices now
decoded, where the proof once decoded five),
`prove-stone25.sh` (the menu at row 37 opened from
the button, Rest's row the typing line's own row,
and the second boot's bar sample at the foot),
`prove-stone28.sh` (the bar's title and clock read
at the foot at both sizes, the settings window's
places at rows 30 and 14, the Large press and the
chime press at their new rows, the typing echo at
row 29 at large print, and the settings frame's span
check now reading the window's shadow past its right
edge), `prove-stone29.sh` (the menu opened from the
button, its choices at rows 37 onward; the verse
window's large place at row 18 and the settings
places), `prove-stone30.sh` (the menu opened from
the button, the Calculator choice at its risen row),
and `prove-stone31.sh` (the help window's places at
rows 30 and 14, the menu opened from the button, and
the help page's own line read in its new words, "The
round button opens the menu."). The full suite passes on the glass build — every
proof green but Stones 1 and 2, spoken of next.
Stones 1 and 2 fail on this bench on the unmodified
Stone 32 build too — checked against the stashed
baseline before any blame was laid — so they stand
as they stood: pre-existing bench failures in the
text-screen proofs, untouched by this stone and
reported in the open rather than repaired under its
name.


### Stone 34 — The drag that no longer flickers

The first of the four glitches Tyler witnessed in
UTM on November 16, 2026, answered at its root:
"when i move windows it flickers the windows."

**The mechanism.** A drag moved its window one cell
at a time, and every step called the whole-desktop
repaint: every closed window washed to black, every
open window redrawn whole — frames, glass, text and
all — straight into the picture screen, with no back
buffer anywhere. Many times a second, windows that
had nothing to do with the move were washed and
redrawn in front of the user's eyes. That
wash-and-redraw shimmer was the flicker. The bench
reckoned it too, in the runtime's own loop passes:
one six-step drag of a window cost 11,765 passes,
nearly all of them repainting untouched windows.

**The fix is scope, not speed.** A drag now repaints
only the road the window travelled — the ground it
left and the ground it took, taken as one stretch of
letter cells — and, within that road, only the
windows whose places touch it. The road is washed
bare, then its windows are painted in the standing
order the whole-desktop repaint has always used
(closed fellows washed in window order, open fellows
drawn in window order, the forward window last), so
the road's final pixels are exactly what the old
repaint would have laid there — the desktop's final
state is unchanged, pixel for pixel. A window
outside the road is never washed and never redrawn,
so it cannot flicker. Two honest edges are kept: an
open window standing where a closed fellow's wash
will fall joins the repaint (the wash would rub a
hole in it that nothing repaints), and while the
start menu or the rest panel stands open — both
paint over everything in their own words — the
whole-desktop repaint keeps its say.

The reckoning stands in `paintregion` in
`src/cardnull.nifla`, beside `paintwindows`. The
road and the window being painted travel through
the desk (its ledger at 384 to 403 in
`src/pixface.nifla`; the desk stands 404 bytes now),
because the machine's registers are already full
with a repaint call's three blocks — the same road
the paint cells' block has always taken. A lone
window's six-step drag now costs 3,685 loop passes,
under a third of the old road's 11,765; a drag whose
road honestly holds several windows costs what
those windows cost, and no more.

Proven by `prove-stone34.sh`: the welcome window is
dragged across a populated desktop while every pixel
below it is hashed — mid-drag, button still held,
the bystanders stand pixel for pixel untouched, and
the drag's loop passes are read out of the guest and
reckoned; the files window is then dragged across
the verse window and back, the crossed window
standing repainted behind it and decoding whole once
brought forward again. The drag proofs of Stones 22,
29 and 33, the pointer-trail proof, and the
no-witness proof pass as they did. As with every
fix here, this is bench-proved; the witness that
counts is Tyler's own in UTM, still to come.


### Stone 35 — The press that no longer flickers the desktop

The second of the four glitches Tyler witnessed in
UTM on November 16, 2026, answered at its root:
"when i paint with multiple windows, all the windows
flicker."

**The mechanism.** Every visit to a feather — the
paint feather above all, which is visited once per
pointer press on its canvas — was bracketed by two
whole-desktop repaints: one as the press landed, in
the pointer's reckoning, and one as the visit was
received. Windows that had nothing to do with the
press were washed and redrawn twice per press,
exactly the wash-and-redraw shimmer of Stone 34,
now keeping time with the painting hand.

**The fix is the same scope, carried to the
visits.** Stone 34's region road now serves the
feather visits too. The press's own repaint and the
receiving's repaint each lay the road over the
visited window alone — widened, when the press
brought a different window forward, to the window
it took the forward place from, whose title bar the
coming-forward repaints in behind colors; and
widened once more, when a disk is keeping the
picture, to the files window, whose list the
keeping can change. Within the road the repaint
keeps Stone 34's standing order, so the road's
final pixels are exactly what the old repaint would
have laid there. A window outside the road is never
washed and never redrawn, so it cannot flicker.
Openings still repaint as openings always have —
the receivings owe only their own window's ground.

The bench reckons the change in the runtime's own
loop passes, on a full desktop with every window
standing open. A press on the calculator's key:
5,201–5,413 passes on the new road, against
5,961–6,966 measured for the old. A press on the
paint canvas: 12,809–12,873, against 13,707–14,706.
The saving is the two bystander repaints that no
longer happen; the visit itself — the feather's own
work, and its window's own redraw — is most of what
remains, and is honestly still there.

Proven by `prove-stone35.sh`, in two boots (on this
bench a second pointer press after a feather-visit
press is not reliable — the emulated pointer's
button keeping desyncs across a long visit — so
each boot makes one press, the way a person makes
one at a time): a calculator press on a full
desktop reckons its 7, a canvas press paints its
cell Red, the welcome window's every pixel stands
hashed and exactly as it stood after each press,
and the presses' loop passes are read out of the
guest and reckoned against the old road's measures.
The calculator, paint-keeping, glass-face, dragging,
pointer-trail, and no-witness proofs pass as they
did. Bench-proved, as every fix here; the witness
that counts is Tyler's own in UTM, still to come.


### Stone 38 — The desktop at the rising

Tyler's steering, November 18, 2026: "make a real
desktop gui like windows 7 or Mac OS for cardnull
instead of being in shell at start up." Until now
the machine woke to its console standing on the
desktop's ground, the typing line and its answers
laid below the windows on the face itself. The
machine now wakes to the desktop alone.

**The console lives in a window.** The terminal
window — the tenth window — stands open at the
rising with its prompt at its foot, and the typing
line and the kept answers live inside it, painted
from the same keeping block they always used.
Closed, it is raised again by the first keystroke,
as the typing line was always the first thing a
keystroke reached; the word 'terminal' brings it
forward, and Escape closes it as it closes every
window. Down the desktop's left edge stand eight
icons — Files, Editor, Paint, Calculator, Verse,
Help, Settings, Terminal, in the order Tyler named
them — each a small picture with the window's own
plain name beside it, and a press on an icon opens
its window, as the start menu's choices and the
typed words do. The words themselves are
unchanged: what a person types is answered in the
terminal, and the words that open windows open
them still.

**The completion sweep.** The stone was built on
November 18 and left standing while the language's
loop guard was re-counted (Nifla Stone 33, which
also cures at the root the paint and calculator
freezes Tyler witnessed — the old Stones 36 and 37
needed no work here). Completed November 19: every
early proof suite was run under the desktop world.
The suites for Stones 3–8, 12, and 18 pass as they
stood (Stones 10 and 11 keep no proof scripts).
Where a suite assumed the shell-at-boot world, its
checks were re-aimed at the places the named
things now stand — the answers inside the terminal
window, the feather reached by the start menu's
Feather choice as the word 'feather' reaches it —
the checks themselves unweakened: Stones 9, 13,
14, 15, and 24, and Stone 16 with them, which
rides on Stone 9's scenario.

Stone 28's one failing check was answered at its
root. At the large size, a terminal answer's first
letters never reached the screen, though the kept
block held the whole line and the tail stood
plain. The loss was pinned to the woven pass in
the terminal row's painting, which laid each
cell's paper and then its letter, cell by cell;
the row is painted in two passes now — the paper
across the whole row first, the letters after —
and the line stands whole at both sizes.

The stick proof's structure checks pass as they
did; its one USB boot proves intermittent on this
bench — for the Stone 35 image as for this one,
the loader's refusal landing at a different
sector from boot to boot — which is the bench's
emulated USB road, not this stone's doing; the
same image boots as a disc every time.

Proven by `prove-stone38.sh`, in four boots and
nineteen checks: the boot arrives at the desktop
itself with no shell face before it, the icons
stand named down the left edge, the terminal
stands open with its prompt at its foot, a press
on an icon opens its window, a typed word's answer
stands inside the terminal, the word 'files'
typed there opens the files window as it always
has, and closing the terminal and typing raises
it again with the answer inside. The Stones 28,
15, 24, 29, and 30 proofs pass with it, and the
early suites as recorded above. Bench-proved, as
every fix here; the witness that counts is
Tyler's own in UTM, still to come.

### Stone 39 — The bar shows the open windows

GUI completeness II, in the ladder planned
November 18, 2026: the desktop had its windows,
its icons, and its menu — but the bar at its foot
said nothing about which windows stood open, or
which one stood forward, except what a person
could see of the desktop itself. The bar tells it
now.

**Presence chips.** The bottom bar — the glass
face of Stone 33, with its round cardinal start
button — carries one plain-words presence chip to
each of the eight windows a person opens and
closes: Files, Editor, Paint, Calculator, Verse,
Help, Settings, Terminal — the names the desktop
already uses, in the icons' order of Stone 38.
The front window's chip stands white on the bar's
blue, as its title bar stands blue; a window
standing behind stands white on light gray, as
its title bar stands gray — the chip tells at the
bar what the title bars tell on the desktop. The
welcome and feather windows keep no chip: they
are the desktop's own first furniture, standing
open from the rising under their title bars at
the desktop's heart, and the chips are for the
windows the icons, the menu, and the typed words
open and close.

**The laying.** The chips are laid along the
bar's upper row from its second cell (the start
button stands in the first two), one blank cell
between chips; when the upper row fills, the
laying goes on at the lower row's middle ground,
from its tenth cell (the bar's name stands in the
eight before it) to where the clock's ground
begins, so no chip ever stands under the button,
the name, or the clock, and the clock's own
redrawing at every tick can never rub one out.
At the usual size the eight names — fifty-one
letters and seven blanks — stand along the upper
row together; at large print, whose bar holds
forty-two cells, the row fills and the last chips
stand on the lower row, as the proof's fourth
boot shows. The laying is reckoned once
(`chipplace` in `src/cardnull.nifla`), and the
painter and the pointer's pressing both read it,
the discipline the icons and windows have kept.
The chips are painted at the end of every whole
repaint — every opening, closing, and
coming-forward — and again after the few region
repaints that move the forward place (the feather
windows' presses and the welcome feather's
visits, Stones 34 and 35's road); the bar's own
ground under the chips is first laid as the bar
itself stands (`pixchipground` in
`src/pixface.nifla` — the sheen bands above, the
tint and blue below), so a closed window's chip
leaves no plate behind and the chips that remain
pack from the row's beginning again. No new desk
standing was needed: the chips read the windows'
standing the desk already keeps.

**Raising.** A press on a chip raises its window
to the front, exactly as a press on the window
itself does — and by the same economy: the
raising repaints by the region road of Stones 34
and 35, the stretch holding the raised window and
the window it takes the forward place from, whose
title bar the coming-forward repaints in behind
colors, and the chips are painted again, for the
front chip's blue has moved. No other window is
washed or redrawn. A press on the front window's
own chip is the chip's still: the window already
stands forward, and nothing is repainted. No chip
minimizes, and no chip opens a closed window —
presence and raising are the whole of the stone.

**One latent fault of the baseline, found and
recorded.** This stone's first proof order opened
every window in one boot, and the machine reset:
on the Stone 38 baseline, in this bench's present
build, the help window and the calculator's
opening visit together reset the machine, in
either order (help then calculator, calculator
then help). It was reproduced on a pristine
Stone 38 tree built with this toolchain — no
Stone 39 code anywhere in it — so it is a latent
fault of the baseline, not of this stone, and it
is not this stone's to fix. The proof therefore
never asks the two to stand together: the help
window's chip is proved in boots 2 and 4, the
calculator's in boot 3, and every other pairing
stands together freely. The fault is recorded
here so a later stone can take it up with its
eyes open. (The same bench note applies to
`prove-stone34.sh` and `prove-stone35.sh`: their
harnesses read the runtime's per-run guard count
(`__guard_passes`), which the current toolchain
no longer lays in the kernel — the per-loop guard
of Nifla Stone 33 keeps a depth (`__guard_depth`)
instead — so both harnesses stop at their setup
on the baseline and on this build alike, before
any system code runs. Their scenarios were not
weakened or re-aimed by this stone; the reckoning
they read is the language's to restore.)

**The building number.** This stone's growth
carried the kernel's staged segment end to
**317,462 bytes** — 10,218 bytes under the BIOS
doorman's 320 KiB claim, no stage moved.

Proven by `prove-stone39.sh`, in four boots and
seventy-six checks: at the rising the bar carries
the terminal's chip alone, standing behind; the
words 'files' and 'verse' lay their chips and move
the blue between them; one press on the files
chip raises the files window, its title bar and
its chip both turning blue; six windows opened by
their words stand chipped together, and Escape's
closing packs the chips again with the closed
window's ground restored; the calculator, opened
last over the terminal at their shared first
place, yields to one press on the terminal's
chip; and at large print the chips stand large
with the terminal's on the lower row, the bar's
name and clock whole beside it. The proofs for
Stones 38, 33, 28, 23, 29, 30, and 31 and the
no-witness proof pass with it (Stone 33's pointer
check failed once on this bench — twenty pixels
at the arrow's own resting place, a screendump
caught mid-carry — and passed on the re-run, on
this build and on the baseline alike). Bench-
proved, as every stone here; the witness that
counts is Tyler's own in UTM, still to come.


### Stone 40 — Names in the files window

The files window could list what the disk keeps
and, since Stone 27, let a note go — but a kept
thing could not be given a name, and a note could
not be copied. Both stand now, in plain words on
the window itself. With this stone the files
window's keeping work stands whole — rename,
copy, and delete together, the first line of the
ARM gate's reckoning for Files.

**Names, kept where the things are kept.** A
note's name lives in its own slot's tail — the
bytes after the words' forty-three-letter
measure, which nothing before this stone ever
wrote: the name's length at the slot's
forty-fifth byte, its letters after it, nineteen
letters at most. The picture's name lives in its
header's spare bytes the same way (the length at
the sixth byte, forty-three letters at most).
Nothing already kept moves: a slot or header laid
before this stone reads as carrying no name, and
the thing then stands under what it always stood
under — a note under its own words, the picture
under "A picture you painted". The files list
shows the name where one stands; a picked note's
words still stand at the window's foot, so what a
rename leaves alone is always in sight. A note's
name rides its slot whole through `notesave` and
`notesload`, which have always carried the slot's
sixty-four bytes entire; the picture's name is
kept by the main body in the notes block's
eleventh slot, read back at boot by the new
`picnameload` and handed to every `picsave`, so
a keeping never rubs it out — and a canvas
cleared clear through, which lets the picture's
keeping go, lets its name go with it.

**The naming way.** While a note stands picked,
"Rename" and "Copy" stand at the window's foot
in white, left of Stone 27's "Let this note go"
(which does not move); while the picture stands
picked, "Rename" stands where the letting-go
words stand for a note. A press on one opens the
naming way in the list's place: the thing being
named shown whole — a note under the name it
stands under, with "Its words:" and its words
below, so a rename's leaving-alone stands in
sight; the picture under its name, with the word
that the picture itself will not change — the
keeper types the new name into the window (the
desktop's own typing, resolved under the same
shifts and Caps Lock as the editor's draft, and
stopped at the name's measure, which the window
says plainly), and Enter keeps it. The pick
cannot move while a naming stands, as it cannot
while the letting-go asking stands; Escape puts
the naming away and leaves everything as it was.
Every change the naming makes — opening,
typing, a keeping, a refusal — repaints by
Stones 34 and 35's region road over the files
window alone (`layroadwins` over window 3, then
`paintregion`), as the feather visits already
widen that road to this window when a keeping
changes its list.

**The refusals, in plain words in the window.**
Enter on an empty name is refused: "Write the
new name first." A name that already stands on
the list is refused: "That name already stands.
Pick another name." — the reckoning is over the
name each listed thing stands under (its given
name, or its words, or the picture's plain
words), the thing being renamed excepted, so no
name is ever given twice and nothing is silently
overwritten. A copy asked of a full page is
refused with the page's own words. A refusal
changes nothing: the naming stands open with the
name as typed, and the keeper may type another
or put the naming away.

**A copy is a real second keeping.** Copying
lays the note's whole slot into the page's next
free place under the new name and writes the
page through by the same `notesave`, so the copy
stands on its own sector with the first note's
words whole: letting the first go leaves the
copy whole (proved), and changing either one —
the editor writes a note's words in its own
slot — never touches the other. A rename is
written through the same store paths, so a name
stays across a restart as the things themselves
do (proved).

**One honest limit.** The picture can be renamed
but not copied: the disk's picture store holds
one picture (sectors 80 to 83, one header), and
a copy would need a second picture's place that
does not stand there. The window offers the
picture no "Copy", and this stone does not
invent the store a bigger shape; a multi-picture
store is a stone of its own, for Tyler's word.

**The doorman's claim, raised once more.** This
stone's growth carried the kernel's staged
segment end to **336,715 bytes**, past the BIOS
doorman's 320 KiB claim — the measure Stones 26,
29, and 32 met the same way. The claim stands at
352 KiB now, and the module stages stand above
the whole of it in the last 32 KiB of low ground:
settings at 0x98000 (2 KiB), the feather at
0x98800 (6 KiB), the paint feather at 0x9A000
(8 KiB), and the calculator feather at 0x9C000,
its 16 KiB claim ending at 0xA0000 exactly, where
the firmware's reserved ground begins — as its
claim ended there in Stone 30's first laying.
No stage stands inside another's claim, as
always; the doorman's own map (in
`boot/cardnull-boot.asm`) tells it in full, and
says plainly what this laying leaves: no low
ground above it, so a system that outgrows
352 KiB must find its stages another road. The
EFI doorman, which claims its pages from the
firmware, needed no move.

Proven by `prove-stone40.sh`, in two boots and
sixty-two checks, with the disk's own bytes
checked between the boots: the naming words at
the files window's foot; the naming way opening
on the picked note with its words whole; an
empty name and a name that already stands each
refused in plain words in the window, with
nothing changed, and Escape putting the naming
away; the first note renamed to "garden notes",
standing under its new name with its words whole
at the foot; a copy laid under "garden copy",
standing picked with the first note's words
whole; the first note let go through Stone 27's
asking, and the copy still opening whole after
it; the kept picture renamed to "garden
picture"; and, after a restart, the copy and the
picture standing under their given names, the
copy's words whole in the files window and in
the editor — the stores' bytes between the boots
carrying the copy on its own sector with its
name in its slot's tail, the wiped fourth
sector, the let-go note's name nowhere left
behind, and the picture's name in its header
with the picture's own bytes untouched. The
proofs for Stones 39, 38, 33, 27, 26, 30, 24,
19, 15, 9, 22, 23, 25, 28, 29, 31, and 17 pass
with it, and the disc proof, the no-witness
proof, and the feather-start proof with them.
Two proofs fail one check each on this build
and on the pristine Stone 39 baseline alike —
Stone 20's, that the typed word "eastern" is
answered in plain words, and Stone 21's, that
the word "notes" answers the notes are kept
until the machine is turned off — so they are
not this stone's doing, and they are recorded
here as Stone 39 recorded the faults it found.
Stone 28's proof failed one check once on this
bench and passed on the re-run, on this build
and on the baseline alike — the same family as
Stone 33's known pointer flake. Bench-proved,
as every stone here; the witness that counts is
Tyler's own in UTM, still to come.

### Stone 41 — The Bible reading window, and the doorman set right

The eleventh window is a reading window: the
whole book of Jonah, in the World English
Bible's own words, kept in the system itself
(`src/bibletext.nifla`, a library in the build's
list) and read at length without any disc or
disk beyond the one the system stands on. It
opens on a contents page — "One whole book
stands here: Jonah, in the World English
Bible's own words. Pick a chapter:" — with the
four chapters listed and the picked one standing
white on blue; the arrow keys move the pick,
Enter (or the foot's "Read") opens the chapter,
and the book reads in thirty pages, its words
wrapped at thirty-six letters to the window's
measure. A reading page's foot offers "Back",
names the standing page ("Page 2 of 30"), and
offers "More"; the down and up arrows turn the
pages the same way, the last page's foot offers
"First page" back to the contents, and Escape
closes the window. Four roads lead in, as they
do to every window: the typed word `bible`, a
ninth desktop icon (a blue book with a gold
cross, the palette's gold, ninth down the left
edge), the start menu's ninth choice (the menu
stands ten choices tall now, Rest still last),
and a ninth chip on the bar. The window's
standing lives at the desk's end — its open
mark at 424, the standing page at 428, its
place at 432 and 436, the contents pick at
440 — and the desk stands 444 bytes now. (The
standing begins at 424 and not 420 for a reason
the bench taught while this stone was built:
the terminal's answers-block address at 416 is
read whole, eight bytes at a time, so its high
half at 420 must stand empty; a first laying
that wrote this window's open mark there sent
the address wild and the window would not open.)

**The doorman set right.** This stone's growth
carried the staged file to 484,880 bytes, and
with it an old fault in the BIOS doorman stood
revealed — the hardest hunt in this repository
so far, and its verdict is recorded plainly:
the fault was never in this window's source,
and never in the Nifla compilers, though a
day's bisection first blamed the bare compiler.
What was happening was a reset. The doorman's
header had long carried a claim — 352 KiB at
the last raising — for the system file's stage
at 0x40000, and the file had outgrown the claim:
its stage in truth runs to 0xB6260 and had
swallowed both the module stages at
0x98000–0xA0000 and the protected-mode stack's
top at 0x8F000, which none of the claim's
raisings (Stones 20, 26, 29, 32, 40) had ever
moved. The doorman's own pushes in its
segment-copy loop then landed inside the staged
file and overwrote the system's code, and the
staged settings and feather overwrote the
segment's tail of strings; a pointer press on
the running desktop derailed on the overwritten
code, faulted, and reset the machine — wearing
the look of the Bible window closing, since the
fresh boot's desk differs from the running one
in just the two fields a close writes. Found by
a full-image diff of the running kernel against
its file and an interrupt trace of the press
(November 20, 2026), and fixed the way this
note's map now tells: the stack's top moved to
0x3F000, below the system stage and above the
loader's own data, and the four module stages
moved to the free low ground between that data
and the stage — settings at 0x10000, the
feather at 0x10800, the paint feather at
0x12000, the calculator feather at 0x14000.
On the healed loader a press no longer resets
the machine, and the running kernel stands
byte-identical to its file across the whole
segment but for one bit the CPU itself sets in
the GDT. The EFI doorman never staged the
system on fixed ground — it reads its files
into the firmware's own buffers and lays the
segments straight from them — so this fault was
the BIOS door's alone; its own verification,
owed since this hunt, is the next thing taken
in hand after this stone.

**The build keeps the laying now.** A stage
check stands in build-iso.sh (the OS half of
the armor Nifla's Stone 43 specified): on every
build, by the files' actual sizes and never any
claim, the staged system's span must meet no
module stage and not the stack's top, every
module's stage span must meet neither the
system's span nor another stage, and every
module file must fit its stage — and a build
that breaks the law stops there and says so, in
plain words, instead of a window misbehaving on
someone's screen months later. The check was
itself proved on the bench: a settings file
grown past its stage stops the build with the
law named.

Bench-proved by prove-stone41.sh in two boots
and 109 checks — the contents page decoded line
by line, Jonah 1 read word for word against the
bundled text, the pages turned by the arrows
and by presses on the foot's own words (the
presses that reset the machine before the
doorman was set right), Jonah 4 read to the
book's last page, First page home, Escape
closing; and the icon, the close mark, and the
menu's Bible choice in the second boot — with
the disc proof and the Stones 40, 39, 38, 17,
no-witness, and feather-start proofs passing
together (Stone 17's USB boot failed once on
this bench's emulated USB road, as it has
before, and passed whole on the re-run). Two
aims of the second boot's proof were corrected
where the proof, not the system, had them
wrong: the close mark is pressed at its own
cell's center, (920, 488), and the icon's name
is read where it stands in the clear — its
first letter beside its picture, the terminal
window at the rising covering the rest, as a
window stands over the icons it covers; the
name whole is read on the opened window's own
title bar. Bench-proved, as every stone here;
the witness that counts is Tyler's own in UTM,
still to come. Committed locally only: the
ferry to GitHub is deferred to the batch at
chain end, when Stones 40–44 travel together.


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

### Stone 42 — The Shield shows itself

The feather door's guard has stood since Stone 5:
every feather that would visit is checked at the door
before it may — its card is read, its bytes are
reckoned against the card, and only a feather whose
reckoning matches is let in; one that does not reckon
true is turned away in plain words and never runs.
Until this stone the guard worked invisibly. Now it
shows itself, in a twelfth window named Shield.

The word 'shield' opens it, a tenth desktop icon
stands for it (a blue shield with a gold cross, in the
icons' own palette gold), the start menu carries it
as its tenth choice of eleven, and the bar shows its
chip when it stands open, like every window's. The
window itself is one still page in plain words: what
the guard does at the door, and two reckonings the
desk now keeps — how many feathers have been let in
since this rising, and how many turned away. The
reckoning is kept at every receiving of a feather —
the welcome feather at the rising and every visit,
opening or carried-press alike — because the door
re-reckons the card on every visit, and the Shield
counts what the door does. A disc carrying no feather
counts as neither. The desk grew twenty bytes for the
window and its reckonings (places 444 to 463; the
desk stands 464 bytes).

Two truths stand on the page, and they are the
standing design, not settings: the Shield has no
switch — it cannot be turned off, and there is no off
switch anywhere for it — and it sends nothing
anywhere: the reckonings live in the desk's own bytes
and leave the machine never (the system has no
network at all). The guard itself is unchanged by
being seen: same card, same reckoning, same refusal.

Proof: prove-stone42.sh, two boots, 43 checks. The
first boot walks every road in (the word, the icon,
the menu's choice, the bar's chip), reads the page's
twelve lines whole, watches the let-in reckoning rise
when a feather visits, and closes the window by its
mark and by Escape. The second boot carries a
tampered feather — one program byte flipped after its
card — and the Shield's page shows it turned away,
one, with none let in, and no visit standing. The
companions pass: prove-iso, prove-stone38,
prove-stone39, prove-stone40, prove-featherstart,
prove-efi, and prove-nowitness (one check on its EFI
boot flickered once under a throttled bench and passed
whole on the re-run). Stone 41's own proof now fails
its start-menu checks, as Stone 31's did at Stone 41:
the menu grew a choice and stands a row higher, and a
stone's proof speaks for its own stone's world — the
new menu is read whole in this stone's proof instead.
Bench-proved on the QEMU bench; Tyler's own witness
in UTM still stands ahead of it, with the batch.

## The witness fix (November 15, 2026)

The adopted build was delivered to Tyler's Mac and
witnessed in UTM that afternoon, and the witness found
what the bench had not. At the SeaBIOS door: a black
screen until he typed, and then the TEXT face — not the
drawn desktop — with the welcome chime unheard. At the
UEFI door: a black screen that typing could not wake at
all. The founding Stones 1–5 disc, booted in the same
setup that morning, had painted its face at once and
worked throughout. All fifteen live proofs had passed
on the witnessed build — because the proofs drive the
machine with injected keys and read its memory or its
screen afterwards, and a fault in the first paint, or
in the road before it, is invisible to that method.
The proofs' correction stands at the end of this entry;
first, what was wrong.

**The UEFI door was dead before the system was ever
reached — proven, and reproduced on the bench.** The
EFI doorman's last step, the handover
(`boot/cardnull-efi-hand.S`), walks the machine down
out of the firmware's 64-bit world: a far return
through its gate lands it in 32-bit compatibility
reach, where paging is turned off and the system is
entered. That piece ran where the firmware had laid
the doorman's own image, on its header's stated trust
that "the firmware lays its applications in the
machine's low memory, as the bench's firmware does."
A firmware is free to lay the image ABOVE the
four-billion line — and the bench's own firmware does
exactly that on the q35 machine shape (image base
about 0x140000000, the handover's gate table standing
at 0x14003000, read back from the stopped machine). In
compatibility reach an instruction pointer is
thirty-two bits wide: the high half of the handover's
address fell away at the far return, and the processor
walked off into whatever stood at the truncated
address, executing stray bytes in low memory with the
firmware's page tables still standing. The system was
never entered — no face, no chime, no answer to keys:
the witness exactly. On the bench's ordinary machine
shape the same firmware lays the image low, the
truncation is harmless, and the door had always
worked — which is why the bench never saw it.

The fix: the handover now stands as one self-carrying
piece — its code, its gate table, and the gate's
pointer inside one span, every inner address reckoned
from the instruction pointer at the run — and the
doorman copies it whole onto a low page it claims for
the purpose (0x8E000, claimed as loader code) and
calls it there. The walking down now always stands on
low ground of Cardnull's own choosing, wherever the
firmware laid the rest. Two smaller faults at the same
door were fixed beside it: the graphics mode search
stopped one short of the firmware's last mode (the
specification's MaxMode is the last mode's own number,
not the count), so a firmware whose only matching
picture stands last would have been refused a picture
that was there; and a failure after the doorman has
set its own picture now gives the firmware its own
picture back before saying its words, because the
firmware's text console keeps drawing in the mode that
stood when the doorman arrived — words said into the
doorman's mode could land on a screen nobody is shown.

**The BIOS door: the grant walk was hardened where it
was genuinely weak.** The bench could not make this
door refuse on any firmware it has: SeaBIOS on both
machine shapes and VMware's picture firmware grant
the asked-for mode with the walk as it stood, and the
one firmware that refuses (the Cirrus one) honestly
offers no 1024x768x32 mode at all — measured mode by
mode with a diagnostic doorman that recorded its own
decisions — so the text fallback there is correct, and
still stands. But the walk carried real hazards of
exactly the witnessed shape, and they are fixed:
both VESA information blocks are wiped before each
asking (the grant was once read out of a block never
cleared, so a mode's framebuffer address or pitch
could be inherited from the mode asked before it);
the controller is asked with the "VBE2" mark standing
in its block, the standard's own way of asking for the
full answer; the asked depth is read from the system's
header instead of assumed; a mode whose block carries
no framebuffer address is refused as no grant and the
walk goes on; the pitch falls back to the block's
linear scan-line field, then to the shape's own
reckoning, when the plain field stands at nothing; a
set is believed only when the firmware, asked which
mode now stands, names the chosen one; and the walk
is bounded, so a broken mode list cannot hang the
door. The system itself now refuses a hollow grant
too: a picture whose address is nothing at all no
longer raises the face of light.

Two parts of the witness the bench could not find in
the machine, and they are recorded as such. The text
face's wait for a keypress: on every firmware the
bench has, the machine paints its face — either face —
before any key is pressed (the new proof below watches
it happen with empty hands), and the kernel's road to
the first paint holds no wait a key could release;
the wait lives in how the emulator's window presented
the frame, not in what the machine drew. The welcome
panel's clipped lines: the panel's drawing — its
place, its size, its very words — is the founding
build's own, unchanged since the morning disc that
showed them whole; the clipping is of a piece with
the wait, a matter of the presented frame, not of the
drawing. And the chime's silence at the BIOS door
stands under Stone 18's own caveat: an emulator may
simply not route the personal computer's speaker. (At
the UEFI door the silence needs no caveat: the
machine never rose, so nothing could sound.)

**The proofs changed, so this class cannot hide
again.** `prove-nowitness.sh` joins the standing set:
five boots of the shipped images — the disc at the
BIOS door on both machine shapes, the disc at the EFI
door on both, and the stick — sending NO key and NO
mouse movement at all, only watching the screen until
the drawn desktop stands on it. Before the fix, its
fourth boot (the EFI door on q35) stayed pure black,
the witness reproduced; now all five paint. The full
regression stands on the fixed build: the fifteen
live proofs pass, and the new no-input proof with
them.

## The feather paint fix (November 16, 2026)

The same afternoon's witness carried a second fault,
in the feather's visit on the face of light: the
feather window opened and the visit stood, but its
writing was garbled — letters dropped in a steady
rhythm and the green panel banded — while every word
the system drew itself on the same screen stood
clean, and the door's own line below the window
("The feather visited, and has gone home again.")
read whole. Tyler read "A fetheris vsitig" for
"A feather is visiting" and "I wa cheked irst
andI amwhol" for "I was checked first, and I am
whole."

**The fault was in the showing, not the visit —
proven, and reproduced on the bench letter for
letter.** On the face of light a feather paints a
block of text cells in the host's keeping, and the
host shows those cells as light (Stone 9). The
showing (onefeather, in the main body) laid each
cell at the place the layout reckonings give its
text-face row and column: laycol squeezes the text
face's eighty columns onto this face's sixty-four,
so every fifth pair of neighboring cells landed on
the SAME face cell and the later painting overwrote
the earlier — the letters at the squeezed places
simply never stood (the 'a' of "feather", the 's'
of "was", the 'f' of "first"); layrow stretches
twenty-five rows over forty-eight, so the panel's
rows landed two face rows apart with the window's
black ground showing between them — the green
bands. Decoded from a bench screendump with the
system's own letter shapes, the pre-fix painting
reads exactly as Tyler read it, and the reckoning
alone, run on paper, gives the same three garbled
lines. The system's own words were never garbled:
they are drawn in the face's own grid to begin
with, and only this one showing ever scaled. The
text face was never garbled either: there the
feather paints the screen's own memory one cell
for one cell.

The fix: the feather's cells are now CARRIED, not
scaled — each stands in the face's own grid exactly
one cell from its neighbor, the panel's first cell
at the feather window's second column and third
row, counted on one for one from there. The window
itself is sized to hold them: fifty-four cells
wide, centered, nine high, its place reckoned once
(fwleft, fwtop, fwwide, fwhigh in the main body)
and taken from that one reckoning by both the
painter and the pointer's pressing, so the two can
never disagree about where the window stands.

**The proofs changed, so this class cannot hide
again.** The standing pixel proofs counted green
and white in bands — and garbled letters carry the
same colors as whole ones, which is why this
shipped. `prove-featherpaint.sh` joins the standing
set: it boots the shipped disc, receives the
feather, and DECODES the painted window against the
system's own letter shapes — the feather's three
lines must read exactly as written, the panel must
stand solid with no unpainted band, and the
system's line below must read whole. On the pre-fix
build it fails five checks; on the fixed build it
passes, and the full standing regression passes
with it (the founding Stones 1 and 2 proofs, which
describe the pre-face screen, fail on the fixed
build exactly as they failed before it — their
staleness, unchanged).

## The pointer trail fix (November 16, 2026)

The same witness carried a third fault: dragging the
pointer across the pixel desktop left DOTTED PIXEL
TRAILS — pixels under the pointer's path were not
restored, and dotted remnants stood on the desktop
where the arrow had passed. Kernel-drawn static
screens were clean; the corruption appeared only
after pointer MOVEMENT, which is why the bench
proofs, which had never compared the desktop after
movement, let it ship.

**The fault was in the save's measure, proven and
reproduced on the bench.** The pointer keeps the
patch of screen under its arrow in a save block and
lays it back when the arrow moves on (Stone 13).
The arrow's black shape stands fourteen rows tall
at y + 2 to y + 15 within its patch, and its white
edge is laid one pixel around the shape — so the
edge's bottom pass paints the shape's last row
again at y + 16, one row BELOW the sixteen-by-
sixteen square the save kept. That row was drawn
but never saved and never laid back: every place
the arrow had stood kept exactly the five white
pixels of its last row (at x + 2, x + 3, x + 4,
x + 8, x + 9). Reproduced on the bench before the
fix: after the arrow moved away, the sixteen kept
rows stood whole — not one stray pixel — and those
five pixels at y + 16 stood white on the black
ground, at the first stop and at every stop after.
The restore's timing and place were always right;
the save was simply one row too short for the
arrow it kept.

The fix: the save and the laying back now cover
the arrow's whole footprint — sixteen pixels wide
and SEVENTEEN tall — the save block is grown to
hold it (16 × 17 × 4 = 1088 bytes), and the
pointer's place is kept seventeen rows from the
screen's bottom edge, so the whole patch always
stands on the screen. The arrow itself is drawn
exactly as before, its point at the same place.

**The proofs changed, so this class cannot hide
again.** Stone 13's proof moved the arrow and
checked the square it left — sixteen rows of it —
and passed, because the trail stands in the
seventeenth row it never looked at.
`prove-pointertrail.sh` joins the standing set: it
boots the shipped disc, takes a reference picture
of the desktop, drags the pointer through wide
moves and a small-step drag across different
grounds and home again, and requires the desktop
afterwards to agree with the reference at EVERY
pixel below the top bar (whose clock honestly
advances), with the old trail row at every stop
named and checked on its own. On the pre-fix build
it fails with 55 differing pixels — 25 of them the
five-pixel remnants at the five wide stops, the
rest along the drag's stands; on the fixed build
the two pictures agree at every pixel, and the
full standing regression passes with it (the
founding Stones 1 and 2 proofs fail on the fixed
build exactly as they failed before it — their
staleness, unchanged).

## The feather start fix (November 16, 2026)

Booting the delivered disc of that day, Tyler
witnessed a plainer fault, in his own words:
"feather still say feath by the way when the
operating system starts." When the operating
system starts, the feather window's title read
"Feath" — the word "Feather" losing its last two
letters, "er", in the first view a person meets:
at the desktop's rising both windows stand open,
the feather's behind the welcome's, its title bar
in plain sight before any word is typed.

**This is a different defect from the feather
paint fix above, and the bench proved it so.** The
paint fix was in the showing of the feather's own
cells — cells scaled from the text grid onto the
face of light, letters overwritten inside the
visit's panel. This fault is in the system's own
chrome, in a different routine entirely: a window's
title is drawn by naming a span — where the text
begins and how many letters of it stand — and the
feather window's painter (`onefeather`, in the
main body) named a span of **five** letters for
"Feather", the Files window's measure, where
"Welcome" names seven, "Settings" eight, and
"Paint" five for its five. `pixtext` draws exactly
the span it is named, no more: five letters stood,
and the last two were never drawn at all — not
clipped by the window's edge (the window is
fifty-four cells wide, the title seven), not
overwritten by a later painting, and not scaled.
Every other place the word stands at startup was
read on the same boot and stood whole: the
window's own body ("No feather has visited yet.")
and the invitation's "feather" are drawn by
`pixline`, which names its span from the text's
own length, and they never lost a letter. An audit
of every title span in the main body found this
one alone short of its word.

Reproduced on the bench before the fix, from the
startup path exactly as a person meets it: the
shipped disc booted with **no input at all**, and
the startup pixels decoded against the system's
own letter shapes read the title as `'Feath  '` —
five letters and two blank cells — while the body
and the invitation read whole on the same screen.

The fix is the span itself: `onefeather` now names
all seven letters of "Feather", with the reason
written beside it in the source. Nothing else
changed — no geometry, no paint order, no other
window's title.

**The proofs changed, so this class cannot hide
again.** The feather-paint proof types `feather`
first and decodes the visit; the no-input witness
proof watches the startup face but counts colors
in bands, and five whole letters carry the same
colors as seven. `prove-featherstart.sh` joins the
standing set: it boots the shipped disc, sends no
key and moves no mouse, and DECODES every place
the word "feather" stands in the startup view —
the feather window's title, its body's sentence
before any visit, and the word in the invitation
line. On the pre-fix build (a pristine worktree of
Stone 25) it fails one check, reading `'Feath  '`;
on the fixed build it passes all four, and the
neighboring proofs pass with it — the feather-paint
proof (8 of 8), the no-input witness proof (five
boots), the ISO proof, and Stones 14, 23, and 24.

### Stone 43 — The USB stick in the running system

Until this stone a USB stick could only be a door:
the system booted from one (Stone 17) and never spoke
to it again. Now a mass-storage stick standing on the
xHCI bus is raised by the running system itself, and
its sectors are read and written while the system
runs — a new library, usbstick.nifla, carrying a
bulk-only-transport driver on the controller the
keyboard road set walking, with the SCSI words the
carriage speaks (test-unit-ready, read-capacity,
read, write, synchronize-cache), one sector at a
time.

The stick can carry the keeping. Its library holds a
twin of the keeping's whole layout — the settings
card at sector 8, the notes page at sectors 64 and
after, the kept picture at sectors 80 and after, in
diskkeep.nifla's very shapes — and the choice of
which disk keeps is made once, at the rising: a
fitted hard disk keeps its place, as it always has,
and the stick keeps when no hard disk stands fitted.
Every keeping call in the main body goes through a
row of wrappers that hand the call to the rising's
keeping disk, so no call site knows which disk it
speaks to. The word 'usb' reports the stick beside
the keyboards ("A USB stick is here. It holds 16384
sectors." for the bench's stick), and when the stick
is the disk offered, the rising's offer names it:
"A USB stick is here. Type setup to let it remember
your choices." Behind the setup gate's yes the stick
is carded and cleared exactly as a hard disk is, and
notes and the picture live on it across reboots.

The stone exposed three faults that were already in
the house, and fixed them where they stood; each is
told in its code where it lives.

First, a second device on the xHCI bus broke the
first road's waking. The control ring is shared by
every waking, and the controller reads ahead on a
ring while the reckoning bit matches — so a former
device's leavings, still wearing the first cycle,
were carried out as the new device's own askings,
and the new device's true askings, laid behind the
reading, were never heard. With a stick woken before
the keyboard, the keyboard's waking was answered by
the stick's leftover askings and the keyboard never
woke; a lone device was never harmed, its ring being
clean from the making. The addressing now scrubs the
ring clean and stands the laying hand at its head
before each device is addressed on it (xlayaddress,
and the stick road's ulayaddress alike), so a fresh
chain always meets a dead reckoning after it.

Second, a device the keyboard walk woke to ask its
kind and set aside stood still addressed, and
refused a second addressing outright — the keeping
road's raising of the stick failed at its address
command for exactly that reason. The walk now sets
down every device it does not keep (the Disable Slot
command), giving its claim back, and the keeping
road does the same for a candidate it cannot keep.

Third, the keeping road's waits scan the shared
event ring, and a keyboard completion met there was
passed by — and the poll re-arms the keyboard's
interrupt door only when it sees that completion
itself, so one passed by left the keyboard silent
for good: after the setup gate (whose sixty-six
writings to the stick scan the ring many times) no
word typed was ever answered. A waiter that meets
the keyboard's completion now keeps the keyboard's
service on its behalf — the keys read into the
queue, the door armed again — exactly as the poll
would (xkbkeep, called from the command wait and
the stick's transfer wait).

And the stone outgrew the doorman's stage. The
system's segment, staged at 0x40000, crossed
0xA0000 — where the firmware's reserved ground
begins — and its tail bytes were lost into that
ground: the desktop wore the loss as small
wrongnesses (an icon's name read blank, a feather's
visit failing) while every direct-loaded proof stood
green, the loss living only in the doorman's road.
The stage could not be raised, the firmware's disc
service addressing no higher than its first
megabyte, so it came down the hill to 0x20000, the
segment ending at 0x839D7 with the reserved ground
untouched above it, and the protected-mode stack
tucked from 0x3F000 into the free ground at 0x1F000
between the module stages and the stage. The build
check (build-iso.sh) now measures the segment's own
end from the file's program headers and holds it
below 0xA0000, loudly. The doorman's own note tells
the whole laying, as it always has.

Proof: prove-stone43.sh, four boots, 36 checks. A
blank stick and no hard disk: the stick is offered,
'usb' reports it, the keyboard on the same bus
stands ready, the gate's yes gives the stick the
keeping, and two notes are kept on it — the stick
image's own bytes then prove the card and the notes
stand on the stick, in the disk's layout. The same
stick booted again: the notes are read back, a third
is kept, and the bytes prove the page grew. No
stick: nothing is offered and 'usb' names none. A
blank stick and a blank hard disk together: the hard
disk keeps its place, is offered and carded, and the
stick's image stands byte-identical after, never
written. The companions pass: prove-iso,
prove-stone6, prove-stone8, prove-stone15,
prove-stone32, prove-stone38, prove-stone39,
prove-stone40, prove-stone42, prove-efi,
prove-nowitness, and prove-featherstart;
prove-stone41 fails only the two start-menu checks
that went stale at Stone 42, as it did there.
prove-stone17 (the USB-disc boot) fails on this
bench today on the Stone 42 tree as on this one —
its emulated USB boot has always been intermittent
here — and no real stick has booted the system yet:
that witness, like every witness, is Tyler's in UTM
and on his own hardware.

### Stone 44 — A second screen

A machine may carry more than one display adapter,
and until this stone the system never looked: the
doorman grants one screen, and one screen is all it
ever raised. Now, at the rising, the running system
walks the PCI bus for a second display adapter and,
when one stands, raises a still companion page on
it — a new library, twoscreen.nifla. The page is
not a second desktop and not a mirror: no window
stands on it and nothing moves there but the
clock's minute. On the desktop's own deep glass
ground, in its pale ink and the system's own
letters, it carries the name Cardnull, the words
"The second screen", the day and the date in plain
words, the clock's face, and the Psalm 127 lines —
"Unless Yahweh builds the house, they labor in vain
who build it." The main loop paints it again when
the minute turns, beside the bar's own drawing. The
rising's answers name it in plain words — "A second
screen is here." — and when no second adapter
stands, nothing anywhere changes: the raising
answers no, and the page is never painted.

Three findings of the bench are written into the
raising, each learned by watching the machine
refuse a simpler shape. First, the second adapter
commonly stands under the PCI class "display,
other", not "VGA" — the firmware gives the VGA name
to the first adapter alone — so the scan takes any
display-class device whose framebuffer is not the
granted one, and lets the adapter's own extension
ID word be the true test of the candidate. Second,
the raising speaks the Bochs video extension
through the adapter's MMIO ground (its second
memory region, the registers laid flat at 0x500):
the screen put down, the shape laid — 1024 by 768
at 32 bits, the granted screen's own measure — and
the screen raised with its framebuffer standing.
Third, the extension's mode alone raises no
picture: the second adapter's VGA heart stands in
text mode from its waking, no firmware ever having
set it, and its display path goes on following the
text registers until the attribute register's
graphics bit is flipped through the register window
in the same MMIO ground (at 0x400) — the bench
proved this by contrast, the granted adapter
following an extension mode-set at once while the
second head stood at its power-on size until the
bit was set. Every word the raising sets is read
back before the standing is claimed: a screen that
did not take its mode, or its graphics bit, is no
screen, and the raising answers honestly.

The bench proof (prove-stone44.sh, sixteen checks)
boots the shipped disc twice. With a second adapter
fitted (the bench's secondary VGA) and the clock
pinned to a known morning: the main desktop stands
untouched, and the second head — read through the
monitor's screendump for that device, by a helper
this stone adds to tools/pixels.py — stands at
1024 by 768 on the glass ground, every line of the
page decoded against the system's own letter
shapes, the clock's face among them; and when the
minute turns the page stands painted again with a
new minute. With no second adapter: the desktop
stands exactly as before, and there is no second
head to read. The companions pass: prove-iso,
prove-stone38, prove-stone39, prove-stone40,
prove-stone42, prove-stone43, prove-efi,
prove-nowitness, and prove-featherstart (three of
them — the Shield's, the EFI door's, and
nowitness — failed first-frame reads in the first
loaded batch and passed whole on a quiet re-run,
the bench's known timing flake); prove-stone41
fails only the two start-menu checks that went
stale at Stone 42, as it has since that stone. All
of this is bench-proved only: no real machine's
second monitor has carried the page yet, and that
witness, like every witness, is Tyler's in UTM and
on his own hardware.

### Stone 45 — The repaint roads healed

Tyler witnessed the Stone 44 build in UTM the day
it landed (November 24, 2026) and found two faults
with his own eyes: dragging the welcome window left
its body a big flat gray, with garbled streak lines
along the rows where its words should stand, and
while a window moved, all the windows flickered.
The bench's diagnosis (kept with the day's scratch)
pinned both to the repaint roads, and this stone
heals them there.

The face paints straight onto the screen — there is
no back buffer and no clipping anywhere in it — and
every window's painter first lays its frame's full
undercoat, a flat dark gray (85, 85, 85), and only
then paints the body over it: the welcome's own
body is light (170, 170, 170) with black words. A
region repaint (paintregion, the road Stones 34 and
35 laid) washed its road, re-laid every icon the
road touched — whole, all three rows and the name
beside the picture — and repainted the windows
whose places touched the road. But a pass writes
farther than its road: an icon's whole span can
stand partly outside the road, over a window that
does not touch the road at all; and a repainted
window is painted whole, frame and body and the
shadow's reach past its right and foot, over
whatever stands there — including a window in front
of it whose own place never touched the road. Such
a window kept the writing standing on it with no
body over it: the frame's gray undercoat where its
words belonged, an icon's name stamped across its
body — state right, glass wrong, healed only when
some later whole repaint happened by. The set is
now closed before anything is washed (the
body-always-lands closure): a window whose place
meets a re-laid icon's whole span, or the
place-and-shadow of a window already in the set,
joins the set, and the closing repeats until no
window is added, since a joined window's own
painting writes just as far. Every window a pass
writes on is repainted in that same pass, after the
icons, in the standing order.

The flicker was the drag road itself: at Stone 34
a drag step repainted, whole, every window touching
the union of the ground left and the ground taken —
so as a window crossed the desktop, its bystanders
were washed and redrawn at every step. A step now
paints only what the step itself disturbs
(dragstep): the ground the window is leaving is
washed bare and its icons laid again, and the
window — forward since the hold was taken — is
painted at its new place. The windows a step
uncovers stand washed for the drag's length; the
drag's following gathers the whole road the window
travelled, place by place, and letting the button
go lays one region repaint over that whole road,
which makes the glass whole again, once. The step's
errand travels in the desk at 464 to 475 (the desk
stands 476 bytes now), the way the region repaint's
road travels at 384 — the call's three blocks fill
the machine's registers already.

The stone also restores the drag's own proof.
prove-stone34 had stood broken since the compiler
changed under it: it read the runtime's loop-pass
counter from a global cell, __guard_passes, that
the compiler no longer lays in the kernel (each
loop's guard stands in the loop's own frame now),
so it died before booting and the drag road had no
working guard. The restored proof checks directly
what the counter stood for, and more strongly: the
populated desktop below the dragged welcome window
is hashed after EVERY step of its drag, button
still held, and must stand pixel for pixel
untouched at every instant; and after the drop the
dragged window's own wholeness is proved — a census
of its body's interior finds no frame-gray standing
in it, and all five of its lines decode. Its drags
are taken the way this bench demands: the pointer
paced in small steps, each take-hold confirmed by
the pressed window's title bar turning the front
window's blue before any step is sent, and frames
left to settle between inputs — the bench's mouse
loses packets under repaint load, and a press it
lost is simply tried again. A screendump in the
restored harness is read only after a breath and
believed only when its measure is whole: the first
restored runs read frames a step behind the glass
under this bench's load, took repaints still in
flight for settled desktops, and sent drag steps
into them to be lost. The proof passed whole on
this stone's code — twenty-one checks, the
crossings and the returns of its second drag among
them.

The companion proofs stand: the disc's own
(prove-iso, fourteen checks), Stones 38, 39, 40,
43, and 44, the EFI door, and the feather start all
pass on this stone's tree. Stone 41's proof fails
its two start-menu checks and Stone 42's fails its
eight — the stale-menu reckoning Stone 42's growth
left in Stone 41's proof, met again: those proofs
read the menu at the rows Stone 41's menu stood on,
and Stone 46's growth (the next stone) moves the
reckoning again and mends both proofs there, as
recorded with that stone. The no-witness proof
failed its welcome-panel checks on a single first
frame read mid-paint — its letter checks passed in
the same frame — the first-frame timing flake this
bench has always had; nothing at the rising changed
at this stone.

The bench limit, stated plainly, because it was
measured and not guessed: after the proof's whole
pass, this bench's emulated mouse would no longer
carry a drag at all — a take-hold confirmed by the
title bar's blue, six paced steps sent, and the
window unmoved — and the same harness on the
unmodified Stone 44 tree showed the same standstill,
so the limit is the bench's, not this stone's
roads. Tyler's UTM drags windows on the living
machine (it was a moving drag that showed him the
faults), where the mouse is hardware-paced and
faithful. So the healing stands proved on the roads
and their ordering and on the one whole pass the
bench gave; the witness that the flicker and the
gray body are gone from the living machine is
Tyler's in UTM, still to come.

Addendum (later the same day, on the Stone 46
tree, the bench quiet): the no-witness proof
passes whole — forty checks — and with it the
full companion sweep of the stone before (the
disc's own proof and Stones 38, 39, 40, 43, and
44, the EFI door, and the feather start) passes
on the final tree. The reading above stands
confirmed: the no-witness failures at this stone
were the first-frame timing flake, nothing at the
rising.

### Stone 46 — All the programs in the start menu

At the same witness Tyler gave the word: all the
programs belong in the start menu. The menu named
eleven choices, and two of the desktop's programs
were missing from it — Paint and Terminal could be
opened from their icons or their typed words, but
not from the menu. The menu names thirteen now, and
its choices stand in the desktop icons' own order:
Welcome and Feather first, as they have always
stood, then Files, Editor, Paint, Calculator,
Verse, Help, Settings, Terminal, Bible, and Shield,
with Rest last, as it has always stood. Paint
stands fifth, after Editor, and Terminal tenth,
after Settings — where each stands among its
neighbors on the desktop itself. The menu's
reckoning grew with it: thirteen rows, its foot
still on the bar's top edge, its top two rows
higher; the painter and the pointer read the one
reckoning, as the menu's discipline has always
required, and the two new choices open their
windows exactly as their typed words do — Paint
with its feather's opening visit standing in it,
Terminal brought forward — and the moved choices,
Bible eleventh among them, land where they always
landed.

The stone's proof (prove-stone46) opens the menu,
decodes all thirteen choices at their rows, and
presses the new and the moved: Paint, Terminal,
Bible on its contents page, and Rest, whose panel
Stay then puts away — twenty-two checks, passing
whole. Its presses are taken the way this bench
demands, and the taking is recorded in the proof
itself: the road to each press point is walked in
small steps, a lost press is simply taken again,
and Rest's row — the menu's lowest, eight pixels
from the bar — is pressed first among the choices,
while the pointer's reckoning is freshest; on this
bench the reckoning drifts a little with every move
it is given, and the proof's first runs, which
pressed Rest last, watched that drift spend itself
on the lowest row.

The growth stales the menu reckonings two older
proofs carry, and both are mended here, as the
discipline requires — no check weakened, the same
words decoded at their true rows: Stone 41's proof
reads the thirteen choices from row 33, Bible on
row 43, its press on the Bible choice at that row;
Stone 42's proof the same thirteen, Shield standing
twelfth — on row 44, the very row it stood on
before, the menu having risen as far as the choice
moved down. Both proofs pass whole again on this
stone's tree (Stone 41's, one hundred twelve
checks; Stone 42's, forty-five). The companions of
the stone before stand as recorded there.

### Stone 47 — The drag heal

Tyler witnessed Stones 45 and 46 in UTM that same
evening: the start menu had grown as Stone 46
promised, but windows still glitched when clicked
and moved — the whole window GUI breaking until
the machine was reset — and Paint flickered as it
was painted in. The second bench diagnosis (kept
with the work, DIAGNOSIS2.md) found why Stone 45's
healing had not held: the damage of a drag
accumulates and never heals, because four roads
write outside the reckoning Stone 45 closed. The
terminal's painter keeps its answers and typing
rows at the place the window first stood, so a
dragged terminal spills its answers below its own
foot forever. The desktop's ground texts — the
invitation lines, and the feather-visit receipt
the pixel face stamped on the ground — have no
repaint owner at all, so a wash leaves them rubbed
out for the rest of the sitting. An icon's label
is painted on whatever paper the last pass left
standing, so labels flip black to blue with the
desktop's repaint history. And every press carried
inside Paint or the Calculator was answered with a
whole road wash and region repaint — the flicker
itself, repainting bystanders to answer a stroke.

This stone heals the four roads, in six parts. The
window mover's terminal branch now lays the
console's rows from the window's new top, reckoned
the way the rising lays them, so the answers and
the typing follow their window. A drag's drop pays
one whole repaint of every window instead of the
road-limited region pass, so whatever a drag's
steps left standing is made whole at the drop; the
per-step diet Stone 45 built is untouched, so no
flicker returns during the drag itself. The ground
gains an owner: the invitation's two lines are laid
by one helper the rising and every repaint share,
the whole-face repaint lays them before the icons,
and a region pass reckons before its wash whether
its road touches a line — a touched line joins the
pass's closure like an icon's span, and is laid
again on the washed ground before the windows
whose bodies must land over it. The feather-visit
receipt leaves the ground and is kept where every
other answer is kept, in the terminal's own
keeping. An icon now sets its own paper before it
paints its label's name, so a label's ground no
longer depends on what was painted before it. And
a press visit inside Paint or the Calculator
repaints that window directly — no road wash, no
bystander repainted — while the Files list a
stroke owes (a picture newly kept) is paid once,
when the button is let go, instead of at every
packet of the stroke.

The stone's proof (prove-stone47) stands in five
boots: a terminal-drag census, the labels' paper,
the ground's invitation, the press band, and the
Files owing. What the bench could carry, it
carried whole. The labels keep their paper
(six of seven checks; the seventh is the drag
itself). The invitation stands whole at the rising
and after a crossing region road laid the lines
its road touched (boot 3). A held Paint stroke
writes nothing outside its own window at any of
five steps, its title standing throughout, and the
band around the desktop stands unchanged after it;
the Calculator's press likewise writes nothing
outside its window (boot 4, eighteen of twenty —
the two it could not show are the sum's own line
and a title read taken while this slow bench was
still repainting). The feather-visit receipt is
read where it is now kept, in the terminal, by the
mended prove-featherpaint, which passes whole, and
prove-stone5 passes as it stood — the text face
keeps its receipt at its own row, as it always
did. The companions stand whole at their recorded
counts: the disc (14), Stone 38 (19), Stone 39
(77), Stone 40 (64), Stone 41 (112), Stone 42 (45),
Stone 43 (36), Stone 44 (16), Stone 46 (22), the
no-witness proof (40), and the feather's start
(4). The EFI door's proof read one icon's name
empty on its first run and passed whole on its
second (8) — the first-frame timing this bench is
known for, both runs recorded.

What the bench could not carry is the drags
themselves, and it is recorded plainly, as Stone
45's limit was. On the day of this stone the
bench's emulated mouse would not carry a held drag
on any tree: the diagnosis's own drag sequence,
run on the unmodified Stone 46 tree, ends in the
same blackened, garbled frame it ends in here, and
prove-stone34 — the house's own drag proof — fails
its drags the same way on this tree (ten checks,
every one of them drag carriage or a reading
downstream of a drag that never landed; the
crossed terminal still decodes whole when Tab
brings it forward again).
So the terminal-drag census (boot 1) and the Files
owing's payment at the stroke's end (boot 5) stand
unproven on this bench: their drags never landed,
and boot 5's mid-stroke check, passing, is vacuous
without them — no picture was ever painted for the
list to owe. The roads themselves are as the
diagnosis scoped them and the source shows them;
whether the drag is healed is not the bench's to
say. Tyler's witness in UTM decides, as it decided
for the stone before.

### Stone 48 — The Picture Window

The kept picture — the one Paint keeps to the
disk, standing in the Files window's list since
Stone 26 — could be opened only back inside Paint
itself, at the paint window's own measure. This
stone gives it a window of its own, the desktop's
thirteenth, where it stands open big: every cell
of the kept canvas sixteen pixels wide and
thirty-two tall, the whole canvas 768 by 224
pixels, drawn cell by cell from the picture
block's own keeping — the real kept data, read
through the block's address laid in the desk —
never a placeholder. Its place is reckoned the
way every window's is: fifty cells wide when the
grid leaves room, two short of the grid's whole
width at the large print, sixteen high, first
standing centered at the face's middle height;
painter and pointer read the same place cells, at
both word sizes, as every window's do. The desk
grew for it, 476 to 492: its standing at 476, the
kept picture block's address at 480, its place at
484 and 488, all entered in the desk ledger in
pixface.nifla in the established style. The
forward reckoning grew honestly with it — 13 is
the picture window — through the whole-face
repaint's passes, the region road's closure, the
window mover (which knows its place pair, so the
title bar drags it by Stone 47's healed roads, no
drag arithmetic changed), the Tab cycle, the
Escape closing, the close mark, and the bar's
chips, where it stands eleventh in the icons'
order. No state reckoning changed beyond the new
window's own standing; Stone 47's six parts and
the Shield's truths stand untouched.

It opens three ways. In the Files window, while
the picture stands picked, the foot carries a new
word, "Look at it", beside "Rename", and the
foot's line now names both doors plainly: "Enter
opens it in Paint. Look at it sees it big." Stone
26's own door stands exactly as it stood — a
press on the picture's row, or Enter while it is
picked, opens it in Paint, and Stone 26's proofs
stand on that — so the new window's Files door is
the foot word, the house's own pattern for a
second way into a picked thing ("Let this note
go", "Rename", "Copy" are its kin). The typed
word 'picture' opens it too, and the start menu
gained its choice in the icons' order discipline
of Stone 46: fourteen choices now, Picture
thirteenth after Shield and Rest last, the menu
risen one row higher to stand them (its top row
is 32 now). Chosen with no picture kept, the
window still opens, and its body says so plainly:
"No picture stands kept yet. Paint one in the
paint window and keep it, and it will stand here,
big, to look at." It has no desktop icon, and the
reason is plain: the icon column already stands
full — on the short grid of the large print a
eleventh icon's box would reach past the bar, the
tenth already reaching the bar's top row. Its
doors are the Files word, the menu, the typed
word, and its chip.

One fault of this stone's own making is recorded
because the bench found it: the painter's first
cell reader took the block's address from the
desk as a whole eight-byte word, whose upper half
is the window's own left place standing in the
next cell — a wild address, from which the cells
read as whatever lay there, and the window would
not stand. The desk's cells are four-byte words
and are written so; the reader now reads its
address as one, and the picture stands exact.
(The paint window's older reader of the same
shape stands as it always stood: the cell after
its address has only ever held nothing, and its
readings have been true on every stone.)

The stone's proof (prove-stone48) stands in three
boots. Boot 1 keeps a picture the bench's way —
Paint draws a Red cell and a Blue cell, as Stone
26's proof draws them — and the Files window
lists it; the down arrow picks it, the foot's new
word and its line decode, a press on "Look at it"
opens the picture window forward, and the picture
stands in it in its big measure: the Red cell's
block whole to its corner, the Blue cell's block,
an untouched cell on the canvas ground (17 checks,
whole). Boot 2, with no disk fitted, opens the
window by its word and decodes the empty window's
three plain lines exactly; the menu's fourteen
choices all decode, Picture thirteenth and Rest
last; a press on the Picture choice opens the
window; and with the Files window forward, a press
on the picture window's chip raises it, its bar
blue again (26 checks, whole). Boot 3 boots again
on boot 1's disk, and the word 'picture' shows the
kept picture from the disk's keeping alone — the
Red and Blue cells standing in the window with no
painting done this sitting — and a press on the
close mark at the window's standing place closes
it (5 of 6 checks). The sixth is the drag: the
window was to be dragged three cells right and
two rows up and its picture read whole at the new
place, and the bench's emulated mouse would not
carry the held drag, exactly as Stones 45 and 47
recorded of this bench — the window stood at its
first place through every taking. Its place pair
stands in the window mover as the source shows;
whether the drag carries it is not the bench's to
say, and Tyler's witness in UTM decides, as it
decided for the stones before.

The companions stand whole at their counts: the
disc (14), the EFI door (8), Stone 26 (27), Stone
38 (19), Stone 39 (77), Stone 40 (64), Stone 41
(113), Stone 42 (46), Stone 43 (36), Stone 44
(16), Stone 46 (23), the no-witness proof (40),
the feather's start (4), and the feather's paint
(9). Four companion proofs were mended where this
stone's intended changes staled them, no check
weakened: Stone 26's second boot reads the foot's
new line in the old line's place; Stone 41's
second boot, Stone 42's first, and Stone 46's
first read the menu as it now stands — fourteen
choices from row 32, each loop gaining the new
choice's own decode, which is why Stone 41, 42,
and 46 each count one more check than the stone
before recorded. Stone 34 and Stone 47 fail on
this tree only where they fail on any tree this
bench is given: Stone 34's drags (7 of 19 — every
failure a drag's carriage or a reading downstream
of a drag that never landed, the family Stone 47
recorded), and Stone 47's boots as its own record
leaves them — the labels keep their paper (6 of
7, the seventh the drag itself), the press band
stands at eighteen of twenty with the same two
readings its own stone recorded, and the
drag-census and Files-owing boots unproven as
they stood. Stone 47's third boot was run also on
the unmodified Stone 47 tree as a control, and
the two runs agree check for check, its two
failures the drag and a word typed into the
drag's garbled aftermath; the invitation itself
stands whole in both. Bench proof is bench proof:
nothing here is claimed as witnessed.

### Mend found by Stone 49 — Carried presses reach Paint only when Paint stands forward

Stone 49 was built and, before it was committed,
verified — and the verification found its picture
exchange corrupted: by exactly one byte in the
copying to the stick, and whole in the bringing
in, where the brought-in picture was overwritten
after it landed. Instrumented proof cleared the
exchange itself — its copies are faithful to the
picture block at their moments — and found the
fault in a road Stone 24 built: the paint
feather's carried presses. While the paint window
stood open and a visit had stood in it, any press
landing inside the window's shown region was
carried across the desk to the feather, which
laid its cell, and the keeping that follows a
visit wrote the canvas back to the disk. The road
never asked which window stood forward. Picking
the kept picture in the files window opens it in
the paint window behind (Stone 26's way), and the
files window's own presses — Stone 49's exchange
row among them — land inside the shown region's
ground; so a press meant for the files window
painted a cell through it, and the re-keeping
that followed overwrote what the exchange had
just done.

The mend is one gate, and nothing more: a press
is carried now only while the paint window stands
forward — the desk's forward reckoning (180) is 6
for the paint window. While another window stands
forward, the press is that window's alone,
exactly as if the paint window stood closed. The
road's other standings stand as they stood — the
drag's exemption, the rest panel's, the shown
region's reckoning — and nothing of Stone 47's
six parts, Stone 48's window, the Shield's
truths, or the exchange itself was touched. The
calculator feather's road (Stone 30) is of the
same shape and keeps it: it carries no keeping
that a stray press could overwrite, and no fault
was found on it; the difference is recorded here
so it stands as a decision, not an oversight.

The mend's own proof (prove-mend49) boots the
shipped disc twice, on two keeping disks laid
byte for byte the same. In the first boot a
picture is painted the bench's way — the carried
presses painting with the paint window forward,
as they must — the files window picks it with the
paint window open behind, and Stone 49's exchange
press is made at the same point of the screen;
the files window answers it alone, in plain
words: "No stick stands in this computer." The
second boot is the control: every step the same,
the press never made. The two disks' picture
keepings — the header sector and the body's three
— are then compared byte for byte, and they stand
identical: the press laid no cell and re-kept
nothing (17 checks in all; the comparison is
guarded against emptiness — the header shows a
picture truly kept, and the body holds the
painting, not the untouched ground). The feather
paint proof passes whole beside it (9 checks),
its carried visits unhindered. One bench note is
recorded honestly: under load, this bench's
harness watching — a screendump and a full-frame
count at every poll — can starve the very rise it
waits for; this proof's first runs timed out so,
at 150 seconds and at 300, while the same
scenarios run alone stood drawn in seconds. The
scenarios now let the machine rise unwatched for
a breath before the watch begins; no check was
weakened for it. Bench proof is bench proof:
nothing here is claimed as witnessed, and Tyler's
witness on the living machine decides, as it
decided for the stones before.

### Stone 49 — The Stick and Disk Exchange

What the keeping disk holds, a stick can now
carry away, and what a stick carries can be
brought home: the files window exchanges a picked
kept thing with a plugged-in stick, in both
directions, in plain words. The files window grew
one row for it — the desk 492 to 496, the new
cell (492) holding the exchange's word, the
window's reckoning of its rows fifteen become
sixteen, and its top row risen one, 31 to 30, to
stand the taller window. While a note or the
picture stands picked, the window's foot carries
two new words, "To the stick" and "From the
stick". Every road answers plainly. To the stick
refuses, in the window, when no stick stands in
the computer, when that name already stands on
the stick (Stone 40's discipline — a copy never
silently overwrites), when the stick's page
already holds its eight, when a picture already
stands on the stick, and when the copy itself
fails; and it answers "Copied to the stick." when
the thing stands copied. From the stick refuses
when no stick stands in, when the stick holds no
note of the picked name, when it holds no
picture, and when the disk would not keep what
was brought; and it answers "Brought in from the
stick." when the thing stands home. The copies
run through scratch blocks of the desk (the
stick's notes at 704, its picture at 1536), so a
source is read and never written by its own
copying; bringing in lands through the keepings
themselves — the picked note's own slot is
refreshed, the picture takes the kept picture's
place — and the roads underneath are Stone 43's
USB roads, as they stand.

One scope reading is recorded as the design
stands, Tyler's to overturn: bringing in works on
the picked thing's twin. A man picks a note on
his disk and brings in the stick's note of the
same name; the picture likewise. A note that
stands only on the stick, under a name his disk
does not hold, cannot be brought in as a new note
— there is no picked thing for it to be the twin
of. The refusal says so plainly, and the wider
road waits for his word, as other roads have.

This stone stands on the mend recorded just
above, and the order matters: the mend was
committed first, alone, and this stone landed on
the mended tree. Without it, the exchange's own
presses painted through the files window and the
re-keeping overwrote the exchange's work, as the
mend's section tells.

The stone's proof (prove-stone49) stands in four
boots and the shells' own byte reckonings, 53
checks whole. Boot 1, on a prepared disk — the
Eastern card and two notes, one of them named —
and a blank stick: the exchange row decodes while
a note stands picked, both notes are copied and
answered, a picture is painted and kept the
bench's way and copied likewise, and the refusals
stand in their plain words, the picture copied
again and the first note copied again; the
stick's own bytes then prove the copies — its
notes page holds the disk's two slots entire,
name tail and all, and the picture's three
sectors stand on the stick byte for byte the
disk's — while the disk's notes page stands byte
for byte as it was laid, the source untouched.
Boot 2 prepares the stick with a keeping of its
own — a note under the second note's name with
other words, and a picture of its own — and
brings both in: the note's words at the window's
foot are the stick's words now, the stick's
picture stands in the picture window in its big
measure at its own cell, and the first note is
refused, the stick holding no note of that name.
The disk's bytes prove what was brought in stands
kept there, and the stick's image stands
byte-identical across the whole boot — bringing
in never writes its source. Boot 3, with no stick
on the bus, hears both presses answered "No stick
stands in this computer." Boot 4, with no hard
disk and a keeper stick carrying its card and two
notes, hears both answered "The stick is this
computer's keeping."

One bench note is recorded honestly, as the
mend's section recorded its own: on the night of
the landing this bench's SeaBIOS wedged at
"Booting from DVD/CD..." again and again on the
stick-carrying boots — the guest spinning, the
handoff never made — while other boots of the
same disc rose in seconds. The proof's boots were
therefore driven through a bench driver differing
from the shipped script only in its boot's
patience: each machine was watched lightly and
relaunched when it wedged, a wedged attempt never
having run the system at all, and every scenario
and every byte reckoning that ran is the shipped
proof's own, word for word (the shipped script
itself, earlier the same evening, carried boot 1
and its byte reckonings whole before a later
boot's rise wedged). No check was weakened, and
no count above comes from the driver — they are
the proof's own checks, all of them landed.

The companions stand whole at their counts: the
disc (14), the EFI door (8 — a first run's one
blank reading of the files icon's name, gone on
the re-run, the door's known flake), Stone 26
(27), Stone 38 (19), Stone 39 (77), Stone 40
(64), Stone 41 (113), Stone 42 (46), Stone 43
(36), Stone 44 (16), Stone 46 (23), the
no-witness proof (40), the feather's start (4),
and the feather's paint (9). Stone 48 stands at
49 of its 50, the one failure its third boot's
held drag — the limit its own section recorded,
the window standing at its first place through
every taking. The rest of the failures are the
bench's and the past's, classified as they stand:
Stone 34's drag census did not complete — its
machine rose and its reckonings waited on drags
the bench's mouse would not carry, as Stone 47's
record shows it failing identically on
unmodified trees; Stone 47's six failures are its
first boot's terminal-drag census, every one
downstream of the drag that never landed, its
standing bench limit; Stone 22's two are readings
downstream of its own drag; Stone 19's two are
its Tab readings, which fail identically on a
pristine Stone 48 tree, control-proven before
this stone was built; and Stones 23, 25, and 33
still carry the nine-choice menu reckoning from
before Stone 46 grew the menu — their logs read
the grown menu's own words in the old list's
places — a small future mend stone's work, named
here so it is not lost, and not this stone's to
fix in passing.

The files window's growth staled the companions'
reckoning of its top row, and they were mended —
proofs 19, 22, 23, 25, 26, 27, 33, 38, 39, 40,
and 48 — the constant carried 31 to 30 and the
comments with it, no check weakened; two of them
(22 and 33) also widen a remnant scan by the same
row, covering more ground, not less. The mending
is recorded with its own fault, found in
verification before the landing: one companion
mend of the first building had silently dragged
the editor's place along in Stones 27 and 40; it
was restored to its true reckoning and both
proofs re-run whole. Stone 48's second boot reads
the picture chip's plate by Stone 39's reckoning
where the taller files window now covers its old
read point whole — a mechanism swapped, the check
itself unchanged, disclosed in prove-stone48's
own header. Bench proof is bench proof: nothing
here is claimed as witnessed, and no real stick
has yet carried the exchange — Tyler's witness,
on a real stick in the living machine, decides,
as it decided for the stones before.

## The EFI door verified (November 24, 2026)

The disc has carried two doors since it was first
laid: the BIOS doorman, whose stage fault Stone 41
set right, and the EFI doorman
(`boot/cardnull-efi.c` and its handover,
`boot/cardnull-efi-hand.S`), which reads its files
into the firmware's own buffers, lays the system's
segments straight from them at their recorded
addresses, lays the module row at 0x300000, and
hands over the same multiboot-shaped table the
BIOS door lays. The EFI door had never been
booted on this bench — every proof drove the BIOS
door — and Stone 41's hunt made the debt plain.

It is paid now. prove-efi.sh boots the shipped
disc under the bench's OVMF firmware (the pair
under ~/qemu-root/usr/share/OVMF, the variables
image copied throwaway so no boot writes anything
that lasts) and proves in eight checks: the
desktop rises at the EFI door; the Files icon's
name reads; the feather window stands; the word
`feather` brings the welcome feather through this
door — its module read from the disc's EFI system
partition — card-checked, painting its own panel,
its own words read on it ("I was checked first,
and I am whole."); the word `bible` opens the
Bible window on its contents page; and Escape
closes it, the feather's panel standing in the
clear again. Nothing at this door proved broken,
and nothing speculative was changed: the one
correction the check carried is a comment in the
handover that still told the stack's place as
"where the BIOS doorman sets his (0x8F000)" — the
BIOS stack moved to 0x3F000 in Stone 41, and the
EFI stack at 0x8F000 is this door's own claimed
page, which the comment now says. Bench-proved,
as every claim here; Tyler's own witness in UTM
stands for both doors alike, still to come.

## The kernel's files

The kernel is built as several files, never one big one — Tyler's
standing rule (November 15, 2026), kept from the first Cardnull OS,
whose kernel stood in twenty files. The seed kernel began the
founding morning as a single file; the same day, at Tyler's word, it
was split by duty, without changing its behavior:

- `src/cardnull.nifla` — the main body: the boot sequence, the
  first-breath lift of what the loader brought, all the system's
  state, the face, the typing line, and the loop that calls the
  libraries. The windows' painting lives here too (Stone 14:
  winframe, onewelcome, onefeather, paintwindows; Stone 19:
  onefiles and filenotetext, the files window and its drawing
  of the kept notes from their bytes; Stone 20: onesettings
  and sechoice, the settings window and its choice rows;
  Stone 21: oneeditor, the editor window and its two ways),
  reading the windows' standing from the pixel face's desk.
  The bar's window chips live here too (Stone 39: chipwin,
  chipname, chipplace, paintchips — the laying reckoned
  once, read by the painter and the pointer alike).
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
- `src/xhcikey.nifla` — ears on the modern USB road (Stone 32):
  the xHCI host and the HID boot keyboard it wakes, its whole
  estate in one desk of bytes the main body hands it at every
  asking (xhinit, xhpoll, and their helpers); its small ledger
  hands and its HID translation are the UHCI library's own,
  called as they stand.
- `src/rtclock.nifla` — the real clock (Stone 7): reading the
  machine's own CMOS clock into a block the main body hands
  it, and the calendar reckoning that turns a reading into a
  date in plain words (rtcread, rtcbaseof, datetext, and their
  helpers).
- `src/diskkeep.nifla` — what the system remembers on a hard
  disk (Stone 8): waking the drive, the settings card and its
  reading, the write-back, and the setup clearing
  (diskhere, savedoffset, remember, disksetup). Stone 20
  grows the card by its chime byte (savedchime, rememberall). The notes
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
  pixrestore, pixarrow). The bar's ground under the
  window chips is laid here too (Stone 39:
  pixchipground — pixbar's own bands over the chips'
  two spans, and nothing else on the bar).
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
- `src/rest.nifla` — the resting (Stone 25): the ACPI
  power doors tried in turn (the bench's own first,
  measured from its ACPI tables: the word 0x2000 to
  the door at 0x0604), the reset doors (the keyboard
  controller's reset word, then the reset control door
  at 0xCF9), and the final halt the shutdown fallback
  stands on (powout, powerofftry, cf9out,
  machinerestart, haltmachine). The disk's own flush
  word stands in diskkeep.nifla (ataflush, Stone 25).
- `src/verses.nifla` — the verse window's kept set
  (Stone 29): twelve beloved verses in exact World
  English Bible wording, each with its reference, and
  the day reckoning that chooses among them
  (versecount, versetext, verseref, verseday).
- `src/helpwords.nifla` — the help window's words
  (Stone 31): five short pages of eleven plain lines
  telling how Cardnull works — every window, every
  typed word, moving windows, the menu, and resting —
  each line at most thirty-six letters, so none is
  cut at either print size (helppages, helplines,
  helptext).

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
