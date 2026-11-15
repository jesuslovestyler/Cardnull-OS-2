#!/bin/sh
# Builds Cardnull OS 2.
#
#   build/cardnull.elf — the system itself: a bare-metal Nifla
#                        program that boots on its own.
#   build/guest.bin    — the welcome guest (built only when its
#                        source is present, from Stone 5 on).
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
#   guestdoor  the guest door (Stone 5)
#   commands   deciding what a typed word is answered with
#   usbkey     ears on the USB road (Stone 6)
#   rtclock    the real clock: the CMOS reading and the
#              calendar reckoning (Stone 7)
LIBRARIES="src/screenlib.nifla src/clock.nifla src/bootmods.nifla src/guestdoor.nifla src/commands.nifla src/usbkey.nifla src/rtclock.nifla"
PRELUDE=""
for lib in $LIBRARIES; do
    # Word splitting is intended: one --prelude pair per file.
    PRELUDE="$PRELUDE --prelude $lib"
done

# shellcheck disable=SC2086
"$NIFLA_REPO/niflac" --bare src/cardnull.nifla $PRELUDE -o build/cardnull.elf

if [ -f src/welcome-guest.nifla ]; then
    # The guest is built WITHOUT the screen-library prelude:
    # as the language stands, a guest's floor blocks must be
    # handed plainly-shaped values where they are handed, and
    # the library's parameterized floor tools are refused in a
    # guest build even when uncalled. The guest carries its
    # own drawing code. (See src/welcome-guest.nifla.)
    "$NIFLA_REPO/niflac" --bare --guest src/welcome-guest.nifla -o build/guest.bin
    echo "Built build/guest.bin (the welcome guest)"
    # The two small modules that ride beside it on the disc:
    # the settings and the guest's card (Stones 4 and 5).
    python3 tools/make-modules.py build/guest.bin build/settings.bin build/card.bin
fi

echo "Built build/cardnull.elf (Cardnull OS 2)"
