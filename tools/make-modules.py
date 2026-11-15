#!/usr/bin/env python3
# Lays the settings module that rides the Cardnull disc
# beside the system and the feather (Stone 4):
#
#   settings.bin — 512 bytes: the letters C and N, then one
#     byte holding the clock's hour offset with 64 added
#     (Eastern -5 is kept as 59; the world's standard time,
#     0, as 64). The disc as built carries Eastern.
#
# This tool once also laid a second module: the feather's
# card — a 32-byte binary card (CNCG, the feather image's
# length, and its FNV-1a checksum) that the system's door
# read beside the feather's image. That half retired with
# the adoption of Nifla's Stone 20 (November 15, 2026):
# feathers now come from the compiler itself
# (niflac --bare --guest --feather) carrying plain-text
# cards at their own heads, and the door reads the card
# from the feather it is handed. What remains here is the
# settings, which are the machine's own and no feather's.
#
# Usage: make-modules.py <settings.bin> [offset-byte]
# The offset byte defaults to 59 (Eastern); the proofs pass
# 64 to lay a disc whose settings carry the world's time.

import sys

settings_out = sys.argv[1]
offset_byte = int(sys.argv[2]) if len(sys.argv) > 2 else 59

settings = bytearray(512)
settings[0] = 67  # C
settings[1] = 78  # N
settings[2] = offset_byte
open(settings_out, "wb").write(settings)

print(f"Modules laid: settings (offset byte {offset_byte}).")
