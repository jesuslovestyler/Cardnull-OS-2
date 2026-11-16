#!/bin/sh
# Builds Cardnull OS 2.
#
#   build/cardnull.elf — the system itself: a bare-metal Nifla
#                        program that boots on its own.
#   build/welcome.feather — the welcome feather (built only when
#                        its source is present, from Stone 5 on),
#                        compiled WITH its card by the compiler's
#                        feather mode (Nifla Stone 20, adopted
#                        here November 15, 2026).
#   build/paint.feather — the paint feather (Stone 24), built
#                        the same way, riding the disc as its
#                        own module beside the welcome feather's.
#
# The compiler is Nifla's own `niflac`; it stays in the Nifla
# repository and is never copied into this one. NIFLA_REPO names
# the Nifla checkout (default ~/workspace/nifla-repo); if its
# niflac has not been built yet, it is built first.

set -e
cd "$(dirname "$0")"

NIFLA_REPO="${NIFLA_REPO:-$HOME/workspace/nifla-repo}"
if [ ! -x "$NIFLA_REPO/niflac" ]; then
    (cd "$NIFLA_REPO" && ./build.sh >/dev/null)
fi

mkdir -p build

# The kernel is several files, never one big one: the main
# body (src/cardnull.nifla) holds the boot sequence and all
# the system's state, and the libraries join it as preludes
# — files of pure functions laid under the body, as if they
# stood at its top. Each is named here, in the order they
# are laid:
#   screenlib  the screen library (Stone 3)
#   clock      the clock's face and the time choice
#   bootmods   reading what the loader brought (Stones 4–5)
#   featherdoor  the feather door (Stone 5)
#   commands   deciding what a typed word is answered with
#   usbkey     ears on the USB road (Stone 6)
#   rtclock    the real clock: the CMOS reading and the
#              calendar reckoning (Stone 7)
#   diskkeep   what the system remembers on a hard disk
#              (Stone 8)
#   font       the letters of the face of light: the
#              hand-drawn bitmap font (Stone 9)
#   pixface    the face of light: the picture screen's
#              desk, its palette, and its drawing (Stone 9)
#   mouse      the pointer: the PS/2 mouse's waking and
#              its packets (Stone 13)
#   speaker    the voice: the PC speaker's notes, timed
#              off the timer's count (Stone 18)
LIBRARIES="src/screenlib.nifla src/clock.nifla src/bootmods.nifla src/featherdoor.nifla src/commands.nifla src/usbkey.nifla src/rtclock.nifla src/diskkeep.nifla src/font.nifla src/pixface.nifla src/mouse.nifla src/speaker.nifla"
PRELUDE=""
for lib in $LIBRARIES; do
    # Word splitting is intended: one --prelude pair per file.
    PRELUDE="$PRELUDE --prelude $lib"
done

# The shipped kernel asks the loader for a picture screen
# (Stone 9): 1024x768, thirty-two bits a pixel. The same
# kernel is also built once without the asking, as
# cardnull-text.elf — the disc laid down with it proves
# the text face's honest fallback (prove-stone9.sh).
# shellcheck disable=SC2086
"$NIFLA_REPO/niflac" --bare --video 1024x768x32 src/cardnull.nifla $PRELUDE -o build/cardnull.elf
# shellcheck disable=SC2086
"$NIFLA_REPO/niflac" --bare src/cardnull.nifla $PRELUDE -o build/cardnull-text.elf

if [ -f src/welcome-feather.nifla ]; then
    # The feather is built WITHOUT the screen-library prelude:
    # as the language stands, a feather's floor blocks must be
    # handed plainly-shaped values where they are handed, and
    # the library's parameterized floor tools are refused in a
    # feather build even when uncalled. The feather carries its
    # own drawing code. (See src/welcome-feather.nifla.)
    "$NIFLA_REPO/niflac" --bare --guest --feather src/welcome-feather.nifla -o build/welcome.feather
    echo "Built build/welcome.feather (the welcome feather, with its card)"
    # The paint feather (Stone 24): a second feather, built
    # the same way — its own source, its own card, laid on
    # the disc as its own module (paint.fea) and received
    # through the same door.
    "$NIFLA_REPO/niflac" --bare --guest --feather src/paint-feather.nifla -o build/paint.feather
    echo "Built build/paint.feather (the paint feather, with its card)"
    # The one small module that still rides beside it on the
    # disc: the settings (Stone 4). The feather's card is no
    # longer a module of its own — it stands at the feather's
    # head, laid there by the compiler (Nifla Stone 20).
    python3 tools/make-modules.py build/settings.bin
fi

echo "Built build/cardnull.elf (Cardnull OS 2)"
