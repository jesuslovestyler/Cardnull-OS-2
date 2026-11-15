#!/usr/bin/env python3
# Lays the two small modules that ride the Cardnull disc
# beside the system and the guest (Stones 4 and 5):
#
#   settings.bin — 512 bytes: the letters C and N, then one
#     byte holding the clock's hour offset with 64 added
#     (Eastern -5 is kept as 59; the world's standard time,
#     0, as 64). The disc as built carries Eastern.
#   card.bin — 32 bytes: the letters C, N, C, G, then the
#     guest image's length and its FNV-1a checksum (the
#     64-bit form, reckoned here over the guest's file),
#     each as an eight-byte number.
#
# Usage: make-modules.py <guest.bin> <settings.bin> <card.bin> [offset-byte]
# The offset byte defaults to 59 (Eastern); the proofs pass
# 64 to lay a disc whose settings carry the world's time.

import struct
import sys

guest_path, settings_out, card_out = sys.argv[1:4]
offset_byte = int(sys.argv[4]) if len(sys.argv) > 4 else 59

guest = open(guest_path, "rb").read()
h = 0xCBF29CE484222325
for b in guest:
    h = ((h ^ b) * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF

settings = bytearray(512)
settings[0] = 67  # C
settings[1] = 78  # N
settings[2] = offset_byte
open(settings_out, "wb").write(settings)

card = bytearray(32)
card[0:4] = b"CNCG"
struct.pack_into("<Q", card, 8, len(guest))
struct.pack_into("<Q", card, 16, h)
open(card_out, "wb").write(card)

print(f"Modules laid: settings (offset byte {offset_byte}), "
      f"card for a guest of {len(guest)} bytes.")
