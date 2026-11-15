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

# The screen library joins the build once it exists (Stone 3).
PRELUDE=""
if [ -f src/screenlib.nifla ]; then
    # Word splitting is intended: this is either empty or two words.
    PRELUDE="--prelude src/screenlib.nifla"
fi

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
