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
    # shellcheck disable=SC2086
    "$NIFLA_REPO/niflac" --bare --guest src/welcome-guest.nifla $PRELUDE -o build/guest.bin
    echo "Built build/guest.bin (the welcome guest)"
fi

echo "Built build/cardnull.elf (Cardnull OS 2)"
