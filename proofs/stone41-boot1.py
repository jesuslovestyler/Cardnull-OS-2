# Stone 41 proof, boot 1: the Bible reading window,
# opened by its word, with no disk fitted. The word
# 'bible' opens the window on its contents page —
# decoded line by line against the system's own letter
# shapes: the page names the book (Jonah, whole) and
# its translation (the World English Bible, the verse
# window's own), lists its four chapters as the
# plain-words choice of a passage, and stands the
# picked chapter's line white on blue. The pick moves
# with the arrow keys; Enter reads the picked chapter.
# Every reading page checked here is decoded line by
# line and compared against the bundled text's own
# words — the book of Jonah in src/bibletext.nifla,
# wrapped as the window wraps it (thirty-six letters,
# a blank line between verses, nine lines to a page,
# each chapter on a fresh page) — the pages turned
# forward by the down arrow and by a press on the
# foot's More word, and back by the up arrow and by a
# press on the foot's Back word, the earlier words
# standing again exactly. Jonah 4 is read the same
# way, turned to the book's last page, whose foot
# offers First page; a press on it returns to the
# contents page, and Escape closes the window.
#
# The window's place on this face (1024x768, sixty-four
# cells across): left cell 5, top row 30 — centered, at
# the layout's row 17, like the help window's —
# fifty-four wide, sixteen high, its passage named at
# its top + 1, its page's lines at its left + 2 from
# its top + 3, its foot at its top + 14: the Back word
# at its left + 2, the page's standing at its left + 8,
# and its turning word at its right (More and Read at
# its left + 48, First page at its left + 42).

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

_vals = {}
for _m in re.finditer(r"block\[(\d+)\] = (\d+)",
                      open("src/font.nifla").read()):
    _vals[int(_m.group(1))] = int(_m.group(2))
GLYPHS = {}
for _code in range(32, 127):
    GLYPHS[_code] = tuple(_vals.get((_code - 32) * 8 + _r, 0)
                          for _r in range(8))


def cell_bitmap(d, cx, cy, ink):
    rows = []
    for r in range(8):
        v = 0
        for c in range(8):
            if pixel(d, cx + 2 * c + 1, cy + 2 * r + 1) == ink:
                v |= 1 << (7 - c)
        rows.append(v)
    return tuple(rows)


def decode(d, prow, pcol, text, ink):
    if d[0] < (pcol + len(text)) * 16 or d[1] < (prow + 1) * 16:
        return ""
    out = []
    for i in range(len(text)):
        bm = cell_bitmap(d, (pcol + i) * 16, prow * 16, ink)
        if all(v == 0 for v in bm):
            out.append(" ")
            continue
        best, bestd = None, 999
        for code, g in GLYPHS.items():
            dist = sum(bin(a ^ b).count("1") for a, b in zip(bm, g))
            if dist < bestd:
                bestd, best = dist, code
        out.append(chr(best) if bestd <= 2 else "?")
    return "".join(out)


# The bundled book, page by page, exactly as
# src/bibletext.nifla keeps it, wrapped as the
# window wraps it: the contents page first, then
# Jonah 1 (pages 2 to 12 in the foot's reckoning),
# Jonah 2 (13 to 17), Jonah 3 (18 to 23), and
# Jonah 4 (24 to 30).
CONTENTS = (
     'One whole book stands here:',
     'Jonah, in the World English',
     "Bible's own words.",
     'Pick a chapter:',
     'Jonah 1',
     'Jonah 2',
     'Jonah 3',
     'Jonah 4',
     '',)
PAGES = (
    (
     'One whole book stands here:',
     'Jonah, in the World English',
     "Bible's own words.",
     'Pick a chapter:',
     'Jonah 1',
     'Jonah 2',
     'Jonah 3',
     'Jonah 4',
     '',),
    (
     'Now the word of Yahweh came to Jonah',
     'the son of Amittai, saying,',
     '',
     '"Arise, go to Nineveh, that great',
     'city, and preach against it, for',
     'their wickedness has come up before',
     'me."',
     '',
     'But Jonah rose up to flee to',),
    (
     'Tarshish from the presence of',
     'Yahweh. He went down to Joppa, and',
     'found a ship going to Tarshish; so',
     'he paid its fare, and went down into',
     'it, to go with them to Tarshish from',
     'the presence of Yahweh.',
     '',
     'But Yahweh sent out a great wind on',
     'the sea, and there was a mighty',),
    (
     'storm on the sea, so that the ship',
     'was likely to break up.',
     '',
     'Then the mariners were afraid, and',
     'every man cried to his god. They',
     'threw the cargo that was in the ship',
     'into the sea to lighten the ship.',
     'But Jonah had gone down into the',
     'innermost parts of the ship, and he',),
    (
     'was laying down, and was fast',
     'asleep.',
     '',
     'So the shipmaster came to him, and',
     'said to him, "What do you mean,',
     'sleeper? Arise, call on your God!',
     'Maybe your God will notice us, so',
     'that we won\'t perish."',
     '',),
    (
     'They all said to each other, "Come,',
     'let us cast lots, that we may know',
     'who is responsible for this evil',
     'that is on us." So they cast lots,',
     'and the lot fell on Jonah.',
     '',
     'Then they asked him, "Tell us,',
     'please, for whose cause this evil is',
     'on us. What is your occupation?',),
    (
     'Where do you come from? What is your',
     'country? Of what people are you?"',
     '',
     'He said to them, "I am a Hebrew, and',
     'I fear Yahweh, the God of heaven,',
     'who has made the sea and the dry',
     'land."',
     '',
     'Then were the men exceedingly',),
    (
     'afraid, and said to him, "What is',
     'this that you have done?" For the',
     'men knew that he was fleeing from',
     'the presence of Yahweh, because he',
     'had told them.',
     '',
     'Then they said to him, "What shall',
     'we do to you, that the sea may be',
     'calm to us?" For the sea grew more',),
    (
     'and more stormy.',
     '',
     'He said to them, "Take me up, and',
     'throw me into the sea. Then the sea',
     'will be calm for you; for I know',
     'that because of me this great storm',
     'is on you."',
     '',
     'Nevertheless the men rowed hard to',),
    (
     'get them back to the land; but they',
     'could not, for the sea grew more and',
     'more stormy against them.',
     '',
     'Therefore they cried to Yahweh, and',
     'said, "We beg you, Yahweh, we beg',
     "you, don't let us die for this man's",
     "life, and don't lay on us innocent",
     'blood; for you, Yahweh, have done as',),
    (
     'it pleased you."',
     '',
     'So they took up Jonah, and threw him',
     'into the sea; and the sea ceased its',
     'raging.',
     '',
     'Then the men feared Yahweh',
     'exceedingly; and they offered a',
     'sacrifice to Yahweh, and made vows.',),
    (
     '',
     'Yahweh prepared a great fish to',
     'swallow up Jonah, and Jonah was in',
     'the belly of the fish three days and',
     'three nights.',
     '',
     '',
     '',
     '',),
    (
     'Then Jonah prayed to Yahweh, his',
     "God, out of the fish's belly.",
     '',
     'He said, "I called because of my',
     'affliction to Yahweh. He answered',
     'me. Out of the belly of Sheol I',
     'cried. You heard my voice.',
     '',
     'For you threw me into the depths, in',),
    (
     'the heart of the seas. The flood was',
     'all around me. All your waves and',
     'your billows passed over me.',
     '',
     "I said, 'I have been banished from",
     'your sight; yet I will look again',
     "toward your holy temple.'",
     '',
     'The waters surrounded me, even to',),
    (
     'the soul. The deep was around me.',
     'The weeds were wrapped around my',
     'head.',
     '',
     'I went down to the bottoms of the',
     'mountains. The earth barred me in',
     'forever: yet have you brought up my',
     'life from the pit, Yahweh my God.',
     '',),
    (
     '"When my soul fainted within me, I',
     'remembered Yahweh. My prayer came in',
     'to you, into your holy temple.',
     '',
     'Those who regard lying vanities',
     'forsake their own mercy.',
     '',
     'But I will sacrifice to you with the',
     'voice of thanksgiving. I will pay',),
    (
     'that which I have vowed. Salvation',
     'belongs to Yahweh."',
     '',
     'Yahweh spoke to the fish, and it',
     'vomited out Jonah on the dry land.',
     '',
     '',
     '',
     '',),
    (
     'The word of Yahweh came to Jonah the',
     'second time, saying,',
     '',
     '"Arise, go to Nineveh, that great',
     'city, and preach to it the message',
     'that I give you."',
     '',
     'So Jonah arose, and went to Nineveh,',
     'according to the word of Yahweh. Now',),
    (
     'Nineveh was an exceedingly great',
     "city, three days' journey across.",
     '',
     'Jonah began to enter into the city a',
     "day's journey, and he cried out, and",
     'said, "In forty days, Nineveh will',
     'be overthrown!"',
     '',
     'The people of Nineveh believed God;',),
    (
     'and they proclaimed a fast, and put',
     'on sackcloth, from the greatest of',
     'them even to the least of them.',
     '',
     'The news reached the king of',
     'Nineveh, and he arose from his',
     'throne, and took off his royal robe,',
     'covered himself with sackcloth, and',
     'sat in ashes.',),
    (
     '',
     'He made a proclamation and published',
     'through Nineveh by the decree of the',
     'king and his nobles, saying, "Let',
     'neither man nor animal, herd nor',
     'flock, taste anything; let them not',
     'feed, nor drink water;',
     '',
     'but let them be covered with',),
    (
     'sackcloth, both man and animal, and',
     'let them cry mightily to God. Yes,',
     'let them turn everyone from his evil',
     'way, and from the violence that is',
     'in his hands.',
     '',
     'Who knows whether God will not turn',
     'and relent, and turn away from his',
     'fierce anger, so that we might not',),
    (
     'perish?"',
     '',
     'God saw their works, that they',
     'turned from their evil way. God',
     'relented of the disaster which he',
     'said he would do to them, and he',
     "didn't do it.",
     '',
     '',),
    (
     'But it displeased Jonah exceedingly,',
     'and he was angry.',
     '',
     'He prayed to Yahweh, and said,',
     '"Please, Yahweh, wasn\'t this what I',
     'said when I was still in my own',
     'country? Therefore I hurried to flee',
     'to Tarshish, for I knew that you are',
     'a gracious God, and merciful, slow',),
    (
     'to anger, and abundant in loving',
     'kindness, and you relent of doing',
     'harm.',
     '',
     'Therefore now, Yahweh, take, I beg',
     'you, my life from me; for it is',
     'better for me to die than to live."',
     '',
     'Yahweh said, "Is it right for you to',),
    (
     'be angry?"',
     '',
     'Then Jonah went out of the city, and',
     'sat on the east side of the city,',
     'and there made himself a booth, and',
     'sat under it in the shade, until he',
     'might see what would become of the',
     'city.',
     '',),
    (
     'Yahweh God prepared a vine, and made',
     'it to come up over Jonah, that it',
     'might be a shade over his head, to',
     'deliver him from his discomfort. So',
     'Jonah was exceedingly glad because',
     'of the vine.',
     '',
     'But God prepared a worm at dawn the',
     'next day, and it chewed on the vine,',),
    (
     'so that it withered.',
     '',
     'It happened, when the sun arose,',
     'that God prepared a sultry east',
     "wind; and the sun beat on Jonah's",
     'head, so that he fainted, and',
     'requested for himself that he might',
     'die, and said, "It is better for me',
     'to die than to live."',),
    (
     '',
     'God said to Jonah, "Is it right for',
     'you to be angry about the vine?" He',
     'said, "I am right to be angry, even',
     'to death."',
     '',
     'Yahweh said, "You have been',
     'concerned for the vine, for which',
     'you have not labored, neither made',),
    (
     'it grow; which came up in a night,',
     'and perished in a night.',
     '',
     "Shouldn't I be concerned for",
     'Nineveh, that great city, in which',
     'are more than one hundred twenty',
     "thousand persons who can't discern",
     'between their right hand and their',
     'left hand; and also much livestock?"',),
)

BX, BY = 5, 30

# The pointer's point, tracked as the bench moves it:
# it starts at the screen's middle (506, 378).
CUR = [506, 378]


def move_to(x, y):
    # The point is walked in short steps: one great
    # move saturates the pointer's reckoning on the
    # bench, and its steps are lost.
    while CUR[0] != x or CUR[1] != y:
        dx = max(-61, min(61, x - CUR[0]))
        dy = max(-61, min(61, y - CUR[1]))
        mousemove(dx, dy)
        CUR[0] += dx
        CUR[1] += dy


def check_page(d, page, name):
    """The standing page's passage name and every one
    of its nine lines decode exactly, and its foot
    names the page."""
    said = decode(d, BY + 1, BX + 2, name, BLACK)
    expect(said == name,
           f"the page stands under its passage's name {name!r} (read: {said!r})")
    for i, line in enumerate(PAGES[page]):
        if line == "":
            continue
        said = decode(d, BY + 3 + i, BX + 2, line, BLACK)
        expect(said == line,
               f"page {page + 1}'s line {i + 1} reads exactly (read: {said!r})")
    foot = f"Page {page + 1} of 30"
    said = decode(d, BY + 14, BX + 8, foot, BLACK)
    expect(said == foot,
           f"the foot names the standing page {foot!r} (read: {said!r})")


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

# The word 'bible' opens the window on its contents page.
typewrite("bible")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, BY, BX + 1, "Bible", WHITE) == "Bible", 25)
expect(d is not None, "the word 'bible' opened the Bible window")
if d:
    expect(pixel(d, 200, BY * 16 + 8) == BLUE,
           "the Bible window stands forward, its title bar blue")
    said = decode(d, BY + 1, BX + 2, "Jonah", BLACK)
    expect(said == "Jonah",
           f"the contents page names the book (read: {said!r})")
    for i, line in enumerate(CONTENTS):
        if line == "":
            continue
        ink = WHITE if i == 4 else BLACK
        said = decode(d, BY + 3 + i, BX + 2, line, ink)
        expect(said == line,
               f"the contents page's line {i + 1} reads exactly (read: {said!r})")
    foot = "Page 1 of 30"
    said = decode(d, BY + 14, BX + 8, foot, BLACK)
    expect(said == foot,
           f"the foot names the contents page {foot!r} (read: {said!r})")
    said = decode(d, BY + 14, BX + 48, "Read", WHITE)
    expect(said == "Read",
           f"the contents page's foot offers 'Read' (read: {said!r})")

# The down arrow moves the pick to Jonah 2.
sendkey("down")
d = waitdump(lambda d: d is not None
             and decode(d, BY + 3 + 5, BX + 2, "Jonah 2", WHITE) == "Jonah 2", 15)
expect(d is not None, "the down arrow moved the pick to Jonah 2")
if d:
    said = decode(d, BY + 3 + 4, BX + 2, "Jonah 1", BLACK)
    expect(said == "Jonah 1",
           f"Jonah 1's line stands plain again (read: {said!r})")

# The up arrow moves the pick back to Jonah 1.
sendkey("up")
d = waitdump(lambda d: d is not None
             and decode(d, BY + 3 + 4, BX + 2, "Jonah 1", WHITE) == "Jonah 1", 15)
expect(d is not None, "the up arrow moved the pick back to Jonah 1")

# Enter reads the picked chapter: Jonah 1's first page.
enter()
d = waitdump(lambda d: d is not None
             and decode(d, BY + 1, BX + 2, "Jonah 1", BLACK) == "Jonah 1"
             and decode(d, BY + 14, BX + 8, "Page 2 of 30", BLACK) == "Page 2 of 30", 15)
expect(d is not None, "Enter read the picked chapter, Jonah 1")
if d:
    check_page(d, 1, "Jonah 1")
    said = decode(d, BY + 14, BX + 2, "Back", WHITE)
    expect(said == "Back",
           f"the foot offers 'Back' (read: {said!r})")
    said = decode(d, BY + 14, BX + 48, "More", WHITE)
    expect(said == "More",
           f"the foot offers 'More' (read: {said!r})")

# The down arrow turns to Jonah 1's second page: the
# passage's later words.
sendkey("down")
d = waitdump(lambda d: d is not None
             and decode(d, BY + 14, BX + 8, "Page 3 of 30", BLACK) == "Page 3 of 30", 15)
expect(d is not None, "the down arrow turned to Jonah 1's second page")
if d:
    check_page(d, 2, "Jonah 1")

# A press on the foot's More word turns to the third
# page. The point walks from the screen's middle to
# the More word's center (872, 712).
move_to(872, 712)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, BY + 14, BX + 8, "Page 4 of 30", BLACK) == "Page 4 of 30", 15)
expect(d is not None, "a press on the foot's More word turned to Jonah 1's third page")
if d:
    check_page(d, 3, "Jonah 1")

# The up arrow turns back: the second page's words
# stand again, exactly.
sendkey("up")
d = waitdump(lambda d: d is not None
             and decode(d, BY + 14, BX + 8, "Page 3 of 30", BLACK) == "Page 3 of 30", 15)
expect(d is not None, "the up arrow turned back to Jonah 1's second page")
if d:
    check_page(d, 2, "Jonah 1")

# A press on the foot's Back word turns back to the
# first page. The point walks from (872, 712) to the
# Back word's center (120, 712).
move_to(120, 712)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, BY + 14, BX + 8, "Page 2 of 30", BLACK) == "Page 2 of 30", 15)
expect(d is not None, "a press on the foot's Back word turned back to Jonah 1's first page")
if d:
    said = decode(d, BY + 3, BX + 2, PAGES[1][0], BLACK)
    expect(said == PAGES[1][0],
           f"the first page's first line stands again (read: {said!r})")

# The up arrow on the chapter's first page returns to
# the contents page.
sendkey("up")
d = waitdump(lambda d: d is not None
             and decode(d, BY + 14, BX + 8, "Page 1 of 30", BLACK) == "Page 1 of 30", 15)
expect(d is not None, "the up arrow returned to the contents page")

# The pick walks down to Jonah 4, and Enter reads it.
sendkey("down")
sendkey("down")
sendkey("down")
d = waitdump(lambda d: d is not None
             and decode(d, BY + 3 + 7, BX + 2, "Jonah 4", WHITE) == "Jonah 4", 15)
expect(d is not None, "the pick walked down to Jonah 4")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, BY + 1, BX + 2, "Jonah 4", BLACK) == "Jonah 4"
             and decode(d, BY + 14, BX + 8, "Page 24 of 30", BLACK) == "Page 24 of 30", 15)
expect(d is not None, "Enter read Jonah 4")
if d:
    check_page(d, 23, "Jonah 4")

# Six turns of the down arrow reach the book's last
# page: Jonah 4's own last words, and First page at
# the foot.
for _ in range(6):
    sendkey("down")
d = waitdump(lambda d: d is not None
             and decode(d, BY + 14, BX + 8, "Page 30 of 30", BLACK) == "Page 30 of 30", 15)
expect(d is not None, "the down arrow turned to the book's last page")
if d:
    check_page(d, 29, "Jonah 4")
    # The arrow stands where the Back press left it —
    # clear of the foot's right end — so the turning
    # word is read as it stands.
    said = decode(d, BY + 14, BX + 42, "First page", WHITE)
    expect(said == "First page",
           f"the last page's foot offers 'First page' (read: {said!r})")

# A press on First page returns to the contents page.
# The point walks from (120, 712) to that word's center
# (872, 712).
move_to(872, 712)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, BY + 14, BX + 8, "Page 1 of 30", BLACK) == "Page 1 of 30", 15)
expect(d is not None, "a press on First page returned to the contents page")

# Escape closes the window back to the desktop.
sendkey("esc")
d = waitdump(lambda d: d is not None
             and pixel(d, 200, BY * 16 + 8) == BLACK, 15)
expect(d is not None, "Escape closed the Bible window")

done()
